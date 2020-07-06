FROM python:3

WORKDIR /app

RUN pip install botocore
COPY delete-indexes.py .

CMD ["python", "delete-indexes.py"]
