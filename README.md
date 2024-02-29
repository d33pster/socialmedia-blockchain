# <p align='center'>Social Media Using Block Chain</p>
<p align='center'>:made by d33pster:</p>
<p align='center'>
    <a href='#Commands'>Commands</a>
</p>

#### About
This project implements basic social media functionalities through blockchain, which means the data is stored in blocks and every action is registered as a transaction which can be seen by anyone (de-centralized).

#### Usage
```console
## git clone the repository
$ git clone https://github.com/d33pster/socialmedia-blockchain.git

## move into the directory
$ cd socialmedia-blockchain
```
###### On UNIX/LINUX based systems
```console
## install requirements
$ pip install -r requirements.txt

## give permission to main.py and run it
$ chmod a+x ./main.py
$ ./main.py
```
###### On Windows
```console
## install requirements
$ pip install -r requirements.txt

## run using python (if you get command not found error, install python3)
$ python main.py
```
###### Commands
```console
## command list
$ create user ## create one user

$ create users ## create multiple users (developer option)

$ login ## login as a user

$ logout ## logout current user

$ show user blocks ## show the blockchain containing user info (password not shown)

$ show users ## just show user info

$ show transactions ## show friend request transaction blockchain

$ show friend db ## show global friend list

$ send request to @<userid> ## example: send request to @d33pster

$ accept/reject @<userid> ## accept or reject request

$ exit ## exit

```