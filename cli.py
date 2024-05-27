"""
iA.Téléservices CLI


Usecases :

-   List all Teleservices instances
-   List all Teleservices instances for a specific package
-   SSH into a Teleservices instance trough passed arguments (can be partial of
    the name), if multiple instances are found, prompt user for a choice.

Usage:

    # List all Teleservices instances
    $ python3 cli.py list

    # List all Teleservices instances with "saint" in the name
    $ python3 cli.py list --name saint

    # List all Teleservices instances with "imio_ts_aes" package
    $ python3 cli.py list --package imio_ts_aes

    # Connect to a Teleservices instance
    $ python3 cli.py ssh etalle

    # Connect to a Teleservices instance with "saint" in the name (multiple instances found, prompt user for a choice)
    $ python3 cli.py ssh saint

    # List url of all Teleservices instances (can be combined with other options)
    $ python3 cli.py list --url-only

    # List all Teleservices instances with "imio_townstreet" package and display only the URL
    $ python3 cli.py list --package imio_townstreet --url-only

    # List all Teleservices instances for host ts021
    $ python3 cli.py list --host ts021
    $ python3 cli.py list --host ts021 --url-only
"""

import os
import subprocess

import click
import requests

DEFAULT_INFRA_API_URL = "https://infra-api.imio.be/application/teleservices"
infra_api_url = os.getenv("INFRA_API_URL", DEFAULT_INFRA_API_URL)


class Config(object):
    """
    This class is used to store the configuration of the CLI.
    Think of the Config class as a backpack that your CLI carries around.
    Whenever a command (like a tool in this backpack) needs something
    (like the verbose setting), it can easily reach in and grab it.
    """

    def __init__(self):
        self.verbose = False
        self.user = os.getenv("USER")  # Hardcode your ssh user here if that doesn't work


pass_config = click.make_pass_decorator(Config, ensure=True)


# Main CLI
@click.group()
@click.option("--verbose", is_flag=True, help="Enables verbose mode.")
@pass_config
def cli(config, verbose):
    """
    Welcome to the Teleservices CLI.
    This CLI allows you to manage Teleservices instances.
    """

    config.verbose = verbose
    if verbose:
        click.echo(click.style("Verbose mode enabled.", fg="green"))


# List Teleservices instances
@cli.command()
@click.option("--name", "-n", default="", help="Filter instances by name. Part of the name is sufficient.")
@click.option("--package", "-p", default="", help="Filter instances by package.")
@click.option("--url-only", is_flag=True, help="Display only the URL of the Teleservices.")
@click.option("--host", "-h", help="Filter instances by host.")
@pass_config
def list(config, name, package, url_only, host):
    """
    List Teleservices instances. Can be filtered by name.
    """
    if config.verbose:
        click.echo(click.style("Listing all Teleservices instances", fg="green"))
    teleservices = request_teleservices(config)

    # Filter by package
    if package:
        teleservices = return_teleservices_for_package(config, teleservices, package)
        if not teleservices:
            click.echo(f"No Teleservices found for package {package}", fg="red")
            return

    # Filter by host
    if host:
        teleservices = [ts for ts in teleservices if host in ts["host"]]
        if not teleservices:
            click.echo(f"No Teleservices found for host {host}", fg="red")
            return

    # Filter by name
    for teleservice in teleservices:
        # an empty string is considered to be a substring of any string in Python
        # Therefore, all instances will be displayed if the name is empty
        if name.lower() in teleservice["application_name"].lower():
            display_teleservice(teleservice, url_only)

    if not teleservices:
        click.echo(click.style("No Teleservices found.", fg="red"))
    else:
        click.echo(
            click.style(
                f"All Teleservices listed successfully ({len(teleservices)} elements found so far!)", fg="green"
            )
        )


# SSH into a Teleservices instance
@cli.command()
@click.argument("teleservice")
@pass_config
def ssh(config, teleservice):
    """
    SSH into a Teleservices instance. Count matches if multiple instances are found and prompt user for a choice.
    """
    if config.verbose:
        click.echo(click.style(f"Searching for Teleservice {teleservice}", fg="green"))
    teleservices = request_teleservices(config)
    teleservices = [ts for ts in teleservices if teleservice in ts["application_name"]]
    if not teleservices:
        click.echo(click.style(f"Teleservice {teleservice} not found.", fg="red"))
        return
    elif len(teleservices) > 1:
        click.echo(click.style(f"Multiple Teleservices found for {teleservice}. Please choose one:", fg="yellow"))
        for i, ts in enumerate(teleservices):
            click.echo(f"{i+1}. {ts['application_name']} ({ts['environment']})")
        choice = click.prompt("Enter the number of the Teleservice you want to connect to", type=int)
        if choice < 1 or choice > len(teleservices):
            click.echo(click.style("Invalid choice.", fg="red"))
            return
        teleservice = teleservices[choice - 1]
    else:
        teleservice = teleservices[0]

    if config.verbose:
        click.echo(click.style(f"Connecting to {teleservice['host']}...", fg="green"))
    subprocess.run(["ssh", f"{config.user}@{teleservice['host']}"])
    return


def return_teleservices_for_package(config, teleservices, package):
    """Returns teleservices for a specific package"""
    if config.verbose:
        click.echo(click.style(f"Filtering teleservices for package {package}", fg="green"))
    if not teleservices:
        teleservices = request_teleservices(config)
    return [teleservice for teleservice in teleservices if package.lower() in teleservice["packages"]]


def request_teleservices(config):
    """
    Request the list of teleservices from the infra-api.
    """
    if config.verbose:
        click.echo(click.style(f"Requesting teleservices from {infra_api_url}", fg="green"))
    try:
        with requests.get(infra_api_url) as response:
            response.raise_for_status()
            if config.verbose:
                click.echo(click.style("Teleservices received successfully.", fg="green"))
            teleservices_json = response.json()
            # Order by application_name
            teleservices_json = sorted(teleservices_json, key=lambda x: x["application_name"])
            return teleservices_json
    except requests.RequestException as e:
        click.echo(f"Failed to fetch teleservices: {e}", err=True)
        return []


def display_teleservice(teleservice, url_only=False):
    """
    Display formatted information about a teleservice.

    For reference (teleservice object):
    {'application_name': 'etalle_teleservices', 'is_docker': False,
    'type': 'teleservices', 'environment': 'production', 'image_id': '',
    'images_version': '', 'vhost_name': 'https://etalle.guichet-citoyen.be',
    'total_size': '293.099876', 'instance_port_urls': None, 'minisites': {},
    'packages': ['imio_ts_aes'], 'host': 'ts003.prod.imio.be'}
    """
    if url_only:
        click.echo(teleservice["vhost_name"])
        return
    else:
        total_size = float(teleservice["total_size"])
        total_size_gb = total_size / 1024
        click.echo(
            click.style(f"{teleservice['application_name']} ({teleservice['environment']})", fg="blue", bold=True)
        )
        click.echo(
            f"Host: {teleservice['host']} · Vhost: {teleservice['vhost_name']} · Total size: {total_size_gb:.2f} GB"
        )
        click.echo(f"Packages: [{', '.join(teleservice['packages'])}]")


if __name__ == "__main__":
    cli()
