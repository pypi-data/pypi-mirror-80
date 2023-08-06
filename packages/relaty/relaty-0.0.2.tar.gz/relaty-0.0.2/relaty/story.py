import typing


class Story():
    title: str
    screens: typing.List[str]
    options: typing.Union[typing.List['Story'], None]

    def __init__(
            self,
            title: str,
            screens: typing.List[str] = [],
            options: typing.Union[typing.List[typing.Dict], None] = None,
    ):

        self.title = title
        self.screens = screens

        if options is not None:
            self.options = [Story(**option) for option in options]
        else:
            self.options = options

    @property
    def get_number_endings(self):
        """Get the number of endings of the Story
        """
        if self.options is None:
            return 1
        else:
            return sum([option.get_number_endings for option in self.options])

    def display_options(self):
        if self.options is None:
            return

        for number, option in enumerate(self.options):
            print(f'{number+1} - {option.title}')

        try:
            option_number = int(input("Input option number: "))

            if option_number < 1 or option_number > len(self.options):
                raise ValueError

            return option_number
        except ValueError:
            print("The input wasn't valid, try again")
            self.display_options()

    def add_screen(self, screen: str):
        self.screens.append(screen)

    def add_option(self, option: 'Story'):
        if self.options is None:
            self.options = []
        self.options.append(option)

    def get_option(self, number):
        if self.options is None:
            return None
        return self.options[number]

    def shallow_equal(self, story: 'Story'):
        return \
            self.title == story.title and all(
                [a == b
                 for a, b in zip(self.screens, story.screens)])

    def __eq__(self, other):
        # If it's not a Story
        if not isinstance(other, Story):
            return False

        # If it's not shallow equal
        if not self.shallow_equal(other):
            return False

        if self.options is None or other.options is None:
            return False

        if len(self.options) != len(other.options):
            return False

        return self.options == other.options

    def navigate(self, path: typing.List[int]):
        result = self

        for option in path:
            result = result.get_option(option)

        return result

    def play(self):
        # Print title
        print(self.title)

        # Print each screen
        for s in self.screens:
            print(s)
            input("Print any key to continue...")

        option_number = self.display_options()

        if option_number is None:
            return

        self.options[option_number-1].play()
