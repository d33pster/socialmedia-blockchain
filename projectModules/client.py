#!/usr/bin/env python3

import socket

class client:
    def __init__(self):
        self._connectTo = ('0.0.0.0', 8080)
    
    def _connect(self, message: str):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._connectTo)
        self._client.send(str(len(message)).encode())
        if self._client.recv(6).decode()=='gotint':
            self._client.send(message.encode())
            chatsLength = self._client.recv(64).decode()
            if chatsLength:
                chatsLength = int(chatsLength)
                # print(f'chat length: {chatsLength}')
                self._client.send('gotint'.encode())
                chats = self._client.recv(chatsLength).decode()
                self._client.send('gotchat'.encode())
                chats = chats.split('\n')
                count = 1
                print('Server response:')
                for chat in chats:
                    if chat=='' or chat==' ':
                        continue
                    print(f'{count}: {chat}')
                    count += 1
        self._client.close()
        
        return chats
    
    def _refresh(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._connectTo)
        self._client.send('refresh'.encode())
        leng = self._client.recv(64).decode()
        leng = int(leng)
        self._client.send('gotint'.encode())
        chats = self._client.recv(leng).decode()
        self._client.send('gotchat'.encode())
        chats = chats.split('\n')
        count = 1
        print('Server response:')
        for chat in chats:
            if chat=='' or chat==' ':
                continue
            print(f'{count}: {chat}')
            count += 1
        
        self._client.close()
        
        return chats