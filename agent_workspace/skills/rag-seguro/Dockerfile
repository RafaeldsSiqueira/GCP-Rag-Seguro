FROM python:3.12-slim

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo-fonte
COPY . .

# Define PYTHONPATH para encontrar os modulos em src/
ENV PYTHONPATH=/app

# Expoe a porta do Cloud Run
EXPOSE 8080

# Inicia a API FastAPI com Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
