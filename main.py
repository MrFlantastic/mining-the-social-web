import selenium as selenium

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

proxy_ip_port = ''

driver = webdriver.Chrome('/Users/MFlanagan/Desktop/chromedriver')

driver.get('https://whatismyipaddress.com')

time.sleep(8)

driver.quit()