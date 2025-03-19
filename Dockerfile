FROM python:3.9-slim

WORKDIR /app

# Install necessary tools
RUN apt-get update && \
    apt-get install -y net-tools && \
    rm -rf /var/lib/apt/lists/*

# Create FTP user
RUN useradd -m -d /app/virtual_fs ftpuser

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .
COPY .env .

# Create directory for virtual filesystem and setup initial files
RUN mkdir -p /app/virtual_fs /app/logs && \
    python filesystem_generator.py && \
    chown -R ftpuser:ftpuser /app/virtual_fs /app/logs && \
    chmod -R 755 /app/virtual_fs

# Switch to ftpuser for running the server
USER ftpuser

# Expose FTP control port and passive ports
EXPOSE 2121
EXPOSE 30000-30010

# Run the honeypot
CMD ["python", "honeypot.py"] 