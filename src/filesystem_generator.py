import os
import json
import random
from datetime import datetime, timedelta

class FileSystemGenerator:
    def __init__(self, base_path):
        self.base_path = base_path
        
    def _write_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
            
    def generate_config_files(self):
        # Apache configuration
        apache_config = """
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""
        self._write_file(os.path.join(self.base_path, 'etc/apache2/sites-available/000-default.conf'), apache_config)

        # MySQL configuration
        mysql_config = """
[mysqld]
user = mysql
pid-file = /var/run/mysqld/mysqld.pid
socket = /var/run/mysqld/mysqld.sock
port = 3306
basedir = /usr
datadir = /var/lib/mysql
tmpdir = /tmp
bind-address = 127.0.0.1
key_buffer_size = 16M
max_allowed_packet = 16M
"""
        self._write_file(os.path.join(self.base_path, 'etc/mysql/my.cnf'), mysql_config)

    def generate_web_files(self):
        # Main website files
        index_html = """
<!DOCTYPE html>
<html>
<head><title>Company Internal Portal</title></head>
<body>
    <h1>Welcome to Internal Portal</h1>
    <p>Please log in to access secure resources.</p>
</body>
</html>
"""
        self._write_file(os.path.join(self.base_path, 'var/www/html/index.html'), index_html)

        # PHP configuration file with "sensitive" data
        config_php = """
<?php
// Database Configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'admin');
define('DB_PASS', 'super_secret_password_123');
define('DB_NAME', 'company_db');

// API Keys
$api_keys = array(
    'stripe' => 'sk_test_123456789',
    'aws' => 'AKIA1234567890EXAMPLE',
    'gmail' => 'oauth:1234567890abcdef'
);
?>
"""
        self._write_file(os.path.join(self.base_path, 'var/www/html/includes/config.php'), config_php)

    def generate_log_files(self):
        # Generate fake access logs
        ips = ['192.168.1.' + str(i) for i in range(100, 200)]
        paths = ['/login.php', '/admin/', '/wp-admin/', '/includes/config.php', '/user/profile']
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-G960U)'
        ]
        
        log_entries = []
        current_time = datetime.now()
        
        for i in range(1000):
            ip = random.choice(ips)
            path = random.choice(paths)
            user_agent = random.choice(user_agents)
            status = random.choice(['200', '404', '403', '500'])
            timestamp = (current_time - timedelta(minutes=i)).strftime('%d/%b/%Y:%H:%M:%S +0000')
            
            log_entry = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" {status} 1234 "-" "{user_agent}"'
            log_entries.append(log_entry)
        
        self._write_file(
            os.path.join(self.base_path, 'var/log/apache2/access.log'),
            '\n'.join(log_entries)
        )

    def generate_backup_files(self):
        # Fake database backup
        db_backup = """
-- MySQL dump 10.13  Distrib 5.7.33
-- Host: localhost    Database: company_db
-- ------------------------------------------------------
-- Server version 5.7.33

CREATE TABLE users (
  id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  password_hash varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users VALUES 
(1,'admin','$2y$10$Ht1KRV2c4y6m3Q', 'admin@company.com'),
(2,'john.doe','$2y$10$Xs3F9k2c4y6m3Q', 'john@company.com');

CREATE TABLE customer_data (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  credit_card varchar(255) NOT NULL,
  PRIMARY KEY (id)
);
"""
        self._write_file(os.path.join(self.base_path, 'var/backups/db_backup_latest.sql'), db_backup)

        # Fake SSH keys
        ssh_private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvt9y2j6Lw9IGp3HK8Fs4CJZ6giJ4KZhvZ9xuGHT6r7z8rgAB
... [truncated for security] ...
KvkqGJqTw4ZJUwwGJsV5OQWjHAAqaNPwW3Zm0wYjBxkj/hQu
-----END RSA PRIVATE KEY-----
"""
        self._write_file(os.path.join(self.base_path, 'home/admin/.ssh/id_rsa'), ssh_private_key)

    def generate_development_files(self):
        # Git configuration with "sensitive" data
        git_config = """
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[remote "origin"]
    url = https://github-token:ghp_1234567890abcdef@github.com/company/secret-repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[user]
    email = developer@company.com
    name = Lead Developer
"""
        self._write_file(os.path.join(self.base_path, 'var/www/html/.git/config'), git_config)

        # Environment file with "secrets"
        env_file = """
# Production Environment Variables
DB_PASSWORD=prod_db_password_123
AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_SECRET_KEY=sk_live_123456789
JWT_SECRET=super_secret_jwt_token_123
"""
        self._write_file(os.path.join(self.base_path, 'var/www/html/.env'), env_file)

    def generate_all(self):
        """Generate the entire file structure"""
        self.generate_config_files()
        self.generate_web_files()
        self.generate_log_files()
        self.generate_backup_files()
        self.generate_development_files()

def create_virtual_filesystem(base_path):
    generator = FileSystemGenerator(base_path)
    generator.generate_all()

if __name__ == "__main__":
    create_virtual_filesystem("/app/virtual_fs") 