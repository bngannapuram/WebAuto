from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import sys, csv, time
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.info("BEGIN")

timeout = 10

url = "https://www.dicksmith.com.au/"
testDataFile = "testdata_webui.csv"

chrome_driver_path = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
# options.add_argument('headless') 
driver=webdriver.Chrome(options=options, executable_path=chrome_driver_path)

def launchWebsite(url):
    """
    @param url: url to launch 
    """
    try:
        driver.get(url)
        wait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'product-search-field')))
        logging.info("Launched %s" % str(url))
        dismissOfferDialog()
    except TimeoutException as e:
        logging.info("Failed to load URL")
        return 1

def searchProduct(item):
    """
    @param item: item to search for
    """
    logging.info("Searching '%s'" % str(item))
    try:
        pObj = wait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'product-search-field')))
        pObj.clear()
        pObj.send_keys(item)
    
        scrollViewToElementAndClick("//button[contains(@class,'search-nav__button')][@type='submit']")

        wait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'department-title')))
        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'View as')]")))
        logging.info(" => %s found" % str(item))
    except TimeoutException as e:
        logging.info(" => %s not found/not in stock" % str(item))
        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@class='react-autosuggest__container']/button"))).click()
        return 1

def addItemToCart(item):
    """
    @param item: item to add to cart
    """
    try:
        pObj = driver.find_elements_by_xpath("//div[@class='_1umis']/figure")
        pObj[0].click()

        scrollViewToElementAndClick("//button[@type='submit']//span[text()='Add to Cart']")
        wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//p[text()='Added to Cart']")))
        logging.info(" => Item added to cart...")
    except TimeoutException as e:
        logging.info("'%s' not found, continuing.." % str(item))
        return 1

def checkoutItems():
    """
    checkout items for making payment
    """
    try:
        logging.info("Checking out items")
        scrollViewToElementAndClick("//span[contains(text(),'Cart')]")

        try:
            # Shopping Cart
            wait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Your Shopping Cart']")))
            pObj = driver.find_elements_by_xpath("//span[text()='Checkout']")
            pObj[0].click()
    
            # Billing/Shipping Information
            scrollViewToElementAndInputText("//input[@id='email']", "myorder123@gmail.com")
            scrollViewToElementAndInputText("//input[@id='full_name']", "Balanagesh")
            scrollViewToElementAndInputText("//input[@id='phone']", "0447083777")
            scrollViewToElementAndClick("//span[text()='Continue']")
            logging.info(" => Entered Contact details...")
    
            scrollViewToElementAndSelectText("//input[@id='address']", "7 Sturrock Court, Altona Meadows")
            logging.info(" => Entered Delivery details...")

            pObj = driver.find_elements_by_xpath("//span[text()='Continue']")
            pObj[0].click()
        except:
            logging.info("Failed to checkout...")

        # Payment Information
        scrollViewToElementAndClick("//h4[text()='Credit Card']")
        scrollViewToElementAndInputText("//input[@name='number']", "5555555555554444")
        scrollViewToElementAndInputText("//input[@name='expiry']", "1220")
        scrollViewToElementAndInputText("//input[@name='cvc']", "123")
        pObj = driver.find_elements_by_xpath("//input[@name='name']")
        c = len(pObj)
        pObj[c-1].send_keys('Random Name')
        logging.info(" => Entered payment details...")
        time.sleep(5)

    except:
        logging.info("Cart is Empty, please add items...")

def dismissOfferDialog():
    """
    Dismiss the offer dialog banner
    """
    try:
        scrollViewToElementAndClick("//div[text()='\xd7']")
        logging.info(" => Dismiss offer dialog")
    except TimeoutException as e:
        pass

def dismissCovidUpdate():
    """
    Dismiss the covid update banner
    """
    try:
        scrollViewToElementAndClick("//div[@id='kespa-close-button']")
        logging.info(" => Dismiss covid update banner")
    except TimeoutException as e:
        pass

def scrollViewToElement(pObjXpath, waittime=15, count=1):
    '''
    Scroll view to the element
    @param pObjXpath: element to scrollview to 
    '''
    scroll = 0
    pObj = wait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, pObjXpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', pObj)
        time.sleep(2)
        scroll += 1
    time.sleep(2)

def scrollViewToElementAndClick(pObjXpath, waittime=15, count=1):
    '''
    Scroll view to the element and click
    @param pObjXpath: element to scrollview to 
    '''
    scroll = 0
    pObj = wait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, pObjXpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', pObj)
        time.sleep(2)
        scroll += 1
    time.sleep(2)
    pObj.click()

def scrollViewToElementAndSelectText(pObjXpath, input_text, times=0, count=1):
    '''
    Scroll view to the element, enter text, select matching text with arrow keys and press enter
    @param pObjXpath: element to scrollview to 
    @param input_text: text to enter
    @param arrow: ARROW_DOWN/ARROW_UP/ARROW_LEFT/ARROW_RIGHT arrow key to press
    @param press: after selecting press ENTER key
    @param times: no. of times to do backspace
    @param count: no. of times to scroll 
    '''
    scroll = 0
    pObj = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, pObjXpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', pObj)
        time.sleep(2)
        scroll += 1
    for i in range(times):
        pObj.send_keys(Keys.BACKSPACE)
    pObj.send_keys(input_text)
    time.sleep(2)
    pObj.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    pObj.send_keys(Keys.ENTER)

def scrollViewToElementAndInputText(pObjXpath, input_text, waittime=15, count=1):
    '''
    Scroll view to the element and input text
    @param pObjXpath: element to scrollview to 
    @param input_text: text to enter
    '''
    scroll = 0
    pObj = wait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, pObjXpath)))
    while scroll < count: # scroll count times
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', pObj)
        time.sleep(2)
        scroll += 1
    pObj.clear()
    pObj.send_keys(input_text)

def exitBrowser():
    """
    Exit the browser
    """
    driver.close()
    driver.quit()


if __name__ == "__main__":

    if (1 == launchWebsite(url)): sys.exit()
    flag = True
    with open(testDataFile, 'r') as readfile:
        csv_reader = csv.reader(readfile, delimiter=',')
        for row in csv_reader:
            product = str(row[0])
            if (1 == searchProduct(product)): continue
            if flag == True:
                dismissCovidUpdate()
                flag = False
            if (1 == addItemToCart(product)): continue
    checkoutItems()
    readfile.close()
    exitBrowser()
    LOGGER.info("END")
