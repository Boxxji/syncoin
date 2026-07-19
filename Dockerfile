FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir websockets numpy scikit-learn

COPY bioacoustic_worker.py .
COPY syncoin_node.py .

EXPOSE 8766

CMD ["python3", "syncoin_node.py"]
