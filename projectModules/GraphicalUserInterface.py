#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from os.path import join, exists as there
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
from datetime import datetime
from projectModules.Blockchain import Blockchain, Block
from projectModules.client import client

# class generate to initialize
class generate:
    def __init__(self, master: Tk, _imagefolder: str):
        ## initialise ##
        # set variables
        self._client = client()
        self._session_userid = ""
        self._isloggedin = False
        self._returntype = ""
        self.users = Blockchain()
        self.posts = Blockchain()
        if there('chat.bak'):
            with open('chat.bak', 'r') as bakfile:
                content = bakfile.readlines()
            
            if len(content)>0:
                for c in content:
                    c = c.replace('\n', '')
                    user = c.split(':')[0][1:]
                    con = c.split(':')[1]
                    data = {
                        'Name':'post',
                        'user':user,
                        'content':con
                    }
                    self.posts.add_block(Block(self.posts.count+1, datetime.now(), data, ''))
        
        self._post_cards = []
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        # get parent window
        self._parent = master
        # set parent window size and posisition
        self._parent.geometry('600x225+500+340')
        # get logo image
        self._logo_image = ImageTk.PhotoImage(Image.open(join(_imagefolder, 'logo.png')))
        # make Enclosing Frame
        self._EnclosingFrame = ttk.Frame(master=self._parent)
        self._EnclosingFrame.pack(fill=BOTH, expand=True)
        ## initialize END ##
        
    
    def _reinitialize(self):
        # destroy all widgets in the Enclosing Frame
        for widget in self._EnclosingFrame.winfo_children():
            widget.destroy()
    
    def _start(self):
        # create a notebook for login/Register
        self._notebook = ttk.Notebook(self._EnclosingFrame)
        self._notebook.pack(fill=BOTH, expand=True)
        
        # create two tabs - login/Register
        self._tab_login = ttk.Frame(self._notebook)
        self._tab_register = ttk.Frame(self._notebook)
        
        # add the tabs in the notebook
        self._notebook.add(self._tab_login, text='login')
        self._notebook.add(self._tab_register, text='register')
        
        # create Enclosing Frames for both the tabs
        self._loginEnclosingFrame = ttk.Frame(self._tab_login)
        self._loginEnclosingFrame.pack(fill=BOTH, expand=True)
        self._registerEnclosingFrame = ttk.Frame(self._tab_register)
        self._registerEnclosingFrame.pack(fill=BOTH, expand=True)
        
        ## login screen ##
        # create a frame for username
        self._login_Frame_one = ttk.Frame(self._loginEnclosingFrame)
        self._login_Frame_one.pack(fill=BOTH, expand=True)
        # create username label
        self._username_label = ttk.Label(self._login_Frame_one, text='username:')
        self._username_label.place(relx=0.3, rely=0.33)
        # create username entry
        self._username_entry = ttk.Entry(self._login_Frame_one, width=20)
        self._username_entry.place(relx=0.45, rely=0.3)
        # create password label
        self._password_label = ttk.Label(self._login_Frame_one, text='password:')
        self._password_label.place(relx=0.3, rely=0.66)
        # create password entry
        self._password_entry = ttk.Entry(self._login_Frame_one, width=20)
        self._password_entry.place(relx=0.45, rely=0.63)
        # create new frame for button
        self._login_Frame_two = ttk.Frame(self._loginEnclosingFrame)
        self._login_Frame_two.pack(fill=BOTH, expand=True)
        # create login button
        self._login_button = ttk.Button(self._login_Frame_two, text='login', default='active', command=self._loginButton)
        self._login_button.place(relx=0.56, rely=0.3, anchor='center')
        # create stringvar for error label
        self._login_error_text = StringVar()
        # create error label
        self._login_error_label = ttk.Label(self._login_Frame_two, textvariable=self._login_error_text)
        self._login_error_label.place(relx=0.56, rely=0.68, anchor='center')
        ## login screen END ##
        
        ## register screen ##
        # create a frame for name, username and password
        self._register_frame_one = ttk.Frame(self._registerEnclosingFrame)
        self._register_frame_one.pack(fill=BOTH, expand=True)
        # create name label
        self._name_label = ttk.Label(self._register_frame_one, text="name:")
        self._name_label.place(relx=0.3, rely=0.03)
        # create name entry
        self._name_entry = ttk.Entry(self._register_frame_one, width=20)
        self._name_entry.place(relx=0.45, rely=0)
        # create username label
        self._username_firsttime_label = ttk.Label(self._register_frame_one, text='username:')
        self._username_firsttime_label.place(relx=0.3, rely=0.36)
        # create username entry
        self._username_firsttime_entry = ttk.Entry(self._register_frame_one, width=20)
        self._username_firsttime_entry.place(relx=0.45, rely=0.33)
        # create password label
        self._password_firsttime_label = ttk.Label(self._register_frame_one, text='password')
        self._password_firsttime_label.place(relx=0.3, rely=0.69)
        # create password entry
        self._password_firsttime_entry = ttk.Entry(self._register_frame_one, width=20)
        self._password_firsttime_entry.place(relx=0.45, rely=0.66)
        # create another frame for button and error label
        self._register_frame_two = ttk.Frame(self._registerEnclosingFrame)
        self._register_frame_two.pack(fill=BOTH, expand=True)
        # create register button
        self._register_button = ttk.Button(self._register_frame_two, text='register', default='active', command=self._registerButton)
        self._register_button.place(relx=0.56, rely=0.3, anchor='center')
        # create a stringvar for register error label
        self._register_error_text = StringVar()
        # create error label for register
        self._register_error_label = ttk.Label(self._register_frame_two, textvariable=self._register_error_text)
        self._register_error_label.place(relx=0.56, rely=0.68, anchor='center')
        ## register screen END ##

    def _loginButton(self):
        # lock register tab
        self._notebook.tab(1, state='disabled')
        # check if textfields are empty
        if self._username_entry.get().strip()=="" and self._password_entry.get().strip()!="":
            self._login_error_text.set("Please enter username.")
            self._notebook.tab(1, state='normal')
        elif self._username_entry.get().strip()!="" and self._password_entry.get().strip()=="":
            self._login_error_text.set("Please enter password.")
            self._notebook.tab(1, state='normal')
        elif self._username_entry.get().strip()=="" and self._password_entry.get().strip()=="":
            self._login_error_text.set("Username and Password cannot be empty.")
            self._notebook.tab(1, state='normal')
        else:
            # check login
            state = False
            if self.users.count>0:
                for block in self.users.chain:
                    if block.data['Name']!="Genesis Block" and self._username_entry.get().strip() == block.data['username']:
                        if self.fernet.decrypt(block.data['password'].encode()) == self._password_entry.get().strip().encode():
                            # set login status true
                            self._isloggedin = True
                            # set session userid
                            self._session_userid = block.data['username']
                            self._notebook.tab(1, state='normal')
                            self._login_error_text.set("login success.")
                            state = True
                            # proceed.
                            self._parent.after(2000, self._proceed)
                        else:
                            self._login_error_text.set("Wrong password. Try again.")
                            # unlock register tab
                            self._notebook.tab(1, state='normal')
                            state = True
                
                if state==False:
                    self._login_error_text.set(f"No user named \'{self._username_entry.get().strip()}\'")
                    
            else:
                self._login_error_text.set("No user currently registered.")
                # unlock register tab
                self._notebook.tab(1, state='normal')
    
    def _registerButton(self):
        # locl login tab
        self._notebook.tab(0, state='disabled')
        # check if textfields are empty
        empty = []
        if self._name_entry.get().strip()=="":
            empty.append('name')
        if self._username_firsttime_entry.get().strip()=="":
            empty.append('username')
        if self._password_firsttime_entry.get().strip()=="":
            empty.append('pass')
        
        if len(empty)==3:
            self._register_error_text.set("Textfields cannot be empty.")
            self._notebook.tab(0, state='normal')
        elif len(empty)==2:
            self._register_error_text.set(f"please enter {empty[0]} and {empty[1]}.")
            self._notebook.tab(0, state='normal')
        elif len(empty)==1:
            self._register_error_text.set(f"please enter {empty[0]}")
            self._notebook.tab(0, state='normal')
        elif len(empty)==0:
            ## register ##
            # check for username already existing
            userid_check = True
            while(True):
                for block in self.users.chain:
                    if block.data['Name']!="Genesis Block" and block.data['username']==self._username_firsttime_entry.get().strip():
                        userid_check = False
                        self._register_error_text.set("Username already exists")
                        break
                    else:
                        userid_check = True
                if userid_check:
                    self._register_error_text.set("")
                    break
            # store user
            userdata = {
                "Name":self._name_entry.get().strip(),
                "username":self._username_firsttime_entry.get().strip(),
                "password":self.fernet.encrypt(self._password_firsttime_entry.get().strip().encode()).decode()
            }
            
            self.users.add_block(Block(self.users.count+1, datetime.now(), userdata, ""))
            self._register_error_text.set("Registered.")
            self._notebook.tab(0, state='normal')
            ## register END ##
    
    def _proceed(self):
        self._reinitialize()
        # at this point user is logged in
        # change window size
        self._parent.geometry("800x800+500+140")
        # go to feed.
        self._setup_feed()
    
    def _setup_feed(self):
        # set a frame for buttons
        self._navigation_frame = ttk.Frame(self._EnclosingFrame)
        self._navigation_frame.pack(fill=BOTH)
        ## create navigation buttons  and labels ##
        # new post button
        self._new_post_button = ttk.Button(self._navigation_frame, text='New Post', default='active', command=self._newpost)
        self._new_post_button.pack(side=LEFT)
        
        self._refbutton = ttk.Button(self._navigation_frame, text='refresh', command=self._refbutton_)
        self._refbutton.pack()
        # create a logout button
        self._logout_button = ttk.Button(self._navigation_frame, text='logout', command=self._logout)
        self._logout_button.pack(side=RIGHT)
        # create loggedin user label in a new frame
        self._loggedin_user_frame = ttk.Frame(self._EnclosingFrame)
        self._loggedin_user_frame.pack(fill=BOTH)
        self._currently_loggedin_label = ttk.Label(self._loggedin_user_frame, text="loggedin: "+self._session_userid)
        self._currently_loggedin_label.pack()
        ## navigation buttons and labels END ##
        # reinit self.post_card
        self._post_cards = []
        # set a frame for scrollbar and posts
        self._post_area = Listbox(self._EnclosingFrame)
        self._post_area.pack(fill=BOTH, expand=True)
        # set up scrollbar
        self._scrollbar = Scrollbar(self._post_area)
        self._scrollbar.pack(side=RIGHT, fill=Y)
        # find posts
        if self.posts.count>0:
            # create posts and store em in a list
            for post in self.posts.chain:
                if post.data['Name']!="Genesis Block":
                    temp = '@' + post.data['user'] + ': ' + post.data['content']
                    self._post_cards.append(temp)

        # display the posts
        if len(self._post_cards)>0:
            for postcard in self._post_cards:
                self._post_area.insert(END, postcard)
        else:
            self._post_error_label = ttk.Label(self._post_area, text='No Posts yet.')
            self._post_error_label.place(relx=0.5, rely=0.5, anchor='center')
        
    
    def _refbutton_(self):
        self.posts = Blockchain()
        chatdata0 = self._client._refresh()
        for chatdata in chatdata0:
            chatdata = chatdata.replace('\n', '')
            if chatdata == '' or chatdata==' ':
                continue
            user = chatdata.split(':')[0]
            user = user[1:]
            content = chatdata.split(':')[1]
            post = {
                "Name":"post",
                "user":user,
                "content":content
            }
            self.posts.add_block(Block(self.posts.count+1, datetime.now(), post, ''))
            self._parent.after(1, self._proceed)
    
    def _newpost(self):
        # reinitialise
        self._reinitialize()
        # change window size
        self._parent.geometry("600x205+500+340")
        # create a frame for input ## ==> later modify it into a notebook to post text/pictures
        self._newpost_EnclosingFrame = ttk.Frame(self._EnclosingFrame)
        self._newpost_EnclosingFrame.pack(fill=BOTH, expand=True)
        # create a frame for label
        self._newpost_frame_one = ttk.Frame(self._newpost_EnclosingFrame)
        self._newpost_frame_one.pack(fill=BOTH)
        # create a label
        self._new_post_label = ttk.Label(self._newpost_frame_one, text="Create a Post:")
        self._new_post_label.pack(side=LEFT)
        # create a frame for textbox
        self._newpost_frame_two = ttk.Frame(self._newpost_EnclosingFrame)
        self._newpost_frame_two.pack(fill=BOTH)
        # create textbox
        self._newpost_textbox = Text(self._newpost_frame_two, blockcursor=True, relief='flat', height=10)
        self._newpost_textbox.pack(fill=BOTH)
        # create a frame for button and status label
        self._newpost_frame_three = ttk.Frame(self._newpost_EnclosingFrame)
        self._newpost_frame_three.pack(fill=BOTH)
        # create a button
        self._post_button = ttk.Button(self._newpost_frame_three, text='post', default='active', command=self._postButton)
        self._post_button.pack(side=LEFT)
        # create a string var for post status label
        self._post_status = StringVar()
        # create a label
        self._post_status_label = ttk.Label(self._newpost_frame_three, textvariable=self._post_status)
        self._post_status_label.pack(side=RIGHT)
    
    def _postButton(self):
        poststr = '@' + self._session_userid + ':' + self._newpost_textbox.get("1.0", END).strip()
        self._chatdata = self._client._connect(poststr)
        self.posts = Blockchain()
        for chatdata in self._chatdata:
            chatdata = chatdata.replace('\n', '')
            if chatdata == '' or chatdata==' ':
                continue
            user = chatdata.split(':')[0]
            user = user[1:]
            content = chatdata.split(':')[1]
            post = {
                "Name":"post",
                "user":user,
                "content":content
            }
            self.posts.add_block(Block(self.posts.count+1, datetime.now(), post, ''))
        self._post_status.set("Posted.")
        self._parent.after(2000, self._proceed)
    
    def _logout(self):
        self._reinitialize()
        self._parent.geometry('600x225+500+340')
        self._session_userid = ""
        self._isloggedin = False
        self._start()