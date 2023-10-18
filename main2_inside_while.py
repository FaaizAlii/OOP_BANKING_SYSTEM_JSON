import random
import json
import time
import re


# -___--___-User Class--create account / Del account / Show info---
class User:

    def get_info(self):
        name: str = input("Enter Your name: ")
        father_name: str = input("Enter Your fathers' name: ")
        id = self.id_generator()
        phone = self.phone_check()
        password: str = self.pass_check()
        cash: int = int(input("Enter initial cash: "))
        return {'name': name,
                'father_name': father_name,
                'id': id,
                'phone_no': phone,
                'password': password,
                'cash': cash
                }

    @staticmethod
    def phone_check():
        confirm = False
        while True:
            phone = int(input("Enter Phone number: "))
            if len(str(phone)) == 12 and str(phone).startswith("92"):
                try:
                    with open('accounts.json', 'r') as f:
                        file = json.load(f)
                        for item in file:
                            if item['phone_no'] == phone:
                                print("\naccount already registered for provided Phone number!\n")
                                confirm = False
                                break
                            else:
                                confirm = True
                        if confirm:
                            return phone
                except:
                    return phone
            else:
                print("\nInvalid phone number! \nNOTE:Just supports Pakistani networks\n")

    @staticmethod
    def id_generator():
        try:
            confirm: bool = False
            while True:
                id = random.randint(1000, 9999)
                with open('accounts.json', 'r') as f:
                    file = json.load(f)
                for inp in file:
                    if id == inp['id']:
                        confirm = False
                        break
                    else:
                        confirm = True
                if confirm:
                    return id
        except:
            id = random.randint(1000, 9999)
            return id

    @staticmethod
    def pass_check():
        pattern = re.compile("(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*.])(?=.*[0-9])")
        while True:
            password = input("Enter Password: ")
            ok = re.search(pattern, password)
            if len(password) >= 8:
                if ok:
                    return password
                else:
                    print("\nPassword should contain at least:\n1 special character\n1 number!\n1 uppercase letter\n"
                          "1 lowercase letter\n")
            else:
                print("\nPassword length less then 8 characters\n")

    @staticmethod
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

    @staticmethod
    def menu():
        print("1 - Create Account")
        print("2 - Delete Account")
        print("3 - Deposit Money")
        print("4 - Withdraw Money")
        print("5 - Transfer Money")
        print("6 - View An Account Details")
        print("0 - Exit")

    @staticmethod
    def show_info(data):
        print(f"\nname        :{data['name']}")
        print(f"Father name :{data['father_name']}")
        print(f"id          :{data['id']}")
        print(f"password    :{data['password']}")
        print(f"Cash        :{data['cash']}\n")
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

    @staticmethod
    def del_acc(user):
        with open('accounts.json', 'r+') as f:
            file = json.load(f)
            for item in file:
                if user == item:
                    file.remove(item)
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
        with open('accounts.json', 'r+') as f:
            file = json.load(f)
            for item in file:
                if item == self and item['cash'] >= with_cash:
                    item['cash'] -= with_cash
                    error = False
                    break
                else:
                    error = True
            if error:
                print("\nInsufficient cash\n")
            else:
                f.seek(0)
                json.dump(file, f, indent=4)
                f.truncate()
                return True


# ---___--__---_---__--___MAIN___---___--__--__--__--___-___-

if __name__ == '__main__':
    while True:
        User.menu()
        inp = int(input("choose: "))
        if inp == 0:
            break
        elif inp == 1:
            # cr_acc()
            obj = User()
            data = obj.get_info()
            obj.write_data(data)
            obj.show_info(data)
            print("\nAccount Created Successfully!\n")
        elif inp == 2:
            # del_acc()
            obj = User()
            user = obj.info_verification()
            obj.del_acc(user)
            print("\nAccount Deleted Successfully!\n")
        if inp == 3:
            # Deposit
            obj = Functionality()
            user = obj.info_verification()
            cash = int(input("Enter amount to deposit: "))
            if Functionality.deposit(user,cash):
                print("\nCash Deposit Successful\n")
        elif inp == 4:
            # Withdraw
            obj = Functionality()
            user = obj.info_verification()
            cash = int(input("Enter cash to withdraw: "))
            if Functionality.withdraw(user,cash):
                print("\nWithdraw Successful\n")
            # withdraw()
        elif inp == 5:
            # Transfer
            obj = Functionality()
            user = obj.info_verification()
            rec = obj.receiver()
            with_cash = int(input("Enter Amount to Transfer: "))
            confirm = Functionality.withdraw(user, with_cash)
            if confirm:
                Functionality.deposit(rec, with_cash)
                print("\nTransfer Successful!\n")
                time.sleep(2)
            else:
                print("Error Happened!")
        if inp == 6:
            # Show Account
            obj = User()
            user = obj.info_verification()
            obj.show_info(user)
