FROM python:3.12-slim
WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ../api ./api
WORKDIR /backend/api
CMD ["python","file_upload_server_simple.py"]