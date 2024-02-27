#!/usr/bin/env python3

## Blockchain module

import hashlib
from datetime import datetime

class Block:
    def __init__(self, index: int, timestamp, data: dict, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        datastring = ""
        for key, value in self.data.items():
            datastring += key + ":" + value + ";"
        hashstring = str(self.index) + str(self.timestamp) + str(datastring) + str(self.previous_hash)
        return hashlib.sha256(hashstring.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.count = 0
    
    def create_genesis_block(self):
        return Block(index=0, timestamp=datetime.now(), data={"Name":"Genesis Block"}, previous_hash=0)
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.count += 1
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True