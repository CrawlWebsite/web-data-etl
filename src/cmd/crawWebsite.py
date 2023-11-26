import sys
import os
# Add the parent directory of the handler module to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import click
from handler.crawWebsite import crawlWebsiteHandler

@click.command()
@click.option('--name', help='The person to greet.')
def crawlWebsite(name):
    print(name)
    crawlWebsiteHandler()

if __name__ == '__main__':
    crawlWebsite()