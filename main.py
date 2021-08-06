from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy,ProxyType

import time

co=webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")


def get_proxies(co=co):
    driver=webdriver.Chrome()
    driver.get("https://free-proxy-list.net/")

    PROXIES=[]
    proxies=driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result=p.text.split(" ")

        if result[-1]=="yes":
            PROXIES.append(result[0] + ":" + result[1])

    driver.close()
    return PROXIES


ALL_PROXIES=get_proxies()


def proxy_driver(PROXIES,co=co):
    prox=Proxy()

    if len(PROXIES) < 1:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES=get_proxies()

    pxy=PROXIES[-1]

    prox.proxy_type=ProxyType.MANUAL
    prox.http_proxy=pxy
    prox.socks_proxy=pxy
    prox.ssl_proxy=pxy

    capabilities=webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver=webdriver.Chrome(chrome_options=co,desired_capabilities=capabilities)

    return driver


# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy
pd=proxy_driver(ALL_PROXIES)

# code must be in a while loop with a try to keep trying with different proxies
running=True

while running:
    try:
        mycodehere()

        # if statement to terminate loop if code working properly
        # you need to modify condition_met
        if condition_met:
            running=False

        # you
    except:
        new=ALL_PROXIES.pop()

        # reassign driver if fail to switch proxy
        pd=proxy_driver(ALL_PROXIES)
        print("--- Switched proxy to: %s" % new)
        time.sleep(1)