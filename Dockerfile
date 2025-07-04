# Create env
FROM python:3.13.5-slim


# Setup work dir
WORKDIR /app


# Copy and install dependecies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apt-get update && apt-get install -y \
    bash \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy code
COPY . .


# Expose port
EXPOSE 8000


CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]