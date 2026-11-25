# ClassroomPortal Production Container Image
FROM python:3.11-slim

# Set environment flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy dependency requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn waitress

# Copy project source code
COPY . .

# Ensure storage directories exist
RUN mkdir -p uploads/materials uploads/submissions

# Expose HTTP port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Start production server
CMD ["gunicorn", "wsgi:app", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:5000"]
