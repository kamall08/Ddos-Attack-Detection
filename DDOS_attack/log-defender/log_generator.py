import random
import time
from datetime import datetime, timedelta
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "server.log")

def generate_log():
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Normal IPs
    normal_ips = [f"192.168.1.{i}" for i in range(10, 50)]
    
    # Attacker IP
    attacker_ip = "10.0.0.99"
    
    endpoints = ["/index.html", "/login", "/api/data", "/images/logo.png", "/about", "/contact"]
    methods = ["GET", "POST"]
    status_codes = [200, 200, 200, 200, 404, 500, 302]
    
    start_time = datetime.now() - timedelta(hours=1)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        # Generate some normal background traffic
        for _ in range(300):
            ip = random.choice(normal_ips)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice(status_codes)
            size = random.randint(500, 5000)
            
            # Formatting realistic log
            date_str = start_time.strftime("%d/%b/%Y:%H:%M:%S +0530")
            log_entry = f'{ip} - - [{date_str}] "{method} {endpoint} HTTP/1.1" {status} {size} "-" "Mozilla/5.0"\n'
            f.write(log_entry)
            
            start_time += timedelta(seconds=random.randint(1, 15))
            
        # Simulate DDoS attack from the attacker IP (burst of requests)
        print("Injecting DDoS traffic from IP:", attacker_ip)
        for _ in range(450): # Threshold will be 100, this easily triggers it
            method = "GET"
            endpoint = "/"
            status = 200
            size = random.randint(500, 1000)
            
            date_str = start_time.strftime("%d/%b/%Y:%H:%M:%S +0530")
            log_entry = f'{attacker_ip} - - [{date_str}] "{method} {endpoint} HTTP/1.1" {status} {size} "-" "Mozilla/5.0 (Attacker/Bot)"\n'
            f.write(log_entry)
            
            # Small time gap between attack requests
            start_time += timedelta(milliseconds=random.randint(10, 100))
            
        # Add a few more normal requests post-attack
        for _ in range(150):
            ip = random.choice(normal_ips)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice(status_codes)
            size = random.randint(500, 5000)
            
            date_str = start_time.strftime("%d/%b/%Y:%H:%M:%S +0530")
            log_entry = f'{ip} - - [{date_str}] "{method} {endpoint} HTTP/1.1" {status} {size} "-" "Mozilla/5.0"\n'
            f.write(log_entry)
            
            start_time += timedelta(seconds=random.randint(1, 10))

    print(f"Generated simulated log file at {LOG_FILE}")

if __name__ == "__main__":
    generate_log()
