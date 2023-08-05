import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="discoset",
    version="0.9.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "discoset=discoset.__main__:_main",
        ]
    },
    install_requires=["PyYAML"],

    # Metadata
    author="Christoph Echtinger-Sieghart",
    author_email="s@hands-on-imperative.org",
    description="Small script to setup symlinks to dotfiles",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["dotfiles", "symlink", "configs"],
    url="https://github.com/chsigi/discoset",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
