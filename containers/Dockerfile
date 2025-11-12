FROM python:3.11-slim
WORKDIR /app

COPY cd_req.txt ./requirements.txt
COPY model_server.py .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Accept build-time args and bake them as environment variables ---
ARG MODEL_NAME
ARG MODEL_VERSION
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_VERSION=${MODEL_VERSION}

EXPOSE 8200

CMD ["uvicorn", "model_server:app", "--host", "0.0.0.0", "--port", "8200"]
