import argparse
import json
import ipaddress
from pathlib import Path
from typing import List, Dict, Any
import requests

def fetch_dns_rules(url: str) -> List[Dict[str, Any]]:
    """Fetch and parse DNS rules from github repo URL."""
    # Convert raw github URL if needed
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com")
        url = url.replace("/blob/", "/")
    
    response = requests.get(url)
    response.raise_for_status()
    
    rules = []
    for line in response.text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse server=/domain/ip format
        if line.startswith('server='):
            parts = line.split('/')
            if len(parts) == 3:
                domain = parts[1].lstrip('.')
                ip = parts[2]
                rule = {
                    "domain": [domain],
                    "ip_cidr": [f"{ip}/32"],
                    "query_type": ["A"],
                    "invert": False
                }
                rules.append(rule)
    
    return rules

def fetch_apnic_data(url: str) -> List[Dict[str, Any]]:
    """Fetch and parse APNIC delegation data."""
    response = requests.get(url)
    response.raise_for_status()
    
    rules = []
    for line in response.text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split('|')
        if len(parts) >= 7 and parts[0] == 'apnic' and parts[1] == 'CN' and parts[2] == 'ipv4':
            ip = parts[3]
            mask = parts[4]
            try:
                # Convert mask to CIDR notation
                network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                rule = {
                    "ip_cidr": [str(network)],
                    "invert": False
                }
                rules.append(rule)
            except ValueError:
                continue
    
    return rules

def merge_rules(dns_rules: List[Dict[str, Any]], 
                apnic_rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge DNS and APNIC rules into final format."""
    return {
        "version": 3,
        "rules": dns_rules + apnic_rules
    }

def main():
    dns_url = 'https://github.com/felixonmars/dnsmasq-china-list/blob/master/accelerated-domains.china.conf'
    apnic_url = 'https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    output_file = Path('cn-dns-and-ip-list.json')
    
    try:
        # Fetch and parse input data
        dns_rules = fetch_dns_rules(dns_url)
        apnic_rules = fetch_apnic_data(apnic_url)
        
        # Merge rules
        final_rules = merge_rules(dns_rules, apnic_rules)
        
        # Write output
        with open(output_file, 'w') as f:
            json.dump(final_rules, f, indent=2)
            
        print(f"Successfully wrote rules to {output_file}")
        print(f"Processed {len(dns_rules)} DNS rules and {len(apnic_rules)} APNIC rules")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit(1)
    except Exception as e:
        print(f"Error processing data: {e}")
        exit(1)

if __name__ == "__main__":
    main() 