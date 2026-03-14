import re
from collections import defaultdict

def analyze_log(file_content, threshold=100):
    """
    Parses the log file content and detects potential DDoS attacks.
    Expected log format: 127.0.0.1 - - [Date] "Method Endpoint HTTP/1.1" Status Size
    """
    # Regex to match the IP address at the start of a line
    ip_pattern = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    
    ip_counts = defaultdict(int)
    total_requests = 0
    
    lines = file_content.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = ip_pattern.search(line)
        if match:
            ip = match.group(1)
            ip_counts[ip] += 1
            total_requests += 1

    all_ips = []
    suspicious_ips = []
    for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
        status = "Normal"
        if count > threshold:
            status = "Malicious"
            suspicious_ips.append({"ip": ip, "count": count, "status": status})
        elif count > threshold * 0.5:
            # Let's say if it's over 50% of the threshold, it's Suspicious
            status = "Suspicious"
            
        all_ips.append({"ip": ip, "count": count, "status": status})
            
    # Sort all IPs for the graph (top 15 for dashboard)
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
    top_ips_chart = {
        "labels": [item[0] for item in sorted_ips[:15]],
        "data": [item[1] for item in sorted_ips[:15]]
    }

    return {
        "total_requests": total_requests,
        "unique_ips": len(ip_counts),
        "suspicious_ips": suspicious_ips,
        "all_ips": all_ips,
        "is_under_attack": len(suspicious_ips) > 0,
        "chart_data": top_ips_chart
    }
