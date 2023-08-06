from distutils.core import setup
setup(
    name='relaty',         # How you named your package folder (MyLib)
    packages=['relaty'],   # Chose the same as "name"
    version='0.0.2',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Small package to build Choose Your Own Adventure-like stories',
    author='Pablo Toledo Margalef',                   # Type in your name
    author_email='pabloatm980@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/papablo/relaty',
    # I explain this later on
    download_url='https://github.com/PaPablo/relaty/archive/v0.0.2.tar.gz',
    # Keywords that define your package best
    keywords=['fiction', 'interactive', 'writing'],
    install_requires=[            # I get to this in a second
        'click',
        'PyYAML',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
    ],
)
