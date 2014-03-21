from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait #WebDriverWait need add the 
from selenium.webdriver.support import expected_conditions as EC #WebDriverWait need add the 
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, traceback
import logging

def log_info(info):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='hop2.log',
                        filemode='a')
    logging.info(info+"\n")

def log(info,warning):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='hop2.log',
                        filemode='a')
    #logging.debug()
    if warning is None:
        logging.info(info+"\n")
    else:
        logging.warning(warning+"\n")
    #logging.error(error+"\n")
    #logging.critical()

def log_warning(warning):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='hop2.log',
                        filemode='a')
    logging.warning(warning+"\n")

       
class Hop2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        # self.driver=webdriver.Remote("http://localhost:4444/wd/hub",webdriver.DesiredCapabilities.HTMLUNIT.copy())
        # self.driver.implicitly_wait(3)
        #self.driver.set_page_load_timeout(60)
        self.base_url = "http://www.hop2.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_hop2(self):
        try:
            driver = self.driver
            driver.get(self.base_url + "/")
            #self.assertTrue(self.is_element_present("ID","_FromCit")) #assertTrue must add self
            driver.find_element_by_id("_FromCity").clear()
            driver.find_element_by_id("_FromCity").send_keys("pvg")
            driver.find_element_by_id("_ToCity").clear()
            driver.find_element_by_id("_ToCity").send_keys("sfo")
            driver.find_element_by_id("btnFlightSearch").click()
            # for i in range(0,5):
            #     if i>3:
            #         assert "Time Out" 
            #     if self.is_element_present("id","nowTicketsNum"):
            #         break
            #     time.sleep(1)
            WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID,"chkZZ"))).click()
            info_tickets="Tickets search Result is "+str(self.is_element_present('id','nowTicketsNum'));## is there ticket
            driver.find_element_by_link_text("Book Now").click();
            select_card=Select(driver.find_element_by_id("PaymentInfo_ddlCardType"))##-----dropbox select
            select_card.select_by_index(1)
            driver.find_element_by_id("PaymentInfo_txtCreditCardNumber_txtMustInput").clear()
            driver.find_element_by_id("PaymentInfo_txtCreditCardNumber_txtMustInput").send_keys("5499980000000000")
            driver.find_element_by_id("btnBook").click()
            time.sleep(5)
            info=info_tickets+". booking page:  "+str(driver.find_element_by_id("CheckCCNumber").is_displayed())
            log(info,None)
        except:
            log(None,str(traceback.format_exc()))
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
