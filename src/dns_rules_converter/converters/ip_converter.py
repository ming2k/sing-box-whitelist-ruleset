import json
import ipaddress
from pathlib import Path
from typing import Dict, Any
from ..utils.network import fetch_url

def fetch_apnic_data(url: str) -> Dict[str, Any]:
    """Fetch and parse APNIC delegation data."""
    content = fetch_url(url)
    
    rules = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split('|')
        # APNIC format: apnic|CN|ipv4|1.2.3.0|1024|20100222|allocated
        if len(parts) >= 5 and parts[0] == 'apnic' and parts[1] == 'CN' and parts[2] == 'ipv4':
            ip = parts[3]
            count = int(parts[4])
            mask = 32 - count.bit_length() + 1
            
            try:
                network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                rule = {
                    "ip_cidr": [str(network)]
                }
                rules.append(rule)
            except ValueError as e:
                print(f"Warning: Invalid network {ip}/{mask}: {e}")
                continue
    
    return {
        "version": 3,
        "rules": rules
    }

def convert_ip_rules(output_file: Path = Path('cn-ip-cidr.json')) -> None:
    """Convert IP rules and save to file."""
    apnic_url = 'https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    
    ip_rules = fetch_apnic_data(apnic_url)
    
    with open(output_file, 'w') as f:
        json.dump(ip_rules, f, indent=2)
        
    print(f"Successfully wrote rules to {output_file}")
    print(f"Processed {len(ip_rules['rules'])} IP CIDR rules") 