import io
import logging
import os
from os.path import dirname, abspath
from typing import List
from setuptools import Command, find_packages, setup

logger = logging.getLogger(__name__)

root_dir = dirname(abspath(__file__))

try:
    with io.open(os.path.join(root_dir, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


class CleanCommand(Command):
    """
    Command to tidy up the project root.
    Registered as cmdclass in setup() so it can be called with
    ``python setup.py extra_clean``.
    """

    description = "Tidy up the project root"
    user_options: List[str] = []

    def initialize_options(self):
        """Set default values for options."""

    def finalize_options(self):
        """Set final values for options."""

    def run(self):
        """Run command to remove temporary files and directories."""
        os.chdir(root_dir)
        os.system("rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info")


setup(
    name="paperplane",
    author="Abhilash Kishore",
    author_email="abhilash1in@gmail.com",
    description="A simple interactive CLI builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhilash1in/paperplane",
    license="MIT",
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    # colorama enables ANSI colors support on Windows
    # See https://click.palletsprojects.com/utils/
    install_requires=["pyyaml", "click", "colorama"],
    extras_require={
        "docs": ["sphinx", "sphinx_rtd_theme", "recommonmark"],
    },
    entry_points={
        "console_scripts": [
            "paperplane=paperplane:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={"extra_clean": CleanCommand},
    python_requires=">=3.6",
)
