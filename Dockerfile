FROM python:3.11-slim

WORKDIR /app

COPY syncoin_node.py .

EXPOSE 8766

CMD ["python3", "-c", "import syncoin_node; n = syncoin_node.SynCoinNode(); n.start(); import time; time.sleep(99999)"]
