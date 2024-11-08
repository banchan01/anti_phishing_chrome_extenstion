# utilities.py

from datetime import datetime
import requests
import ssl
import socket
from urllib.parse import urlparse

def get_domain_age(url):
    """
    Estimate the age of the domain in days.
    
    Args:
        url (str): The URL to check the domain age.
    
    Returns:
        int: Estimated age of the domain in days.
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # Assume we have a way to retrieve domain creation date (e.g., via a WHOIS API)
        # Here, we'll simulate with a fixed date (replace this with actual WHOIS API logic)
        creation_date = datetime(2020, 1, 1)  # Placeholder; replace with real data
        age_in_days = (datetime.now() - creation_date).days
        return age_in_days
    except Exception as e:
        print(f"Error calculating domain age for {url}: {e}")
        return -1  # Default to -1 on error

def check_ssl_certificate(url):
    """
    Check if the URL has a valid SSL certificate.
    
    Args:
        url (str): The URL to check SSL certificate validity.
    
    Returns:
        int: 1 if SSL certificate is valid, 0 otherwise.
    """
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssl_info = ssock.getpeercert()
                if ssl_info:
                    return 1
        return 0
    except Exception as e:
        print(f"Error checking SSL certificate for {url}: {e}")
        return 0  # Default to 0 if no certificate or error
