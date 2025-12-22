FROM python:3.12-slim
WORKDIR /backend

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ../hiring_agents ./hiring_agents
WORKDIR /backend/hiring_agents
CMD ["python","pro_hire_agent.py"]

