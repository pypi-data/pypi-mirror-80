from .story import Story

from typing import List


class Relat():
    """ Represents the start of an interactive story.

    Relat comes from the catalan word for _tale_

    Attributes:
        story (Story): a story, the entry point of the narrative
    """
    story: Story

    def __init__(self, title, *args, **kwargs):
        self.story = Story(title)

    @classmethod
    def create_from_document(cls, document):
        """Create a Relat from a document

        Arguments:
            document (dict): dict used for creating the document

        Returns:
            a Relat instance

        """
        story = Story(**document)

        instance = cls(story.title)
        instance.story = story

        return instance

    @property
    def get_number_endings(self):
        """Obtain the number of endings of the story

        Since any story in Relaty is represented in the shape
        of a tree, and ending is just a leaf.

        Returns:
            number of endings in the story
        """
        return self.story.get_number_endings

    @property
    def title(self):
        """Obtain the title of the Relat"""
        return self.story.title

    @property
    def screens(self):
        """Access the initial screens of the Relat"""
        return self.story.screens

    @property
    def options(self):
        """Access the root-level options of the Relat"""
        return self.story.options

    def add_screen(self, screen: str):
        """Adds a screen at the end of the initial screens"""
        self.story.add_screen(screen)

    def add_option(self, option: Story):
        """Adds and option to the root-level options of the Relat"""
        self.story.add_option(option)

    def navigate(self, path):
        """Returns the story at the path"""

        return self.story.navigate(path)

    def play(self):
        """Play the story in cli mode

        When this method is invoked, the story can be played in the terminal.
        It shows every screen and ask for confirmation to continue.

        Then displays each options and asks the user to choose one

        """
        self.story.play()
