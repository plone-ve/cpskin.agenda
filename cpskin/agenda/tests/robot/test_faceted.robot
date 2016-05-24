*** Settings ***

Resource        plone/app/robotframework/selenium.robot
Resource        plone/app/robotframework/keywords.robot

Library         Remote  ${PLONE_URL}/RobotRemote

Test Setup      Open test browser
Test Teardown   Close all browsers


*** Test Cases ***
