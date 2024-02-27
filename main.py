#!/usr/bin/env python3

from projectModules.Blockchain import Blockchain, Block
from datetime import datetime
from colorama import init as colorama_init, Fore
from getpass import getpass
from os import system as run

def info(message: str):
    print(Fore.RED, "INFO", Fore.RESET, f" : {message}")

def success(message: str):
    print(Fore.GREEN, "INFO", Fore.RESET, f" : {message}")

def createUser():
    global Users
    currentCount = Users.count
    
    Name = input(Fore.BLUE + "Name: " + Fore.RESET)
    
    userid_check = True
    while(True):
        userid = input(Fore.BLUE + "Choose userid: " + Fore.RESET)
        for block in Users.chain:
            if block.data["Name"] != "Genesis Block":
                if block.data["userid"] == userid:
                    print(Fore.RED, "INFO", Fore.RESET, f" : userid \"{userid}\" already exist.")
                    userid_check = False
                    break
                else:
                    userid_check = True
        
        if userid_check:
           break
    
    password = getpass(Fore.BLUE + "Choose Password: " + Fore.RESET)
    
    new_user_data = {
        "Name":f"{Name.strip()}",
        "userid":f"{userid.strip()}",
        "password":f"{password.strip()}"
    }
    
    Users.add_block(Block(index=currentCount+1, timestamp=datetime.now(), data=new_user_data, previous_hash=""))

def viewUsers():
    global Users
    
    if Users.count == 0:
        print(Fore.RED, "INFO", Fore.RESET, " : No User Found.")
    else:
        for user in Users.chain:
            if user.data["Name"] != "Genesis Block":
                print(Fore.GREEN, f"User Block : {user.index}", Fore.RESET)
                print(Fore.BLACK, "Name", Fore.RESET, f": {user.data['Name']}")
                print(Fore.BLACK, "User ID", Fore.RESET, f": {user.data['userid']}")
                print(Fore.BLACK, "Hash", Fore.RESET, f": {user.hash}")
                print(Fore.BLACK, "Previous Hash", Fore.RESET, f": {user.previous_hash}")

def login(passcheckcount=0):
    global Users, isloggedin, session_userid
    
    if isloggedin:
        print(Fore.RED, "INFO", Fore.RESET, f" : user {session_userid} is currently logged in. Logout to continue.")
    else:
        if Users.count != 0:
            user_to_login = input(Fore.BLUE + "userid: " + Fore.RESET)
            
            userfound = False
            if user_to_login.strip() != "exit":
                for verify in Users.chain:
                    if verify.data["Name"] != "Genesis Block":
                        if verify.data["userid"] == user_to_login.strip():
                            userfound = True
                            password_for_user_to_login = getpass(Fore.BLUE + "password: " + Fore.RESET)
                            if verify.data["password"] == password_for_user_to_login.strip():
                                session_userid = user_to_login.strip()
                                isloggedin = True
                                print(Fore.GREEN, "INFO", Fore.RESET, " : Successfully loggedin.")
                                break
                            else:
                                if passcheckcount == 3:
                                    print(Fore.RED, "INFO", Fore.RESET, " : Login Failed.")
                                else:
                                    passcheckcount += 1
                                    print(Fore.RED, "INFO", Fore.RESET, f" : {3-passcheckcount} Attempts remaining.")
                                    login(passcheckcount)
                        else:
                            userfound = False
                
                if not userfound:
                    info(message=f"{user_to_login} not found.")
                    login()
        elif Users.count == 0:
            info("No Users are present.")

def logout():
    global isloggedin, session_userid
    
    if not isloggedin:
        info(message="No user is currently logged in.")
    else:
        user_just_logged_out = session_userid
        session_userid = ""
        isloggedin = False
        success(message=f"user {user_just_logged_out} logout successful.")

def main():
    global Users
    run("clear")
    print(Fore.MAGENTA, "-> Social BlockChain <-", Fore.RESET)
    while(True):
        user_input = input(Fore.BLACK + "Command: " + Fore.RESET)
        if user_input.strip() == "create user":
            createUser()
        elif user_input.strip() == "show users":
            viewUsers()
        elif user_input.strip() == "login":
            login()
        elif user_input.strip() == "logout":
            logout()
        elif user_input.strip() == "exit":
            exit()
        else:
            info(f"command \"{user_input.strip()}\" not recognised.")

if __name__=="__main__":
    Users = Blockchain()
    Friend_Transaction = Blockchain()
    session_userid = ""
    isloggedin = False
    colorama_init()
    try:
        main()
    except KeyboardInterrupt:
        print("")
        exit()