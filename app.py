from selenium import webdriver
from page.login_page import LoginPage
from config import USERID, PASSWORD
from time import sleep

# put your chromedriver location
driver = webdriver.Chrome(executable_path="./chromedriver.exe")

login_page = LoginPage(driver)
login_page.launchUrl("https://ibank.klikbca.com")
if login_page.verifyPage == False:
    print("Loading login page failed! is site running?")
    exit(1)

login_page.fillUserID(USERID)
sleep(3)
login_page.fillPassword(PASSWORD)
sleep(3)
main_page = login_page.clickLoginButton()
if main_page.verifyPage() == False:
    print("Login failed? check your UserID/Password")
    exit(1)
print("Login success")

# get balance
balance_page = main_page.clickMenuBalanceInquiry()
balances = balance_page.getBalance()

print("\nBalance Inquiry result:")
for balance in balances:
    print("{account:15s} {type:10s} {currency:5s} {amount:s}".format(**balance))

# get account statements
acct_stmt_page = main_page.clickMenuAccountStatement()
statements = acct_stmt_page.getStatements()

print("\nStatements result:")
for stat in statements:
    amount = float(stat['amount'].replace(',', ''))
    if stat['type'] == 'DB':
        amount = -1 * amount
    print("{0:6s} {1:16,.2f} {2}".format(
        stat['date'],
        amount,
        stat['description']))

# get transaction history
history_page = main_page.clickMenuTransactionHistory()
history = history_page.getHistory()

print("\nTransaction history:")
for h in history:
    print("{0:22s} {1:36s} {2:30s} {3:24s} {4}".format(
        h['date'], h['type'], h['description'], h['amount'], h['status']))


# logout and close chrome
main_page.clickLogout()

print("\nJob finished.")
driver.quit()
