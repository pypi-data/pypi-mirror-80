#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()

def main():

    setuptools.setup(
        setup_requires   = ['wheel'],
        name             = "kvector2",
        version          = "1.4.1",
        description      = "implement 2D vectors",
        long_description = (read("README.md")),
        url              = "https://github.com/k39dev/vector2",
        author           = "K 39",
        license          = "mit",
        py_modules       = ["vector2"],
        entry_points     = """
            [console_scripts]
            vector2 = vector2:vector2
        """,
        python_requires  = ">=3.6",
    )

if __name__ == "__main__":
    main()
