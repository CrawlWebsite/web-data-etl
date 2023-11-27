import sys
import os
# Add the parent directory of the handler module to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import click
from handler.crawWebsite import crawlWebsiteHandler

@click.command()
@click.option('--url', help='The website URL to crawl')
@click.option('--pageStart', help='The page that will be started')
@click.option('--pageEnd', help='The page that will be ended')
def crawlWebsite(url, pageStart, pageEnd):
    crawlWebsiteHandler(url, pageStart, pageEnd)

if __name__ == '__main__':
    crawlWebsite()