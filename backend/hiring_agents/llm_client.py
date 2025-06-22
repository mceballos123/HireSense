"""
LLM Client for uAgents Hiring System
===================================

This file contains the shared LLM client that all uAgents use to communicate with ASI:One.
"""

import aiohttp
import ssl
import json
import re
from typing import Dict

# ASI:One API configuration
ASI_API_KEY = "sk_d1a256183aa249f49f49d649dddff42ca039df035fb7404394efe289149d9997"
ASI_API_URL = "https://api.asi1.ai/v1/chat/completions"


class SimpleLLMAgent:
    """Base class for LLM-powered agents"""

    def __init__(self, name: str):
        self.name = name
        self.api_key = ASI_API_KEY
        self.api_url = ASI_API_URL

    async def query_llm(self, prompt: str) -> dict:
        """Query ASI1.ai API with a prompt and get response"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "model": "asi1-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a specialized AI agent for hiring analysis. Provide clear, structured responses.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "stream": False,
            "max_tokens": 800,
        }

        try:
            print(f"🔗 {self.name}: Querying ASI:One API")

            # Create SSL context to bypass certificate verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    self.api_url, headers=headers, json=payload, timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "content": result["choices"][0]["message"]["content"],
                        }
                    else:
                        error_text = await response.text()
                        print(
                            f"❌ {self.name}: API Error {response.status}: {error_text}"
                        )
                        return {
                            "success": False,
                            "content": f"API Error {response.status}: {error_text}",
                        }
        except Exception as e:
            print(f"💥 {self.name}: Error querying ASI:One: {e}")
            return {"success": False, "content": f"Request Error: {str(e)}"}

    def parse_json_response(self, content: str) -> Dict:
        """Parse JSON response from LLM, handling markdown formatting"""
        try:
            # Remove markdown code blocks if present
            content = re.sub(
                r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE
            )
            content = content.strip()
            return json.loads(content)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ {self.name}: JSON parsing error: {e}")
            return {}
