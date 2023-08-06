import click
from .relat import Relat
import yaml


@click.group()
def relaty():
    pass


@click.command(help="Play a story")
@click.argument("story_path")
def play(story_path):
    document=yaml.safe_load(open(story_path))
    relat = Relat.create_from_document(document=document)

    relat.play()


relaty.add_command(play)

if __name__ == "__main__":
    relaty()
