import os
import json
import random
import hashlib
from datetime import datetime
from getpass import getpass

def validatePassword(password:str, minimum:int):
    special_characters = "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?"
    if len(password) < minimum:
        print(f"Password cannot be greater than {minimum}")
        return False
    if not any(char.isupper() for char in password):
        print(f"Password must contain atleast 1 UpperCase")
        return False
    if not any(char.islower() for char in password):
        print(f"Password must contain atleast 1 LowerCase")
        return False
    if not any(char.isdigit() for char in password):
        print(f"Password must contain atleast 1 Digit")
        return False
    if not any(char in special_characters for char in password):
        print(f"Password must contain atleast 1 Special characters")
        return False
    return True

def strHash(string:str):
    return(hashlib.md5(string.encode()).hexdigest())

def print_centered(text, length):
    width_text = len(text)
    gap = (length - width_text)
    print(f" "*(gap//2), end="")
    print(f"{text}", end="")
    print(f" "*(gap//2))

class Account:
    def __init__(self, filePath:str):
        self.filePath = filePath
        self.account = json.load(open(filePath,'r+'))
        self.emails = [email["email"] for email in self.account["accounts"]]
        self.accountNumbers = [number["accountNumber"] for number in self.account["accounts"]]

    def createAccount(self, accountInfo:dict):
        accountInfo["accountNumber"] = int(f"{datetime.now().year}0000{random.randint(1000, 9999)}{str(len(self.accountNumbers)).zfill(4)}")
        if accountInfo["email"] in self.emails:
            print(f'{accountInfo["email"]} account already exist with this email.')
            return False
        if int(accountInfo["amount"]) < 500:
            print(f'Minimum amount greater than 500')
            return False
        if len(accountInfo["pin"]) != 4:
            print(f'Account pin must be 4 digit')
            return False
        if validatePassword(accountInfo["password"], minimum=8):
            accountInfo["password"] = strHash(accountInfo["password"])
            self.account["accounts"].append(accountInfo)
            with open(self.filePath, 'w') as f:
                json.dump(self.account, f, indent=4)
            print("Account created successfull. ",accountInfo["accountNumber"])
            return accountInfo["accountNumber"]
        return False

    def login(self, email:str, password:str):
        if email in self.emails:
            allAccounts = {account['email']: account for account in self.account['accounts']}
            password = strHash(password)
            accountByEmail = allAccounts.get(email)
            if accountByEmail["password"] == password:
                print(f"Logged as {email}")
                return True
            else:
                print(f"Wrong pasword for {email}")
                return False
        else:
            print(f"Account not found with {email}")
            return False
        


class MainAccount:
    def __init__(self, LOGGED_EMAIL:str, filePath:str):
        self.LOGGED_EMAIL = LOGGED_EMAIL
        self.filePath = filePath
        self.accounts = json.load(open(filePath,'r+'))
        self.accountByAc = {account['accountNumber']: account for account in self.accounts['accounts']}
        self.accountInfo = {account['email']: account for account in self.accounts['accounts']}.get(self.LOGGED_EMAIL)

    def getName(self):
        return self.accountInfo["fullName"]
    
    def getAmount(self):
        return int(self.accountInfo["amount"])
    
    def getPin(self):
        return self.accountInfo["pin"]
    
    def getEmail(self):
        return self.accountInfo["email"]
    
    def getAccountNo(self):
        return self.accountInfo["accountNumber"]
    
    def setAmount(self, amount:int):
        self.accountByAc.get(self.getAccountNo())["amount"] -= amount
    def loadAmount(self, amount:int):
        self.accountByAc.get(self.getAccountNo())["amount"] += amount
    def saveData(self):
        accounts_list = []
        for account_number, account_info in self.accountByAc.items():
            accounts_list.append({
                'fullName': account_info['fullName'],
                'email': account_info['email'],
                'password': account_info['password'],
                'pin': account_info['pin'],
                'amount': account_info['amount'],
                'accountNumber': account_number
                })
        accounts_data = {'accounts': accounts_list}
        with open(self.filePath, 'w') as json_file:
            json.dump(accounts_data, json_file, indent=4)

    def transerAmount(self, amount:int, accountNumber:int):
        self.accountByAc.get(accountNumber)["amount"] += amount
        self.saveData()

def mainMenu(LOGGED_EMAIL):
    os.system('cls' if os.name == 'nt' else 'clear')
    logged_ac = MainAccount(LOGGED_EMAIL, "account.json")
    while True:
        print("-"*LENGTH)
        print_centered(f"Name: {logged_ac.getName()}     Amount: {logged_ac.getAmount()}", length=LENGTH)
        print_centered(f"Account No: {logged_ac.getAccountNo()}", LENGTH)
        print("-"*LENGTH)
        print("1. Send Money")
        print("2. Load Money")
        print("3. Check Statement")
        print("4. Exit")
        sel = input("Select any option: ")
        try:
            sel = int(sel)
        except:
            print("Invalid select")
        if sel == 4 or sel == 0:
            print("Exiting....")
            exit()
        elif sel == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-"*LENGTH)
            print_centered(f"Name: {logged_ac.getName()}     Amount: {logged_ac.getAmount()}", length=LENGTH)
            print("-"*LENGTH)
            ac_number = input("Enter Account Number (15 Digit): ")
            blance = input("Enter amount: ")
            remarks = input("Enter remarks: ")
            pin = getpass("Enter your security 4 digit Pin:  ")
            print("-"*LENGTH)
            if not int(ac_number) in ac.accountNumbers:
                print("Account not found.")
            if int(blance) < logged_ac.getAmount():
                if str(remarks) == "":
                    print("Remarks cannot be empty")
                if str(pin) == str(logged_ac.getPin()):
                    print("-"*LENGTH)
                    logged_ac.setAmount(amount=int(blance))
                    logged_ac.transerAmount(amount=int(blance), accountNumber=int(ac_number))
                    print(f"Amount transfed to {ac_number} Rs {blance}")
                    # TODO: Make a function to save statement of all tranction in json file
                else:
                    print("Incorrect Pin !")
            else:
                print("Insufficient blance !")
        elif sel == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-"*LENGTH)
            print_centered(f"Name: {logged_ac.getName()}     Amount: {logged_ac.getAmount()}", length=LENGTH)
            print("-"*LENGTH)
            blance = input("Enter amount: ")
            remarks = input("Enter remarks: ")
            pin = getpass("Enter your security 4 digit Pin:  ")
            print("-"*LENGTH)
            if int(blance) > 0:
                if str(remarks) == "":
                    print("Remarks cannot be empty")
                if str(pin) == str(logged_ac.getPin()):
                    logged_ac.loadAmount(int(blance))
                    logged_ac.saveData()
                    print(f"Rs {blance} loaded sucessfully to {logged_ac.getAccountNo()}")
                    # TODO: Make a function to save statement of all tranction in json file
                else:
                    print("Incorrect Pin !")
            else:
                print("Amount must be greater than 0")

if __name__ == "__main__":
    LOGGED_EMAIL = None
    LENGTH = 50
    ac = Account("account.json")
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print("-"*LENGTH)
        print_centered("Python Banking System by Sachin Shrivastav", length=LENGTH)
        print("-"*LENGTH)
        print("1.     Login with account")
        print("2.     Create Account")
        print("3.     Exit")
        sel = input("Select any option: ")
        try:
            sel = int(sel)
        except:
            print("Invalid select")
        if sel == 3 or sel == 0:
            print("Exiting....")
            exit()
        elif sel == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-"*LENGTH)
            print_centered("Create new account", length=LENGTH)
            print("-"*LENGTH)
            fullName = input("Enter your full name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            pin = input("Enter your 4 digit pin: ")
            amount = input("Enter your minimum amount (600): ")
            print("-"*LENGTH)
            accountInfo = {"fullName": str(fullName),"email": str(email),"password": str(password),"pin": str(pin),"amount":int(amount)}
            ac.createAccount(accountInfo)
        elif sel == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-"*LENGTH)
            print_centered("Login with Email & Password", length=LENGTH)
            print("-"*LENGTH)
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            login_status = ac.login(str(email), str(password))
            if login_status:
                LOGGED_EMAIL = email
                mainMenu(LOGGED_EMAIL)
                