# Shibboleth Get

*Get the content of pages shielded by Shibboleth*

Many organizations (universities, especially) use [Shibboleth](https://www.shibboleth.net/) as a single-sign-on solution to protect secured webpages. This command line tool returns the page content of a URL that is protected by Shibboleth. It currently does this by using [Selenium](https://www.selenium.dev/documentation/en/webdriver/) to provide authentication details to the page.

## Usage

```
shibboleth-get [-h] [-d DELAY] [-s SCREENSHOT] [-q] username password url

Get the content of pages shielded by Shibboleth

positional arguments:
  username              Username to use
  password              Corresponding password to use
  url                   Protected URL to get

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        Seconds to wait for page to load. Default: 2.0
  -s SCREENSHOT, --screenshot SCREENSHOT
                        Take a screenshot to the given .png file
  -q, --quiet           Hide status output
```

Example:

```
nano password.txt
shibboleth-get ajohnson7 "$(cat password.txt)" https://illinoisedu.instructure.com/courses/342/pages/some-page
```

## Installation

This package requires `python3` and the downloaded [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home) executable in your PATH. Make sure the version number corresponds to the version of Chrome you have installed.

Install via PyPI:

```
pip3 install --user shibboleth-get
```
