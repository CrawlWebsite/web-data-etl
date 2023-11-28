import sys
import os
# Add the parent directory of the handler module to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import click
from handler.crawWebsite import crawlWebsiteHandler

@click.command()
@click.option('--url', help='The website URL to crawl')
@click.option('--page_start', help='The page that will be started', default=None)
@click.option('--page_end', help='The page that will be ended', default=None)
def crawlWebsite(url, page_start, page_end):
    crawlWebsiteHandler(url, page_start, page_end)

if __name__ == '__main__':
    crawlWebsite()