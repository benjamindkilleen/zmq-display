import click
import logging
from rich.logging import RichHandler

from .display import ImageDisplay
import click
from .display import ImageDisplay

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.NOTSET, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log.setLevel(logging.DEBUG)


@click.command()
@click.argument("host")
@click.option(
    "--port", type=int, default=7896, help="Port number to connect to. Default: 7896."
)
def main(host: str, port: int):
    display = ImageDisplay(host, port)
    display.run()


if __name__ == "__main__":
    main()
