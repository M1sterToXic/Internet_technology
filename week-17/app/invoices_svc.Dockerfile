FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY weeks/week-17/app/proto ./proto
COPY weeks/week-17/app/invoices_svc ./invoices_svc
ENV PYTHONPATH=/app/proto
CMD ["python", "invoices_svc/main.py"]
