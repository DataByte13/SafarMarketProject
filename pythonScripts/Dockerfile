FROM python:3.9-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir requests pandas pymysql
RUN pip install pymysql cryptography
CMD ["python", "./CrowlerScript.py"]
