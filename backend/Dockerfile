FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p logs

COPY . .

# Gunicornでアプリを起動（ホスト0.0.0.0にバインド）
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
