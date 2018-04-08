from base.SeleniumDriver import cSeleniumDriver
import logging
import utilities.CustomLogger as cl
import time


class cHomepage(cSeleniumDriver):
    log = cl.CustomLogger(logging.DEBUG)
    #locators
    sSearchIn = "searchDropdownBox"
    sBooks = "//select[@id='searchDropdownBox']/option[text()='Books']"
    sSearchTextBox = "twotabsearchtextbox"
    sSearchIcon = "//input[@value='Go']"
    sFirstResult = "//li[@id='result_0']//img"
    sNoResult = "noResultsTitle"
    sSubNavBar = "//div[@id='nav-subnav']/a[1]/span"
    sSelectedDepartment = ".//select[@id='searchDropdownBox']/option[@selected='selected']"

    def __init__(self, driver):
        super(cHomepage, self).__init__(driver)

    def ClickSearchDropDown(self):
        self.ElementClick(self.sSearchIn)

    def ClickBooksFromDropDown(self):
        self.ElementClick(self.sBooks,"xpath")

    def GetSearchBox(self):
        return  self.GetElement(self.sSearchTextBox)

    def EnterSearchKey(self, sSearchKey):
        self.SendKeys(sSearchKey, self.sSearchTextBox)

    def ClickSearchIcon(self):
        self.ElementClick(self.sSearchIcon, "xpath")

    def ClickFirstResult(self):
        self.ElementClick(self.sFirstResult, "xpath")

    def GetNoResultsText(self):
        return self.GetText(self.sNoResult)

    def GetTitle(self):
        time.sleep(2)
        return self.driver.title

    def GetSubNavBarPresence(self):
        return self.IsElementPresent(self.sSubNavBar, "xpath")

    def GetSelectedDepartmentText(self):
        return self.GetText(self.sSelectedDepartment, "xpath")

    def SearchBook(self, sSearchKey):
        self.ClickSearchDropDown()
        self.ClickBooksFromDropDown()
        self.EnterSearchKey(sSearchKey)
        time.sleep(2)
        self.ClickSearchIcon()

    def SelectBook(self):
        self.ClickFirstResult()

    def VerifyNoResultText(self, sSearchKey):
        self.SearchBook(sSearchKey)
        bResult = self.IsElementDisplayed(self.sNoResult)
        sSearchResultText = self.GetNoResultsText()
        return bResult, sSearchResultText

    def ClearSearchBar(self):
        self.GetSearchBox().clear()

    def VerifySubNavigationBarPresence(self):
        return self.GetSubNavBarPresence()

