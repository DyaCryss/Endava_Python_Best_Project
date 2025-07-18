import click
import requests

API_BASE = "http://127.0.0.1:8000"

@click.group()
def cli():
    """CLI pentru apelarea serviciilor matematice"""
    pass

@cli.command()
@click.option('--number', required=True, type=int, help="Număr pentru factorial")
@click.option('--api_key', required=True, type=str, help="Cheia API")
def factorial(number, api_key):
    url = f"{API_BASE}/fact/retrieve"
    headers = {"name": api_key}
    payload = {"number": number}
    r = requests.post(url, json=payload, headers=headers)
    try:
        click.echo(r.json())
    except Exception:
        click.echo(f"[{r.status_code}] {r.text}")


@cli.command()
@click.option('--number', required=True, type=int, help="Număr pentru fibonacci")
@click.option('--api_key', required=True, type=str, help="Cheia API")
def fibo(number, api_key):
    url = f"{API_BASE}/fibo/retrieve"
    headers = {"name": api_key}
    payload = {"number": number}
    r = requests.post(url, json=payload, headers=headers)
    try:
        click.echo(r.json())
    except Exception:
        click.echo(f"[{r.status_code}] {r.text}")


@cli.command()
@click.option('--a', required=True, type=float, help="Baza")
@click.option('--b', required=True, type=float, help="Exponentul")
@click.option('--api_key', required=True, type=str, help="Cheia API")
def power(a, b, api_key):
    url = f"{API_BASE}/pow/float"
    headers = {"name": api_key}  # <-- CORECTAT AICI
    payload = {"a": a, "b": b}
    r = requests.post(url, json=payload, headers=headers)
    try:
        click.echo(r.json())
    except Exception:
        click.echo(f"[{r.status_code}] {r.text}")


if __name__ == '__main__':
    cli()
