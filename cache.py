from memory import Memory, MainMemory
from random import randint
from datetime import datetime
import math

class Cache(Memory):
    def __init__(self, entryNum=4):
        Memory.__init__(self, name='cache', access_time=0.5)
        self.data = [
            {'tag': None, 'data':''} for i in range(entryNum)
        ]
        self.main_memory = MainMemory()
        self.RP = ReplacePolicy(entryNum)
        self.replace_policy = self.RP.get_policy('fifo')
        self.associativity = None
        self.write_back = None
    
    def set_replace_policy(self, pStr):
        self.replace_policy = self.RP.get_policy(pStr)

    def set_write_back_policy(self, policy):
        self.write_back = policy

    def set_associativity(self, asso):
        self.associativity = asso

    def get_entry(self, address):
        for entry in self.data:
            if entry['tag'] == address:
                return entry
        return None
    
    def read(self, address):
        super().read()
        entry = self.get_entry(address)
        if entry:
            print('HIT: ', end='')
            data = entry['data']
            self.update_lru(entry)
        else:
            print('MISS: ', end='')
            data = self.main_memory.read(address)
            self.replace_entry(address, data) 
        print(data) 
        return data

    def replace_entry(self, address, data):
        index = self.replace_policy()
        self.data[index] = {'tag': address, 'data': data}
        
    def write(self, address, data):
        super().write()
        entry = self.get_entry(address)
        if entry:
            self.update_lru(entry)
            entry['data'] = data
        else:
            self.replace_entry(address, data)
        print(data)

    def update_lru(self, entry):
        if self.RP.name == 'lru':
            index = self.data.index(entry)
            self.RP.access_contrl[index] = datetime.now() 





class ReplacePolicy:
    def __init__(self, size):
        self.index = 0
        self.size = size
        self.access_contrl = [datetime.now()] * size
        self.name = ''
    
    # return a method
    def get_policy(self, pStr):
        self.name = pStr
        if pStr == 'fifo':
            return self.fifo
        elif pStr == 'random' or pStr == 'rand':
            return self.rand
        elif pStr == 'least recently used' or pStr == 'lru':
            return self.lru
        else:
            raise Exception('No such replace policy')

    def get_name(self):
        return self.name

    # get next index
    def fifo(self):
        index = self.index
        if index >= self.size:
            index %= self.size
        self.index += 1
        return index
    
    def rand(self):
        index = randint(0, self.size-1)
        print(index)
        return index

    def lru(self):
        least_use_index = self.access_contrl.index(min(self.access_contrl))
        self.access_contrl[least_use_index] = datetime.now()
        return least_use_index

    def __repr__(self):
        ans = [0] * self.size
        timeCopy = [t.timestamp() for t in self.access_contrl]
        cur = 0
        for i in range(self.size):
            minIdx = timeCopy.index(min(timeCopy))
            ans[minIdx] = cur
            timeCopy[minIdx] = math.inf
            cur += 1
        res = 'Policy: '+ self.name + '\n' + 'Access time: ' + str(ans)
        return res

        
        


# def convert(arr):
#     ans = [0] * len(arr)
#     copy = arr[:]
#     cur = 0
#     for i in range(len(arr)):
#         minIdx = copy.index(min(copy))
#         print('minIdx', minIdx)
#         ans[minIdx] = cur
#         copy[minIdx] = math.inf
#         cur += 1
#     return ans


# a = [-10, 44, 2,1,6,8]
# print(convert(a))
            

