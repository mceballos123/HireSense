"""
Test ASI:One API Connection
===========================

Simple script to test the ASI:One API connection and verify the setup.
"""

import asyncio
import aiohttp
import json
import ssl

# Test different API configurations
API_CONFIGS = [
    {
        "name": "ASI1.ai API",
        "url": "https://api.asi1.ai/v1/chat/completions",
        "key": "sk_d1a256183aa249f49f49d649dddff42ca039df035fb7404394efe289149d9997",
        "ssl_context": False
    }
]

async def test_api_connection(config):
    """Test a specific API configuration"""
    print(f"\n🧪 Testing: {config['name']}")
    print(f"🔗 URL: {config['url']}")
    print(f"🔑 Key: {config['key'][:20]}...")
    
    headers = {
        "Authorization": f"Bearer {config['key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "asi1-mini",
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'API connection successful' if you can see this message."}
        ],
        "temperature": 0.1,
        "stream": False,
        "max_tokens": 50
    }
    
    try:
        print("📡 Making API request...")
        
        # Create SSL context
        if config.get("ssl_context") is False:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)
        else:
            connector = None
        
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(config['url'], headers=headers, json=payload, timeout=30) as response:
                print(f"📊 Response Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ SUCCESS! Response: {content}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ ERROR {response.status}: {error_text}")
                    return False
                    
    except aiohttp.ClientConnectorError as e:
        print(f"🔌 Connection Error: {e}")
        return False
    except asyncio.TimeoutError:
        print("⏰ Request timeout")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

async def main():
    """Test all API configurations"""
    print("🚀 ASI:One API Connection Test")
    print("="*50)
    
    successful_configs = []
    
    for config in API_CONFIGS:
        success = await test_api_connection(config)
        if success:
            successful_configs.append(config)
    
    print("\n" + "="*50)
    print("📋 TEST RESULTS")
    print("="*50)
    
    if successful_configs:
        print("✅ SUCCESSFUL CONFIGURATIONS:")
        for config in successful_configs:
            print(f"  - {config['name']}")
            print(f"    URL: {config['url']}")
            print(f"    Key: {config['key'][:20]}...")
    else:
        print("❌ NO SUCCESSFUL CONFIGURATIONS")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. Check your internet connection")
        print("2. Verify your API key is correct")
        print("3. Make sure you have credits in your ASI:One account")
        print("4. Try using a different API endpoint")
        print("5. Check if the API service is available")
        print("6. The API might be using a different endpoint - check ASI:One documentation")

if __name__ == "__main__":
    asyncio.run(main()) 