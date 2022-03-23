'''
Filename: setup.py
Created Date:
Author:

Copyright (c) 2021 Henceforth
'''

from setuptools import setup, find_packages

setup(
    # what you want to call the archive/egg
    # TODO Update your project name
    name="Project Name",
    version="0.1",
    # TODO Update the names in the include list based on ur project folder name
    packages=find_packages(include=['Tiktok_Analytics', 'Tiktok_Analytics.*']),
    # custom links to a specific project
    dependency_links=[],
    install_requires=[],
    # optional features that other packages can require
    extras_require={},
    # in case we want to package more data with the application
    package_data={
        # 'Block_IPFS': ['alembic.ini', 'alembic/*', 'alembic/**/*'],
    },
    # TODO update the names of the people working on the project
    author="Person X, Person Y",
    # TODO update the emails of the people working on the project
    author_email="Email1, Email2,",
    description="Full Project Description",
    keywords="Keyword1, Keyword2, Keyword3, Keyword4",
    # TODO update the url to the project remote repository
    url="",
    entry_points={
        # command-line executable to expose
        "console_scripts": [
            "TA = Tiktok_Analytics.main:main",

        ],
        # GUI executable
        "gui_scripts": []
    }
)
