FROM python:3.6

WORKDIR /app

RUN pip install boto3
RUN pip install requests_aws4auth
RUN pip install elasticsearch
RUN pip install elasticsearch-curator

COPY delete-indexes.py .

CMD ["python", "delete-indexes.py"]
