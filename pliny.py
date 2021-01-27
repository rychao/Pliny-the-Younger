from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import string
import time
import datetime
import sys

# HEADLESS VERSION: replace lines 18 & 19
# global driver
# chromeOptions = Options()
# chromeOptions.headless = True #headless runs Chrome WITHOUT UI
# driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chromeOptions)

class Scraper(object):
    global driver
    driver = webdriver.Chrome()

    def __init__(self, url, email, firstName, lastName, address, city, zip, phone, cardNum, cardName, cardExp, ccv):
        self.url = url
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.city = city
        self.zip = zip
        self.phone = phone
        self.cardNum = cardNum
        self.cardName = cardName
        self.cardExp = cardExp
        self.ccv = ccv

    def scrape_init(self):
        url = self.url
        driver.get(url)

        email = self.email
        firstName = self.firstName
        lastName = self.lastName
        address = self.address
        city = self.city
        zip = self.zip
        phone = self.phone
        cardNum = self.cardNum.split()
        cardName = self.cardName
        cardExp = self.cardExp.split()
        ccv = self.ccv

        #age verification
        # driver.find_element_by_id('va-yes').click()

        driver.find_element_by_xpath('//*[@id="AddToCart-product-template"]').send_keys(Keys.RETURN)
        product = driver.find_element_by_class_name('product-single__title').text
        print("{} | Added \'{}\' to cart".format(str(datetime.datetime.now()).split('.')[0], product))
        time.sleep(1)
        driver.get("https://www.shop.russianriverbrewing.com/cart")
        driver.find_element_by_xpath('//*[@id="shopify-section-cart-template"]/div/div/form/div/div[2]/button[2]').click()
        print("{} | Succcesfully retrieved contact information page.".format(str(datetime.datetime.now()).split('.')[0]))
        driver.implicitly_wait(60) # wait 1 min in case of QUEUE

        driver.find_element_by_id('checkout_email').send_keys(email)
        driver.find_element_by_id('checkout_shipping_address_first_name').send_keys(firstName)
        driver.find_element_by_id('checkout_shipping_address_last_name').send_keys(lastName)
        driver.find_element_by_id('checkout_shipping_address_address1').send_keys(address)
        driver.find_element_by_id('checkout_shipping_address_city').send_keys(city)
        driver.find_element_by_id('checkout_shipping_address_zip').send_keys(zip)
        driver.find_element_by_id('checkout_shipping_address_phone').send_keys(phone)
        driver.find_element_by_name('button').click()
        print("{} | Successfully inputted all contact information.".format(str(datetime.datetime.now()).split('.')[0]))

        #shipping button
        # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "continue_button")).click()
        time.sleep(5)
        driver.find_element_by_id('continue_button').click()
        print("{} | Successfully submitted shipping page.".format(str(datetime.datetime.now()).split('.')[0]))

        driver.implicitly_wait(60)
        iframe = driver.find_element_by_class_name('card-fields-iframe') #cardNumber iframe
        driver.switch_to.frame(iframe)

        driver.find_element_by_name('number').send_keys(cardNum[0]) # w/o splitting, returns '4447'
        driver.find_element_by_name('number').send_keys(cardNum[1])
        driver.find_element_by_name('number').send_keys(cardNum[2])
        driver.find_element_by_name('number').send_keys(cardNum[3])

        driver.switch_to.default_content() #resets iframe
        iframe2 = driver.find_element_by_xpath('//iframe[contains(@id, "card-fields-name")]') #card name iframe
        driver.switch_to.frame(iframe2)
        driver.find_element_by_xpath('//input[@id="name"]').send_keys(cardName)

        driver.switch_to.default_content()
        iframe3 = driver.find_element_by_xpath('//iframe[contains(@id, "card-fields-expiry")]')
        driver.switch_to.frame(iframe3)
        driver.find_element_by_xpath('//input[@id="expiry"]').send_keys(cardExp[0])
        driver.find_element_by_xpath('//input[@id="expiry"]').send_keys(cardExp[1])

        driver.switch_to.default_content()
        iframe4 = driver.find_element_by_xpath('//iframe[contains(@id, "card-fields-verification_value")]')
        driver.switch_to.frame(iframe4)
        driver.find_element_by_xpath('//input[@id="verification_value"]').send_keys(ccv)
        print("{} | Successfully illed out payment information.".format(str(datetime.datetime.now()).split('.')[0]))

        driver.switch_to.default_content()
        driver.find_element_by_id('continue_button').click()
        print("{} | Finalized checkout and submitted \'pay now\' button.".format(str(datetime.datetime.now()).split('.')[0]))


def main():
    file = open(sys.argv[1])
    elements = json.loads(file.read())
    url = (elements['url'])
    email = (elements['email'])
    firstName = (elements['firstName'])
    lastName = (elements['lastName'])
    address = (elements['address'])
    city = (elements['city'])
    zip = (elements['zip'])
    phone = (elements['phone'])
    cardNum = (elements['card number'])
    cardName = (elements['card name'])
    cardExp = (elements['card expiry'])
    ccv = (elements['ccv'])

    test = Scraper(url, email, firstName, lastName, address, city, zip, phone, cardNum, cardName, cardExp, ccv)
    test.scrape_init()

if __name__ == "__main__":
    sys.argv[:]
 	main()
