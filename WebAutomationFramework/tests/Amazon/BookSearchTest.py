import unittest
import pytest
import utilities.CustomLogger as cl
import logging
from pages.HomePage import cHomepage
from pages.ProductBookPage import cProductBook
from ddt import ddt, data, unpack
from utilities.ReadCsvData import GetCSVData
from utilities.TestStatus import cTestStatus
import os
@pytest.mark.usefixtures("OneTimeSetUp", "setUp")
@ddt
class cBookSearch(unittest.TestCase):
    log = cl.CustomLogger(logging.DEBUG)

    @pytest.fixture(autouse=True)
    def ObjectSetup(self, OneTimeSetUp):
        self.oHomePage = cHomepage(self.driver)
        self.oBook = cProductBook(self.driver)
        self.oTS = cTestStatus(self.driver)
        self.bResult = True
        self.lFailureMsg = []

    @data(*GetCSVData(os.path.join(os.getcwd(),"testdata.csv")))
    @unpack
    #@pytest.mark.run(order=3)
    def test_3_VerifyBookSearch(self, sBookToSearch):
        try:
            self.PrintStep("3 : test_VerifyBookSearch")

            self.oHomePage.SearchBook(sBookToSearch)
            self.assertEqual("Books", self.oHomePage.GetSelectedDepartmentText())
            sTitle = self.oHomePage.GetTitle()
            self.assertEqual(sTitle, "Amazon.com: " + sBookToSearch + ": Books")
            bPresent = self.oHomePage.VerifySubNavigationBarPresence()
            if not bPresent:
                self.UpdateResult(False, "Sub Navigation Bar Verification")

            self.oHomePage.SelectBook()
            sTitle, dAuthorInfo = self.oBook.GetBookInfo()
            dBookPrice = self.oBook.GetBookPrice()
            sRatings = self.oBook.GetBookRatings()
            self.log.info("\n")
            self.log.info("------------------")
            self.log.info(" BOOK INFORMATION ")
            self.log.info("------------------")

            if sTitle != None:
                self.log.info("Book Title : " + str(sTitle))
            else:
                self.UpdateResult(False, "Unable to get Title")

            if len(dAuthorInfo) >= 1:
                for sAuthor in dAuthorInfo.keys():
                    self.log.info("By : " + str(sAuthor))
                    self.log.info("Contribution : " + str(dAuthorInfo[sAuthor]))
            else:
                self.UpdateResult(False, "Unable to get Author Info")

            if sRatings != None:
                self.log.info("Ratings : " + sRatings)
            else:
                self.UpdateResult(False, "Unable to get Ratings")

            if len(dBookPrice) >= 1:
                self.log.info("Available modes and price :")
                for sMode in dBookPrice.keys():
                    self.log.info(str(sMode) + " : " + str(dBookPrice[sMode]))
            else:
                self.UpdateResult(False, "Unable to get Book Price")

            if not self.bResult:
                self.oTS.FinalResult("test_3_VerifyBookSearch", self.bResult, str(self.lFailureMsg))
            else:
                self.oTS.FinalResult("test_3_VerifyBookSearch", self.bResult, "Book Information")

        except (KeyError, ValueError, TypeError) as Ex:
            self.log.error("Error Occured : " + str(Ex))
            self.oTS.FinalResult("test_3_VerifyBookSearch", False, "KeyError, ValueError, TypeError")
        except AssertionError as Ex:
            self.log.error("Assertion Error : " + str(Ex))
            self.oTS.FinalResult("test_3_VerifyBookSearch", False, "Assertion Fail")

    #@pytest.mark.run(order=2)
    def test_2_VerifyNoResults(self):
        try:
            self.PrintStep("2 : test_VerifyNoResults")

            sSearchKey = "Kurudhipunal"
            self.bResult, sSearchResulText = self.oHomePage.VerifyNoResultText(sSearchKey)
            self.assertEqual("Books", self.oHomePage.GetSelectedDepartmentText())
            sTitle = self.oHomePage.GetTitle()
            self.assertEqual(sTitle, "Amazon.com: " + sSearchKey + ": Books")
            if self.bResult:
                self.assertIn(sSearchKey, sSearchResulText)

            self.oTS.FinalResult("test_VerifyNoResults", self.bResult, "No Result Verification")

        except AssertionError as Ex:
            self.log.error("Assertion Error : " + str(Ex))
            self.oTS.FinalResult("test_NoResult", False, "Assertion Fail")


    # @pytest.mark.run(order=1)
    def test_1_VerifyTitle(self):
        try:
            self.PrintStep("1 : test_VerifyTitle")

            sTitle = self.oHomePage.GetTitle()
            self.assertEqual(sTitle, "Amazon.com: Online Shopping for Electronics, Apparel, Computers, Books, DVDs & more")
            self.oTS.FinalResult("test_VerifyTitle", self.bResult, "Title Verification")
        except AssertionError as Ex:
            self.log.error("Assertion Error : " + str(Ex))
            self.oTS.FinalResult("test_VerifyTitle", False, "Assertion Fail")

    def PrintStep(self, sTestName):
        self.log.info("******************************")
        self.log.info("Test " + sTestName)
        self.log.info("******************************")
        self.log.info("\n")

    def UpdateResult(self, bResult, sMsg):
        self.bResult = bResult
        self.lFailureMsg.append(sMsg)
        self.oTS.StepResult(self.bResult, sMsg)

    def tearDown(self):
        self.oHomePage.ClearSearchBar()

