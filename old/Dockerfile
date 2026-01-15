FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema para impresoras
RUN apt-get update && apt-get install -y \
    cups \
    libcups2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]