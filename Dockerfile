FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV ENV_FILE=/env/.env

COPY /app .
CMD ["python", "app.py"]