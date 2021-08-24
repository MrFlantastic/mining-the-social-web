from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

### find elite proxy ip and port from https://free-proxy-list.net/
proxy_ip_import = '54.37.18.143:8080'

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_import
proxy.ssl_proxy = proxy_ip_import

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

driver = webdriver.Chrome('/users/mflanagan/desktop/chromedriver', desired_capabilities=capabilities)

driver.get('http://whatismyipaddress.com')

time.sleep(8)

driver.quit()
