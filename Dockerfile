FROM python:3.13-slim-trixie

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py metricas_linux.py .

EXPOSE 9000
CMD ["python", "main.py"]
