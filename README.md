# Chinese Domain and IP Rules

Automatically generated ruleset for sing-box that combines:

1. **Chinese Domain Rules**
   - Source: [dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
   - File: `cn-domains.srs`
   - Content: Common Chinese domain names that should be resolved directly

2. **Chinese IP CIDR Rules**
   - Source: [APNIC Delegated List](https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest)
   - File: `cn-ip-cidr.srs`
   - Content: All IP ranges allocated to China

## Auto Updates

Rules are automatically updated daily at 00:20 (UTC+8) via GitHub Actions.

## Usage with sing-box

Add this to your sing-box configuration:

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "cn-domains",
        "type": "remote",
        "format": "binary",
        "url": "https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest/download/cn-domains.srs",
        "download_detour": "direct"
      },
      {
        "tag": "cn-ip-cidr",
        "type": "remote",
        "format": "binary",
        "url": "https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest/download/cn-ip-cidr.srs",
        "download_detour": "direct"
      }
    ],
    "rules": [
      {
        "rule_set": ["cn-domains", "cn-ip-cidr"],
        "outbound": "direct"
      }
    ]
  }
}
```

This configuration will:
- Automatically download the latest rules
- Route Chinese domains and IPs directly
- Update rules when sing-box restarts

## Development

If you want to generate rules locally:

1. Install the package:
   ```bash
   pip install .
   ```

2. Generate rules:
   ```bash
   # Generate both domain and IP rules
   cn-rules all

   # Or generate them separately
   cn-rules domains  # Only domain rules
   cn-rules ip      # Only IP rules
   ```

3. Use custom output paths:
   ```bash
   cn-rules domains -o custom-domains.json
   cn-rules ip -o custom-ip.json
   ```

Format doc: https://sing-box.sagernet.org/configuration/rule-set/headless-rule

## License

MIT

## Credits

- Domain list from [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
- IP data from [APNIC](https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest)


