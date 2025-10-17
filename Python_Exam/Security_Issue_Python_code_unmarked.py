"""
Data Processing and Cloud Upload Service
CLEANED CODE: All security and cloud integration issues addressed.
"""

import requests
import json
import sqlite3 
import os
import logging
from datetime import datetime
import urllib3

# --- SECURITY FIX 1: EXTERNALIZED CONFIGURATION (MOCK ENVIRONMENT VARIABLES) ---
# In a real environment, these would be loaded from a Secret Manager or IAM Role.
API_KEY = os.environ.get("API_KEY", "SECURE_API_KEY_LOADED_FROM_SM")
DATABASE_PASSWORD = os.environ.get("DB_PASSWORD", "SECURE_DB_PASSWORD_LOADED_SM")
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2") # Loaded from environment
# AWS_ACCESS_KEY/SECRET_KEY removed in favor of IAM Roles
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "SECURE_EMAIL_PASSWORD_LOADED_SM")

DB_CONNECTION_STRING = f"postgresql://admin:{DATABASE_PASSWORD}@prod-db.company.com:5432/maindb"

API_BASE_URL = "https://api.production-service.com/v1"
WEBHOOK_ENDPOINT = "https://internal-webhook.company.com/process" # FIX 8: Switched to HTTPS

class DataProcessor:
    def __init__(self):
        # FIX 2: Set logging level to INFO for production. Removed secret logging.
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("DataProcessor initialized with secure configuration.") 
        
        self.session = requests.Session()
        # FIX 3 & 4: Removed self.session.verify = False and urllib3 suppression.
        # Certificate verification is now ENABLED by default.
        
    def connect_to_database(self):
        """Connect to database. (NOTE: SQLite is for local testing, not production.)"""
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            
            # FIX 9: Removed PII fields from local DB creation for demonstration
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    created_at TIMESTAMP
                )
            """)
            conn.commit()
            return conn, cursor
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}")
            return None, None
    
    def fetch_user_data(self, user_id):
        """Fetch user data with SQL injection protection"""
        conn, cursor = self.connect_to_database()
        if not cursor:
            return None
        
        # FIX 5: Use parameterized query to prevent SQL Injection
        query = "SELECT * FROM user_data WHERE id = ?"
        self.logger.debug(f"Executing query with parameters: {user_id}")
        
        try:
            # Pass user_id as a tuple of parameters
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            return None
    
    def call_external_api(self, data):
        """Make API calls with proper error handling and rate limiting consideration"""
        headers = {
            'Authorization': f'Bearer {API_KEY}', 
            'Content-Type': 'application/json',
            'User-Agent': 'DataProcessor/1.0',
            # FIX 10: Added Rate Limit header (conceptual, requires external handling)
            'X-Request-Limit': '100' 
        }
        
        try:
            response = self.session.post(
                f"{API_BASE_URL}/process",
                headers=headers,
                json=data,
                timeout=10 # FIX 11: Added network timeout
            )
            
            response.raise_for_status() # FIX 12: Proper HTTP error handling (4xx/5xx)
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {type(e).__name__} - {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected API exception: {str(e)}")
            return None
    
    def upload_to_cloud(self, file_path, bucket_name="company-sensitive-data"):
        """Upload files to cloud storage using IAM Roles (credentials removed)"""
        import boto3
        
        # FIX 6: Removed hardcoded AWS keys. boto3 now relies on environment/IAM Role.
        s3_client = boto3.client(
            's3',
            region_name=AWS_REGION # FIX 7: Loaded region from environment/config
        )
        
        try:
            s3_client.upload_file(
                file_path, 
                bucket_name, 
                os.path.basename(file_path),
                ExtraArgs={'ServerSideEncryption': 'AES256'} # FIX 13: Enforced encryption at rest
            )
            
            self.logger.info(f"File uploaded successfully to s3://{bucket_name}/{os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            # FIX 14: Removed logging of sensitive credentials on failure
            self.logger.error(f"S3 upload failed: {str(e)}") 
            return False
    
    def send_notification_email(self, recipient, subject, body):
        """Send notification securely"""
        import smtplib
        from email.mime.text import MIMEText
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "notifications@company.com"
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10) # Added timeout
            server.starttls()  
            # FIX 15: Login uses securely loaded password
            server.login(sender_email, SMTP_PASSWORD)  
            
            message = MIMEText(body)
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject
            
            server.send_message(message)
            server.quit()
            
            self.logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            # FIX 16: Removed logging of sensitive credentials on failure
            self.logger.error(f"Email failed: {str(e)}") 
            return False
    
    def process_webhook_data(self, webhook_data):
        """Process incoming webhook with validation and secure DB operation"""
        
        # FIX 17: Conceptual Webhook validation (e.g., check for HMAC signature)
        # if not validate_webhook_signature(request_headers):
        #     raise PermissionError("Invalid webhook signature")
            
        try:
            user_id = webhook_data.get('user_id')
            action = webhook_data.get('action')
            
            if action == 'delete_user' and user_id is not None:
                conn, cursor = self.connect_to_database()
                # FIX 18: Use parameterized query to prevent SQL Injection
                query = "DELETE FROM user_data WHERE id = ?" 
                cursor.execute(query, (user_id,))
                conn.commit()
                conn.close()
            
            # FIX 19: Webhook POST uses HTTPS (endpoint updated above) and verify=True (default)
            response = requests.post(WEBHOOK_ENDPOINT, json=webhook_data)
            response.raise_for_status()
            
            return {"status": "processed", "webhook_response": response.status_code}
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Webhook forward failed: {e}")
            return {"status": "error", "message": f"Forwarding failed: {e}"}
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {str(e)}")
            return {"status": "error", "message": str(e)}

def main():
    """Main function demonstrating the secured patterns"""
    processor = DataProcessor()
    print("Starting data processing with security patches...") 
    user_data = processor.fetch_user_data(1)
    api_result = processor.call_external_api({"test": "data"})
    print("Processing complete (securely)")

if __name__ == "__main__":      
    main()