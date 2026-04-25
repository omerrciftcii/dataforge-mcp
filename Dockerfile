# 1. Hafif bir Python imajı seçiyoruz
FROM python:3.11-slim

# 2. Çalışma dizinimizi belirliyoruz
WORKDIR /app

# 3. Sistem bağımlılıklarını kuruyoruz (Matplotlib ve diğerleri için gerekli paketler)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Bağımlılık dosyasını kopyalıyoruz
# Conda kullanmıştık ama Docker içinde daha hafif olması için requirements.txt kullanacağız
COPY requirements.txt .

# 5. Python kütüphanelerini kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 6. Kaynak kodlarımızı kopyalıyoruz
COPY src/ ./src/

# 7. Çıktı ve veri dizinlerini oluşturuyoruz
RUN mkdir -p output

# 8. Python'a src klasörünü bir paket olarak tanıtıyoruz
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# 9. MCP sunucusunu başlatıyoruz (stdio üzerinden çalıştığı için entrypoint önemli)
ENTRYPOINT ["python", "src/dataforge/server.py"]