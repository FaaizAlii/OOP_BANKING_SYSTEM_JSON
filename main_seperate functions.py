import random
import json
import time
import re


# -___--___-User Class--create account / Del account / Show info---
class User:
    def __init__(self, name: str, father_name: str, id: int, password: str, cash: int):
        self.name = name
        self.father_name = father_name
        self.id = id
        self.password = password
        self.cash = cash

    @staticmethod
    def menu():
        print("1 - Create Account")
        print("2 - Delete Account")
        print("3 - Deposit Money")
        print("4 - Withdraw Money")
        print("5 - Transfer Money")
        print("6 - View An Account Details")
        print("0 - Exit")

    def show_info(self):
        print(f"\nname        :{self['name']}")
        print(f"Father name :{self['father_name']}")
        print(f"id          :{self['id']}")
        print(f"password    :{self['password']}")
        print(f"Cash        :{self['cash']}\n")
        time.sleep(5)

    @staticmethod
    def write_data(data):
        try:
            with open("accounts.json", 'r+') as f:
                file = json.load(f)
                file.append(data)
                f.seek(0)
                json.dump(file, f, indent=4)
        except:
            with open('accounts.json', 'w') as f:
                fdata = [data]
                json.dump(fdata, f, indent=4)

    @staticmethod
    def info_verification():
        no_user_switch = False
        while True:
            id = int(input("Enter your Id:"))
            password = input("Enter Your Password: ")
            with open('accounts.json', 'r') as f:
                file = json.load(f)
                for obj in file:
                    if obj['id'] == id and obj['password'] == password:
                        no_user_switch = False
                        return obj
                    else:
                        no_user_switch = True
                if no_user_switch:
                    print("Incorrect Info! Please check again")
                    f.seek(0)

    def del_acc(self):
        with open('accounts.json', 'r+') as f:
            file = json.load(f)
            for obj in file:
                if self == obj:
                    file.remove(obj)
                    break
                else:
                    pass
            f.seek(0)
            json.dump(file, f, indent=4)
            f.truncate()


# ___----____--__--___Functionality Class Starts here!__---__---__--__---_---_---__----
class Functionality(User):
    def deposit(self, dep_cash):
        confirm = False
        with open('accounts.json', 'r+') as f:
            file = json.load(f)
            for item in file:
                if item == self:
                    item['cash'] += dep_cash
                    confirm = True
                    break
                else:
                    confirm = False
            if confirm:
                f.seek(0)
                json.dump(file, f, indent=4)
                f.truncate()
                return True

    def withdraw(self, with_cash):
        error = False
        confirm = False
        with open('accounts.json', 'r+') as f:
            file = json.load(f)
            for item in file:
                if item == self and item['cash'] >= with_cash:
                    item['cash'] -= with_cash
                    error = False
                    confirm = True
                    break
                else:
                    error = True
                    confirm = False
            if error:
                print("\nIncorrect Info! Try Again\n")
            if confirm:
                f.seek(0)
                json.dump(file, f, indent=4)
                f.truncate()
                return True


# _-_-___------___--__--__--__--___--___--__--___---_--___--___---__--___--___--__--___
def id_generator():
    try:
        confirm: bool = False
        while True:
            id = random.randint(1000, 9999)
            with open('accounts.json', 'r') as f:
                file = json.load(f)
                for inp in file:
                    if id == inp:
                        confirm = False
                        break
                    else:
                        confirm = True
                if confirm:
                    return id
    except:
        id = random.randint(1000, 9999)
        return id


def get_info():
    name: str = input("Enter Your name: ")
    father_name: str = input("Enter Your fathers' name: ")
    id = id_generator()
    password: str = pass_check()
    cash: int = int(input("Enter initial cash: "))
    return {'name': name,
            'father_name': father_name,
            'id': id,
            'password': password,
            'cash': cash
            }


def pass_check():
    pattern = re.compile("(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*:;.,><|/?_=+])(?=.*[0-9]).+")
    while True:
        password = input("Enter Password: ")
        ok = re.search(pattern, password)
        if len(password) >= 8:
            if ok:
                print("\nPassword accepted\n")
                return password
            else:
                print("\nPassword should contain at least:\n1 special character\n1 number!\n1 uppercase letter\n"
                    "1 lowercase letter")
        else:
            print("\nPassword length less then 8 characters\n")


def choice():
    ch = int(input("choose: "))
    return ch


def receiver():
    no_user = False
    while True:
        user = int(input("Enter receiver id: "))
        with open('accounts.json', 'r') as f:
            file = json.load(f)
            for item in file:
                if item['id'] == user:
                    no_user = False
                    return item
                else:
                    no_user = True
            if no_user:
                print("\nIncorrect Info! try Again\n")


# ____________Main Functionality Functions here_-_--_____
def cr_acc():
    allData = get_info()
    user = User(name=allData['name'],
                father_name=allData['father_name'],
                id=allData['id'],
                password=allData['password'],
                cash=allData['cash'])
    user.write_data(allData)
    print("\nAccount created Successfully!\n\n")
    User.show_info(allData)


def del_acc():
    user = User.info_verification()
    User.del_acc(user)
    print("Account Deleted Successfully!\n")
    time.sleep(3)


def show_user_data():
    user = User.info_verification()
    User.show_info(user)


def deposit():
    user = Functionality.info_verification()
    dep_cash = int(input("Enter amount to Deposit: "))
    confirm = Functionality.deposit(user, dep_cash)
    if confirm:
        print('Deposit Successful!')
        time.sleep(2)
    else:
        print('Error Happened')


def withdraw():
    user = Functionality.info_verification()
    with_cash = int(input("Enter Amount to withdraw: "))
    confirm = Functionality.withdraw(user, with_cash)
    if confirm:
        print('Withdraw Successful!')
        time.sleep(2)
    else:
        print('Error Happened')


def transfer():
    user = Functionality.info_verification()
    rec = receiver()
    with_cash = int(input("Enter Amount to Transfer: "))
    confirm = Functionality.withdraw(user, with_cash)
    if confirm:
        Functionality.deposit(rec, with_cash)
        print("\nTransfer Successful!\n")
        time.sleep(2)
    else:
        print("Error Happened!")


# ---___--__---_---__--___MAIN___---___--__--__--__--___-___-

if __name__ == '__main__':
    main_switch = True
    while main_switch:
        User.menu()
        inp = choice()
        if inp == 0:
            break
        elif inp == 1:
            cr_acc()
        elif inp == 2:
            del_acc()
        if inp == 3:
            # Deposit
            deposit()
        elif inp == 4:
            # Withdraw
            withdraw()
        elif inp == 5:
            # Transfer
            transfer()
        if inp == 6:
            # Show Account
            show_user_data()
