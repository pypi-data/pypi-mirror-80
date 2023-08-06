import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lex_game",
    version="0.0.3",
    author="Mattia Monga",
    author_email="mattia.monga@unimi.it",
    description="LEX is Martin Gardner's Hexapawn where matchboxes are Excel files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mmonga/lex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games"
    ],
    python_requires='>=3.6',
    install_requires=['openpyxl'],
    entry_points={
        'console_scripts': ['lex_game = lexcel.game:main']
    }
)
