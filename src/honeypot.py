import os
import json
import logging
from datetime import datetime
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/honeypot.log'),
        logging.StreamHandler()
    ]
)

class HoneypotFTPHandler(FTPHandler):
    def on_connect(self):
        """Log connection attempts"""
        self.log_activity('connect', {
            'ip': self.remote_ip,
            'port': self.remote_port
        })
        super().on_connect()

    def on_disconnect(self):
        """Log disconnection"""
        self.log_activity('disconnect', {
            'ip': self.remote_ip
        })
        super().on_disconnect()

    def on_login(self, username):
        """Log login attempts"""
        self.log_activity('login_attempt', {
            'ip': self.remote_ip,
            'username': username
        })
        super().on_login(username)

    def on_login_failed(self, username):
        """Log failed login attempts"""
        self.log_activity('login_failed', {
            'ip': self.remote_ip,
            'username': username
        })
        super().on_login_failed(username)

    def on_file_sent(self, file):
        """Log when files are downloaded"""
        self.log_activity('file_download', {
            'ip': self.remote_ip,
            'file': file
        })
        super().on_file_sent(file)

    def on_file_received(self, file):
        """Log when files are uploaded"""
        self.log_activity('file_upload', {
            'ip': self.remote_ip,
            'file': file
        })
        super().on_file_received(file)

    def on_incomplete_file_sent(self, file):
        """Log interrupted downloads"""
        self.log_activity('incomplete_download', {
            'ip': self.remote_ip,
            'file': file
        })
        super().on_incomplete_file_sent(file)

    def on_incomplete_file_received(self, file):
        """Log interrupted uploads"""
        self.log_activity('incomplete_upload', {
            'ip': self.remote_ip,
            'file': file
        })
        super().on_incomplete_file_received(file)

    def log_activity(self, activity_type, data):
        """Log activity to file and send to endpoint"""
        timestamp = datetime.now().isoformat()
        log_data = {
            'timestamp': timestamp,
            'type': activity_type,
            **data
        }
        
        # Log locally
        logging.info(f"Activity detected: {json.dumps(log_data)}")
        
        # Send to endpoint if configured
        endpoint_url = os.getenv('NOTIFICATION_ENDPOINT')
        if endpoint_url:
            try:
                requests.post(endpoint_url, json=log_data, timeout=5)
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to send data to endpoint: {e}")

def main():
    # Load environment variables
    load_dotenv()
    
    # Configuration
    FTP_PORT = int(os.getenv('FTP_PORT', 2121))
    FTP_USER = os.getenv('FTP_USER', 'ftpuser')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD', 'password123')
    HONEYPOT_DIR = os.getenv('HONEYPOT_DIR', '/app/virtual_fs')

    # Create authorizer
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, HONEYPOT_DIR, perm='elradfmw')

    # Initialize handler with passive mode configuration
    handler = HoneypotFTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(30000, 30010)
    handler.masquerade_address = '127.0.0.1'

    # Create FTP server
    server = FTPServer(('0.0.0.0', FTP_PORT), handler)
    
    logging.info(f"Starting FTP Honeypot on port {FTP_PORT}")
    server.serve_forever()

if __name__ == '__main__':
    main() 