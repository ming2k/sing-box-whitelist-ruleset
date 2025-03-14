import click
from pathlib import Path
from .converters.dns_converter import convert_dns_rules
from .converters.ip_converter import convert_ip_rules

@click.group()
def cli():
    """Convert Chinese DNS and IP rules to sing-box format."""
    pass

@cli.command()
@click.option('--output', '-o', type=Path, default='cn-domains.json',
              help='Output file path (default: cn-domains.json)')
def domains(output):
    """Convert DNS rules to JSON format."""
    try:
        convert_dns_rules(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        exit(1)

@cli.command()
@click.option('--output', '-o', type=Path, default='cn-ip-cidr.json',
              help='Output file path (default: cn-ip-cidr.json)')
def ip(output):
    """Convert IP CIDR rules to JSON format."""
    try:
        convert_ip_rules(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        exit(1)

@cli.command()
def all():
    """Convert both DNS and IP rules."""
    try:
        convert_dns_rules()
        convert_ip_rules()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        exit(1) 