#!/usr/bin/env python
import click
import pkg_resources
import mandic_panoptes.cli.aws
import mandic_panoptes.cli.gcp


@click.group()
def main():
    """Welcome to Panoptes - The multi cloud security group analyzer

    This project is stored on GitHub and open sourced under Apache 2.0

    To start using it, read the docs at:
    https://github.com/tioxy/panoptes
    """
    pass


@main.group(
    'aws',
    help='Amazon Web Services'
)
def aws_group():
    pass


@main.group(
    'gcp',
    help='Google Cloud Plataform'
)
def gcp_group():
    pass


@main.command(
    'version',
    help='Show Panoptes version'
)
def version_command():
    print(pkg_resources.get_distribution("mandic_panoptes").version)

"""
Adding commands to Click Groups
"""
aws_group.add_command(mandic_panoptes.cli.aws.aws_analyze_command)
gcp_group.add_command(mandic_panoptes.cli.gcp.gcp_analyze_command)


if __name__ == "__main__":
    main()
    exit()
