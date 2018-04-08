from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.CustomLogger as cl
import logging
import time
import os

class cSeleniumDriver():

    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def ScreenShot(self, sResultMessage):
        """
        Takes screenshot of the current open web page
        """
        fileName = sResultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
            self.log.info("\n")
        except Exception as Ex:
            self.log.error("### Exception Occurred when taking screenshot : " + str(Ex))
            print_stack()

    def GetTitle(self):
        return self.driver.title

    def GetByType(self, sLocatorType):
        sLocatorType = sLocatorType.lower()
        if sLocatorType == "id":
            return By.ID
        elif sLocatorType == "name":
            return By.NAME
        elif sLocatorType == "xpath":
            return By.XPATH
        elif sLocatorType == "css":
            return By.CSS_SELECTOR
        elif sLocatorType == "class":
            return By.CLASS_NAME
        elif sLocatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("sLocator type " + sLocatorType +
                          " not correct/supported")
        return False

    def GetElement(self, sLocator, sLocatorType="id", element=None, bWaitForElement = False, isLog = True):
        eElement = None
        sLocatorType = sLocatorType.lower()
        sByType = self.GetByType(sLocatorType)
        try:
            if bWaitForElement:
                self.WaitForElement(sLocator, sLocatorType)
            if element != None:
                eElement =  element.find_element(sByType, sLocator)
            else:
                eElement = self.driver.find_element(sByType, sLocator)

            if eElement == None and isLog:
                self.log.info("Element not found with sLocator: " + sLocator + " and  sLocatorType: " + sLocatorType)

        except Exception as Ex:
            if isLog:
                self.log.info("Exception : ", Ex)
                self.log.info("Element not found with sLocator: " + sLocator + " and  sLocatorType: " + sLocatorType)
        return eElement

    def GetElementList(self, sLocator, sLocatorType="id", bWaitForElement = False):
        """
        NEW METHOD
        Get list of elements
        """
        element = None
        try:
            sLocatorType = sLocatorType.lower()
            byType = self.GetByType(sLocatorType)
            if bWaitForElement:
                self.WaitForElement(sLocator, sLocatorType)
            element = self.driver.find_elements(byType, sLocator)
        except Exception as Ex:
            self.log.info("Exception : ", Ex)
            self.log.info("Element list not found with sLocator: " + sLocator +
                          " and sLocatorType: " + sLocatorType + " Exception : " + str(Ex))
        return element

    def ElementClick(self, sLocator="", sLocatorType="id", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of sLocator and sLocatorType
        """
        try:
            if sLocator:  # This means if sLocator is not empty
                element = self.GetElement(sLocator, sLocatorType)
            element.click()

        except Exception as Ex:
            self.log.info("Cannot click on the element with sLocator: " + sLocator +
                          " sLocatorType: " + sLocatorType + " Exception : " + str(Ex))
            print_stack()

    def SendKeys(self, data, sLocator="", sLocatorType="id", element=None):
        """
        Send keys to an element -> MODIFIED
        Either provide element or a combination of sLocator and sLocatorType
        """
        try:
            if sLocator:  # This means if sLocator is not empty
                element = self.GetElement(sLocator, sLocatorType)
            element.send_keys(data)
        except Exception as Ex:
            self.log.info("Cannot send data on the element with sLocator: " + sLocator +
                  " sLocatorType: " + sLocatorType + " Exception : " + str(Ex))
            print_stack()

    def ClearField(self, sLocator="", sLocatorType="id"):
        """
        Clear an element field
        """
        element = self.GetElement(sLocator, sLocatorType)
        element.clear()

    def GetText(self, sLocator="", sLocatorType="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of sLocator and sLocatorType
        """
        try:
            if sLocator: # This means if sLocator is not empty
                element = self.GetElement(sLocator, sLocatorType)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("textContent")
            if len(text) != 0:
                #self.log.info("Getting text on element :: " +  info)
                #self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except Exception as Ex:
            self.log.error("Failed to get text on element " + str(Ex))
            print_stack()
            text = None
        return text

    def IsElementPresent(self, sLocator="", sLocatorType="id", element=None):
        """
        Check if element is present -> MODIFIED
        Either provide element or a combination of sLocator and sLocatorType
        """
        try:
            if sLocator:  # This means if sLocator is not empty
                element = self.GetElement(sLocator, sLocatorType)
            if element is not None:
                return True
            else:
                self.log.info("Element not present with sLocator: " + sLocator +
                              " sLocatorType: " + sLocatorType)
                return False
        except Exception as Ex:
            self.log.error("Element not found : " + str(Ex))
            return False

    def IsElementDisplayed(self, sLocator="", sLocatorType="id", element=None):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of sLocator and sLocatorType
        """
        isDisplayed = False
        try:
            if sLocator:  # This means if sLocator is not empty
                element = self.GetElement(sLocator, sLocatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
            else:
                self.log.info("Element not displayed")
            return isDisplayed
        except Exception as Ex:
            self.log.error("Element not found : " + str(Ex))
            return False

    def ElementPresenceCheck(self, sLocator, sLocatorType):
        """
        Check if element is present
        """
        try:
            elementList = self.driver.find_elements(sLocatorType, sLocator)
            if len(elementList) > 0:
                return True
            else:
                self.log.info("Element not present with sLocator: " + sLocator +
                              " sLocatorType: " + str(sLocatorType))
                return False
        except Exception as Ex:
            self.log.error("Element not found" + str(Ex))
            return False

    def WaitForElement(self, sLocator, sLocatorType="id", fiTimeout=3, fiPollFrequency=0.5):
        element = None
        try:
            byType = self.GetByType(sLocatorType)
            # self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=fiTimeout,
                                 poll_frequency=fiPollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, sLocator)))
        except Exception as Ex:
            self.log.error("Element not appeared on the web page with sLocator : " + sLocator + " sLocatorType : " + sLocatorType + " Exception : " + str(Ex))
            #print_stack()
        return element

    def WebScroll(self, sDirection="up" , sValue = "500"):
        if sDirection == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, " + str(sValue) + ");")

        if sDirection == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, " + str(sValue) + ");")
