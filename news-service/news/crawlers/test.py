#!/usr/bin/python
# filename: run.py
import re
from coreCrawler import CoreCawler

if __name__ == "__main__": 
    # Using SQLite as a cache to avoid pulling twice
    crawler = CoreCawler()
    crawler.fetch('http://www.anp.ne/')