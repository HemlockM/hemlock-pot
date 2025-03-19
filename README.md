# FTP Honeypot

A honeypot that simulates an FTP server to track and monitor potential attackers. It creates a virtual file system environment that logs all interactions and can send notifications to a specified endpoint.

## Features

- Simulated FTP server with configurable credentials
- Virtual file system with trap files
- Detailed logging of all interactions
- Real-time notifications to external endpoint
- Docker support for easy deployment

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your settings:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` with your desired configuration

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t ftp-honeypot .
   ```

2. Run the container:
   ```bash
   docker run -d \
     -p 2121:2121 \
     -v $(pwd)/logs:/app/logs \
     --name ftp-honeypot \
     ftp-honeypot
   ```

## Running without Docker

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the honeypot:
   ```bash
   python src/honeypot.py
   ```

## Configuration

- `FTP_PORT`: Port for the FTP server (default: 2121)
- `FTP_USER`: Username for FTP authentication
- `FTP_PASSWORD`: Password for FTP authentication
- `HONEYPOT_DIR`: Directory for virtual filesystem
- `NOTIFICATION_ENDPOINT`: URL to send activity notifications

## Logging

All activities are logged to:
- Console output
- `honeypot.log` file
- Specified notification endpoint (if configured)

## Security Notes

- This is a honeypot system designed to track potential attackers
- Do not deploy on production systems without proper security measures
- Regularly monitor logs and notifications
- Keep credentials and endpoints secure

## License

MIT License