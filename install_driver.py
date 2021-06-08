from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def install_driver():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # open browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driveManager = './chromedriver' # ChromeDriverManager().install()
    print(driveManager)

    return driveManager, options