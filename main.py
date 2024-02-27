#!/usr/bin/env python3

## Users data = {Name: "", userid: "", password: ""}
## Friend_Transaction data = {Name: "", sentby: "", sentto: ""}

from projectModules.Blockchain import Blockchain, Block
from datetime import datetime
from colorama import init as colorama_init, Fore
from getpass import getpass
from os import system as run

def info(message: str):
    print(Fore.RED, "INFO", Fore.RESET, f" : {message}")

def success(message: str):
    print(Fore.GREEN, "INFO", Fore.RESET, f" : {message}")

def create_multiple_users():
    count = int(input(Fore.BLUE + "Number of users: " + Fore.RESET))
    
    for i in range(count):
        print(Fore.BLACK, f":: User {i+1} ::", Fore.RESET)
        createUser()

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

def viewUsersBlocks():
    global Users
    
    if Users.count == 0:
        print(Fore.RED, "INFO", Fore.RESET, " : No User Found.")
    else:
        for user in Users.chain:
            if user.data["Name"] != "Genesis Block":
                print(Fore.GREEN, f"User Block : {user.index}", Fore.RESET)
                print(Fore.BLACK, "Created", Fore.RESET, f": {user.timestamp}")
                print(Fore.BLACK, "Name", Fore.RESET, f": {user.data['Name']}")
                print(Fore.BLACK, "User ID", Fore.RESET, f": {user.data['userid']}")
                print(Fore.BLACK, "Hash", Fore.RESET, f": {user.hash}")
                print(Fore.BLACK, "Previous Hash", Fore.RESET, f": {user.previous_hash}\n")

def login(passcheckcount=0, userid=""):
    global Users, isloggedin, session_userid
    
    if isloggedin:
        print(Fore.RED, "INFO", Fore.RESET, f" : user {session_userid} is currently logged in. Logout to continue.")
    else:
        if Users.count != 0:
            if userid == "":
                user_to_login = input(Fore.BLUE + "userid: " + Fore.RESET)
            else:
                user_to_login = userid
            
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
                            else:
                                if passcheckcount == 2:
                                    print(Fore.RED, "INFO", Fore.RESET, " : Login Failed.")
                                else:
                                    passcheckcount += 1
                                    print(Fore.RED, "INFO", Fore.RESET, f" : {3-passcheckcount} Attempts remaining.")
                                    login(passcheckcount, user_to_login)
                            break
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

def showUsers():
    global Users, isloggedin, session_userid
    
    if Users.count == 0:
        info("No users found.")
    else:
        for user in Users.chain:
            if user.data["Name"] != "Genesis Block":
                print(Fore.GREEN, f"User {user.index}", Fore.RESET)
                print(Fore.BLACK, "Name", Fore.RESET, f" : {user.data['Name']}")
                print(Fore.BLACK, "UserID", Fore.RESET, f" : {user.data['userid']}\n")

def sendFriendRequest(target: str):
    global Users, Friend_Transactions, isloggedin, session_userid
    
    if not isloggedin:
        info("login required.")
    else:
        # check for user
        checkuser = False
        for user in Users.chain:
            if user.data["Name"] != "Genesis Block":
                if user.data["userid"] == target:
                    checkuser = True
                    break
        if checkuser:
            # check for preexisting request ### NEED FIXING
            data = {
                "Name":"Friend Request",
                "sentby":f"{session_userid}",
                "sentto":f"{target}",
                "accept":""
            }
            
            Friend_Transactions.add_block(Block(index=Friend_Transactions.count+1, timestamp=datetime.now(), data=data, previous_hash=""))
            
            success(f"Friend Request Sent to @{target}.")
        else:
            info(f"user @{target} not found.")

def showRequests():
    global Friend_Transactions, isloggedin, session_userid
    
    if not isloggedin:
        info("login required.")
    else:
        check = False
        requestcount = 0
        for transaction in Friend_Transactions.chain:
            if transaction.data["Name"]!="Genesis Block" and transaction.data["sentto"]==session_userid and transaction.data["accept"]=="":
                for allother in Friend_Transactions.chain:
                    if allother.data["Name"]!="Genesis Block" and allother.index > transaction.index:
                        if allother.data["sentto"] == transaction.data["sentto"]:
                            if allother.data["accept"] == "yes" or allother.data["accept"]=="no":
                                check = True
                                break
                        else:
                            continue
                
                if not check:
                    requestcount += 1
                    info(f"Pending request from {transaction.data['sentby']}")
        
        if requestcount==0:
            info("No requests at this time.")

def handleRequest(target: str, status: bool):
    global Users, Friend_Transactions, Friends, isloggedin, session_userid
    
    if not isloggedin:
        info("login required.")
    else:
        # check if target exists or not
        checkuser = False
        for user in Users.chain:
            if user.data["Name"] != "Genesis Block":
                if user.data["userid"] == target:
                    checkuser = True
                    break
        
        # check if request is pending instead of checking if it exists or not
        checkrequest = False
        for transaction in Friend_Transactions.chain:
            if transaction.data["Name"]!="Genesis Block" and transaction.data["sentby"]==target and transaction.data["sentto"]==session_userid and transaction.data["accept"]=="":
                for allother in Friend_Transactions.chain:
                    if allother.data["Name"]!="Genesis Block" and allother.index > transaction.index and allother.data["sentby"]==target and allother.data["sentto"]==session_userid:
                        if allother.data["accept"]=="yes" or allother.data["accept"]=="no":
                            checkrequest = True
                            break
            checkrequest = False
        
                            
                            
        if checkuser==True and checkrequest==False:
            if status:
                value = "yes"
            else:
                value = "no"
            
            data = {
                "Name":"Friend Request",
                "sentby":f"{target}",
                "sentto":session_userid,
                "accept":value
            }
            
            Friend_Transactions.add_block(Block(Friend_Transactions.count+1, datetime.now(), data, ""))
            success("Request Accepted")

            if status:
                data_for_Friends_Blockchain = {
                    "Name":"Friend Status",
                    "Member1":session_userid,
                    "Member2":target
                }
                
                Friends.add_block(Block(Friends.count+1, datetime.now(), data_for_Friends_Blockchain, ""))
                success(f"You and {target} are now friends.")
        

def main():
    global Users
    run("clear")
    print(Fore.MAGENTA, "-> Social BlockChain <-", Fore.RESET)
    while(True):
        user_input = input(Fore.BLACK + "Command: " + Fore.RESET)
        if user_input.strip() == "create user":
            createUser()
        elif user_input.strip() == "create users":
            create_multiple_users()
        elif user_input.strip() == "show user blocks":
            viewUsersBlocks()
        elif user_input.strip() == "show users":
            showUsers()
        elif user_input.strip() == "login":
            login()
        elif user_input.strip() == "logout":
            logout()
        elif user_input.strip().split("@")[0] == "send request to ":
            sendFriendRequest(user_input.strip().split("@")[1])
        elif user_input.strip() == "show requests":
            showRequests()
        elif user_input.strip().split("@")[0]=="accept " or user_input.strip().split("@")[0]=="reject ":
            if user_input.strip().split("@")[0]=="accept ":
                handleRequest(user_input.strip().split("@")[1], True)
            else:
                handleRequest(user_input.strip().split("@")[1], False)
        elif user_input.strip() == "exit":
            exit()
        else:
            info(f"command \"{user_input.strip()}\" not recognised.")

if __name__=="__main__":
    Users = Blockchain()
    Friend_Transactions = Blockchain()
    Friends = Blockchain()
    session_userid = ""
    isloggedin = False
    colorama_init()
    try:
        main()
    except KeyboardInterrupt:
        print("")
        exit()