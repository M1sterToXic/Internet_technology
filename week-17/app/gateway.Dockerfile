FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY weeks/week-17/app/proto ./proto
COPY weeks/week-17/app/gateway ./gateway
ENV PYTHONPATH=/app/proto
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
