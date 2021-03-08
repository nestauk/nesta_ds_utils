"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Nesta Data Science Utilities."""


if __name__ == "__main__":
    main(prog_name="ds-utils")  # pragma: no cover
