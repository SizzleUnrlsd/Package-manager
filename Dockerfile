FROM python:3.9-slim
COPY server/server.py /app/server.py
COPY requirements.txt /app/requirements.txt
COPY data.json /data/data.json
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "server.py"]
