"""
@package utilities

cTestStatus class implementation
It provides functionality to assert the bResult

"""
import utilities.CustomLogger as cl
import logging
from base.SeleniumDriver import cSeleniumDriver
from traceback import print_stack

class cTestStatus(cSeleniumDriver):

    log = cl.CustomLogger(logging.INFO)

    def __init__(self, driver):
        """
        Inits CheckPoint class
        """
        super(cTestStatus, self).__init__(driver)
        self.lResultList = []

    def SetResult(self, bResult, sResultMessage):
        try:
            if bResult is not None:
                if bResult:
                    self.lResultList.append("PASS")
                    self.log.info("\n")
                    self.log.info("### VERIFICATION SUCCESSFUL :: + " + sResultMessage)
                    self.log.info("\n")
                else:
                    self.lResultList.append("FAIL")
                    self.log.info("\n")
                    self.log.error("### VERIFICATION FAILED :: + " + sResultMessage)
                    self.ScreenShot(sResultMessage)
            else:
                self.lResultList.append("FAIL")
                self.log.info("\n")
                self.log.error("### VERIFICATION FAILED :: + " + sResultMessage)
                self.ScreenShot(sResultMessage)
        except:
            self.lResultList.append("FAIL")
            self.log.info("\n")
            self.log.error("### Exception Occurred !!!")
            self.ScreenShot(sResultMessage)
            print_stack()

    def StepResult(self, bResult, sResultMessage):
        """
        Mark the bResult of the verification point in a test case
        """
        self.SetResult(bResult, sResultMessage)

    def FinalResult(self, testName, bResult, sResultMessage):
        """
        Mark the final bResult of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final test status of the test case
        """
        self.SetResult(bResult, sResultMessage)

        if "FAIL" in self.lResultList:
            self.log.info("\n")
            self.log.error(testName +  " ### TEST FAILED")
            self.log.info("\n")
            self.lResultList.clear()
            assert True == False
        else:
            self.log.info("\n")
            self.log.info(testName + " ### TEST SUCCESSFUL")
            self.log.info("\n")
            self.lResultList.clear()
            assert True == True