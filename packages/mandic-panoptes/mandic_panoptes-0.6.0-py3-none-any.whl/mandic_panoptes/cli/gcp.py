""" Panoptes - CLI - GCP
Responsible for organizing commands from mandic_panoptes GCP CLI
"""

import click
import mandic_panoptes as panoptes


GCP_AVAILABLE_OUTPUT_OPTIONS = [
    'human',
    'json',
    'yml',
]


@click.command(
    'analyze',
    help="Generate the analysis output"
)
def gcp_analyze_command():
    print("Nothing here")
    return None


if __name__ == "__main__":
    pass
