# PY_4

This is a website statistics/benchmarking tool which helps to crawl data from websites and generate reports in YAML, HTML, JSON, CSV format. It helps to inmplement a command line utility which gathers statistics of a website.

This utility will also gather a list of broken links, a list of links leading to external websites, and loading time for each web page on the website. The command-line utility will crawl the entire website to collect the statistics and also store them into a local database. It will also provide an option to generate a report on a terminal standard output or an HTML file for the statistics collected.

This utility includes the following modules:
1. Website Crawler : crawler.py
2. Statistics Data Model : storage.py
3. Report Generator : representation.py
4. Command Line Parser : command_parser.py

# Website Crawler 
It crawls each page in websites concurrently and handles all the errors and exceptions.

# Statistics Data Model
It stores the crawling statistics into an organised format in the database. It provides an abstraction for storing statistics and extracting them for reports.

# Report Generator
It helps to generate reports on standard output or to a file. Formats accessible are YAML(default), HTML. It also has a provision to add new report generator components to generate report in JSON formats, CSV formats, etc. as a plugin without affecting other components of the application.

# Command Line Parser
It is responsible for parsing command line arguments and generating web response data formats and utility helpers.


It can run as an application, by running the command './website-stats.py' with command-line arguments in windows / mac terminal.
It is also be possible to load it as a module within python program using the package website_stats.

# Requirements:

pip install pyyaml
To generate yaml report

# Package
This final build can be used as a standalone installable package or as a developer library that can be loaded as a module and extended in another python application. 

You just need to run this command on terminal:
pip install pycrawler

You can use this library in your module using the below line:
from PY_4 import website_stats

Include this in your main:
if __name__ == '__main__':
     website_stats.run()
