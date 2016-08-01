__author__ = 'nicholas'

import sys
import pickle
import signal
from bs4 import BeautifulSoup
import urllib2,cookielib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
output_dir='pizza_data/papa_johns/'
hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
#page=urllib2.Request(url, headers=hdr)
#keywords=['Personal$','Medium$','Large$']
#keywords=['Small (10")$','Medium (12")$','Large (14")$','X-Large (16")$']
keywords=['Medium$','Large$','Extra Large$']
def sigint(signal, frame):
    sys.exit(0)

class Scraper(object):
    def __init__(self):
        self.url = 'http://www.fastfoodmenuprices.com/papa-johns-prices/'
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1120, 550)

    #--- STATE -----------------------------------------------------
    def get_state_select(self):
        path = '//select[@id="variation-tablepress-31"]'
        state_select_elem = self.driver.find_element_by_xpath(path)
        state_select = Select(state_select_elem)
        return state_select

    def select_state_option(self, value, dowait=True):
        '''
        Select state value from dropdown. Wait until district dropdown
        has loaded before returning.
        '''
        #path = '//select[@id="variation-tablepress-32"]'
        path = '//select[@id="variation-tablepress-31"]'
        district_select_elem = self.driver.find_element_by_xpath(path)

        def district_select_updated(driver):
            try:
                district_select_elem.text
            except StaleElementReferenceException:
                return True
            except:
                pass

            return False

        state_select = self.get_state_select()
        state_select.select_by_value(value)

        return self.get_state_select()





    def load_page(self):
        self.driver.get(self.url)

        def page_loaded(driver):
            path = '//select[@id="variation-tablepress-31"]'
            return driver.find_element_by_xpath(path)

        wait = WebDriverWait(self.driver, 10)
        wait.until(page_loaded)

    def scrape(self):
        def states():
            state_select = self.get_state_select()
            state_select_option_values = [
                '%s' % o.get_attribute('value')
                for o
                in state_select.options[1:]
            ]

            for v in state_select_option_values:
                state_select = self.select_state_option(v)
                self.driver.page_source
                text=BeautifulSoup(self.driver.page_source, "html.parser").get_text()
                meta_prices=[]
                for keyword in keywords:
                    prices = []
                    counter=text.count(keyword)
                    for z in range(counter):
                        prices.append(text.rsplit(keyword, z+1)[1].splitlines()[0])
                    prices=[float(price) for price in prices]
                    meta_prices.append(prices)
                yield (state_select.first_selected_option.text,meta_prices)



        self.load_page()

        for j,state in enumerate(states()):
            w = open(output_dir+str(j)+'.pk1', "wb")
            pickle.dump(state, w)
            w.close()
            print(state)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint)
    scraper = Scraper()
    scraper.scrape()