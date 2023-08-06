import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettyparse import Usage

usage = Usage('''
    Get the content of pages shielded by Shibboleth

    :username str
        Illinois netid to use
    :password str
        Corresponding password for netid
    :url str
        Protected URL to get
    :-d --delay float 2.0
        Seconds to wait for page to load
    :-s --screenshot str -
    	Take a screenshot to the given .png file
    :-q --quiet
        Hide status output
''')


def shibboleth_get(username, password, url, driver=None, debug=True):
    """Returns a selenium webdriver with the authenticated page"""
    if driver is None:
        if debug:
            print('Launching headless Chrome...', file=sys.stderr)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=640x480")
        driver = webdriver.Chrome(options=chrome_options)
    try:
        if debug:
            print('Fetching page...', url, file=sys.stderr)
        driver.get(url)
        try:
            wait = WebDriverWait(driver, 2)
            wait.until(EC.title_contains("Login"))
        except Exception:
            return driver  # Already logged in
        username_field = driver.find_element_by_id('j_username')
        username_field.send_keys(username)
        password_field = driver.find_element_by_id('j_password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        if debug:
            print('Logging in...', file=sys.stderr)
        wait = WebDriverWait(driver, 2)
        wait.until_not(EC.title_contains("Login"))
        return driver
    except Exception:
        print('Saving screenshot to problem.png...', file=sys.stderr)
        driver.get_screenshot_as_file("problem.png")
        driver.quit()
        raise


def main():
    args = usage.parse()
    driver = shibboleth_get(args.username, args.password, args.url)
    if not args.quiet:
        print('Waiting {:.2f} seconds for page to load...'.format(
            args.delay
        ), file=sys.stderr)
    try:
        sleep(args.delay)
        if args.screenshot:
            driver.get_screenshot_as_file(args.screenshot)
        print(driver.page_source)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
