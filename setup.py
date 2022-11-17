# Automatically created by: scrapyd-deploy

from setuptools import find_packages, setup

setup(
    name="quotesbot",
    version="1.0",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = quotesbot.settings"]},
    package_data={"quotesbot": ["config.ini"]},
    install_requires=["pika"],
)
