from base.SeleniumDriver import cSeleniumDriver
from collections import OrderedDict
import logging
import utilities.CustomLogger as cl
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class cProductBook(cSeleniumDriver):
    log = cl.CustomLogger(logging.DEBUG)

    # locators
    sBookTitle = "productTitle"
    sAuthors = "//div[@id='bylineInfo']/span[contains(@class,'author')]"
    sMainAuthor = "./span/a[1]"
    sOtherAuthor = ".//a[1]"
    # sAuthors = "//div[@id='byline']/span[contains(@class,'author')]/span/a[1]"
    # sContributions = "//div[@id='byline']//span[@class = 'contribution']/span"
    sContributions = "//div[@id='bylineInfo']//span[@class = 'contribution']/span"
    sAverageCustomerReview = "//div[@id='averageCustomerReviews']//span[contains(text(),'stars')]"
    sMediaTab = "mediaTabsHeadings"
    sMediaTabHeadings = "//div[@id='mediaTabsHeadings']/ul/li"
    sMediaTabTitle = ".//span[contains(@class,'mediaTab_title')]"
    sMediaTabSubTitle = ".//span[contains(@class,'mediaTab_subtitle')]"
    sSwatches = "tmmSwatches"
    sAnnounces = "//div[@id='tmmSwatches']//span[@class='a-button-inner']"
    sAnnounceTitle = ".//span[1]"
    sAnnounceSubTitle = ".//span[2]/span"

    def __init__(self,driver):
        super(cProductBook, self).__init__(driver)
        self.sTitle = ""
        self.dAuthorInfo = OrderedDict()
        self.sRatings = ""
        self.dBookPrice = OrderedDict()

    # Element Action Methods
    def GetBookTitle(self):
        return self.GetText(self.sBookTitle)

    def GetAuthors(self):
        elAuthors = []
        elAuthorClass = self.GetElementList(self.sAuthors, "xpath", bWaitForElement=True)
        # self.log.info("len of elAuthors : " + str(len(elAuthorClass)))
        for eAuthorClass in elAuthorClass:
            eAuthor = self.GetElement(self.sMainAuthor, "xpath", element=eAuthorClass, isLog=False)
            if eAuthor is None:
                eAuthor = self.GetElement(self.sOtherAuthor, "xpath", element=eAuthorClass)
            elAuthors.append(eAuthor)

        return elAuthors

    def GetContributions(self):
        return self.GetElementList(self.sContributions, "xpath", bWaitForElement=True)

    def GetAverageCustomerReview(self):
        return self.GetText(self.sAverageCustomerReview, "xpath")

    def GetMediaTab(self):
        return self.GetElement(self.sMediaTab, isLog=False)

    def GetMediaTabHeadings(self):
        elMediaTabHeadings = None
        eMediaTab = self.GetMediaTab()
        if eMediaTab != None:
            elMediaTabHeadings = self.GetElementList(self.sMediaTabHeadings,"xpath",)

        return elMediaTabHeadings

    def GetSwatches(self):
        return self.GetElement(self.sSwatches)

    def GetAnnounces(self):
        elAnnounces = None
        eSwatches = self.GetSwatches()
        if eSwatches != None:
            elAnnounces = self.GetElementList(self.sAnnounces, "xpath")

        return elAnnounces

    # Functionality Methods
    def GetBookInfo(self):
        self.sTitle = self.GetBookTitle()
        elAuthors = self.GetAuthors()
        elContributions = list(self.GetContributions())
        # self.log.info("len of elcontribution : " + str(len(elContributions)))
        for (eAuthor, eContribution) in zip(elAuthors,elContributions):
            self.dAuthorInfo[self.GetText(element=eAuthor)] = self.GetText(element=eContribution)

        return self.sTitle, self.dAuthorInfo

    def GetBookPrice(self):
        elMediaTabHeadings = self.GetMediaTabHeadings()
        if elMediaTabHeadings != None and len(elMediaTabHeadings) >= 1:
            for eHeading in elMediaTabHeadings:
                if self.IsElementDisplayed(element=eHeading):
                    eMediaTabTitle = self.GetElement(self.sMediaTabTitle, "xpath", eHeading)
                    sMediaTabTitle = self.GetText(element=eMediaTabTitle)
                    ePrice = self.GetElement(self.sMediaTabSubTitle, "xpath", eHeading)
                    sPrice = self.GetText(element=ePrice)
                    self.dBookPrice[sMediaTabTitle] = sPrice
        else:
            elAnnounces = self.GetAnnounces()
            if elAnnounces != None and len(elAnnounces) >= 1:
                for eAnnounce in elAnnounces:
                    if self.IsElementDisplayed(element=eAnnounce):
                        eAnnounceTitle = self.GetElement(self.sAnnounceTitle, "xpath", eAnnounce)
                        sAnnounceTitle = self.GetText(element=eAnnounceTitle)
                        ePrice = self.GetElement(self.sAnnounceSubTitle, "xpath", eAnnounce)
                        sPrice = self.GetText(element=ePrice)
                        self.dBookPrice[sAnnounceTitle] = sPrice

        return self.dBookPrice

    def GetBookRatings(self):
        self.sRatings = self.GetAverageCustomerReview()
        self.WebScroll("down", "-200")
        return self.sRatings
