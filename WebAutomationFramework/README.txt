WebAutomationFrameWork

This is a python framework, used to automate any webpage with slight modifications
The framework is built with Unittest and pytest in combination for better flexibility and efficiency
Selenium is the core in this framework

Requirements:
install Python 3 or above
and use pip3 to insall the following:
 selenium
 pytest
 ddt



FrameWork Components:

base        - All core and high level (super classes) modules goes here
configfiles - All configuration files, if any goes here(future use)
pages       - All the page objects goes here
tests       - All the test scripts goes here
utilities   - All the common functionalities which can be utilised by throughout the framework goes here

Report is created under WebAutomationFrameWork/automation.log
Currently every time the automation.log file needs to be deleted before running a test.
Otherwise, the test logs will append.

testdata.csv - to run the same testcase with multiple data sets.
tests/TestSuite.py - to run multiple test scripts as a suite.

How to run a test script?
Eg: py.test -s -v tests\Amazon\BookSearch.py --browser chrome

How to run a test suite?
Eg: py.test -s -v tests\TestSuite.py --browser firefox

Coding standard followed:

print() is avoided and replaced with log
indentation : 4 spaces
variable names should be prefixed with the type of the variable, in order to easily identify the variable type for debugging
eg: variable name of a list object : lNames
                 dictionary object : dNames
                     string object : sNames
           integer or float object : fiValue
                 object of a class : oClassObject
                        class name : cClassName()

