import json
from pathlib import Path
from typing import Dict, Any
from ..utils.network import fetch_url

def fetch_dns_rules(url: str) -> Dict[str, Any]:
    """Fetch and parse DNS rules from github repo URL."""
    content = fetch_url(url)
    
    rules = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse server=/domain/ip format
        if line.startswith('server='):
            parts = line.split('/')
            if len(parts) >= 2:
                domain = parts[1].lstrip('.')
                rule = {
                    # "domain": [domain]
                    "domain_suffix": [domain]
                }
                rules.append(rule)
    
    return {
        "version": 3,
        "rules": rules
    }

def convert_dns_rules(output_file: Path = Path('cn-domains.json')) -> None:
    """Convert DNS rules and save to file."""
    dns_url = 'https://github.com/felixonmars/dnsmasq-china-list/blob/master/accelerated-domains.china.conf'
    
    dns_rules = fetch_dns_rules(dns_url)
    
    with open(output_file, 'w') as f:
        json.dump(dns_rules, f, indent=2)
        
    print(f"Successfully wrote rules to {output_file}")
    print(f"Processed {len(dns_rules['rules'])} DNS rules") 