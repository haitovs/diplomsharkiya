FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

# Copy optional directories only if they exist
COPY scripts/ ./scripts/
COPY .streamlit/ ./.streamlit/

EXPOSE 4084

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:4084/_stcore/health || exit 1

CMD ["streamlit", "run", "src/0_🏠_Home.py", \
    "--server.port=4084", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
