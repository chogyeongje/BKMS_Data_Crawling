from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

def install_driver():
    
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # open browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('debuggerAddreess', "127.0.0.1:9222")
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')

    # driveManager =  ChromeDriverManager().install()
    driveManager = './chromedriver'
    print(driveManager)

    return driveManager, options