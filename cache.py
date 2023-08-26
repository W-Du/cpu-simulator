from memory import Memory, MainMemory
from random import randint
from datetime import datetime
import math

class Cache(Memory):
    def __init__(self, entryNum=4, sets=1):
        Memory.__init__(self, name='cache', access_time=0.5)
        self.data = [
            {'tag': None, 'data':''} for i in range(entryNum)
        ]
        self.main_memory = MainMemory(blockNum = entryNum * 4)
        self.RP = ReplacePolicy(entryNum, sets)
        self.replace_policy = self.RP.get_policy('fifo')
        self.write_through = True
    
    def set_replace_policy(self, pStr):
        self.replace_policy = self.RP.get_policy(pStr)

    def set_write_policy(self, pStr):
        if 'throught' in pStr:
            self.write_through = True
            print("setting write policy to write-through")
        elif 'back' in pStr:
            self.write_through = False
            print('setting write policy to write-back')

    def set_associativity(self, sets):
        if not isinstance(sets, int) or sets > len(self.data) or len(self.data) % sets != 0:
            raise Exception("Illegal number of sets")
        self.RP.sets = sets

    def get_entry(self, address):
        for entry in self.data:
            if entry['tag'] == address:
                print('HIT ', end='')
                return entry
        else:
            print('MISS ', end='')
            return None
    
    def read(self, address):
        super().read()
        entry = self.get_entry(address)
        if entry:
            data = entry['data']
            self.update_lru(entry, address)
        else:
            data = self.main_memory.read(address)
            self.replace_entry(address, data) 
        print(data) 
        return data

    def replace_entry(self, address, data):
        set_number = 0
        if self.RP.sets > 1:
            set_number = address % self.RP.sets
        index = self.replace_policy(set_number)
        print('index', index, end=' - ')
        ori_data = self.data[index]['data']
        new_entry = {'tag': address, 'data': data}
        self.data[index] = new_entry
        print(data)
        if self.write_through:
            self.main_memory.write(address, data)
        elif ori_data is None:
            pass
        elif not self.write_through and ori_data != data:
            self.main_memory.write(address, ori_data)
            
        
    def write(self, address, data):
        super().write()
        entry = self.get_entry(address)
        if entry:
            self.update_lru(entry, address)
            entry['data'] = data
            ori_data = entry['data']
            print(data)
            if self.write_through:
                self.main_memory.write(address, data)
            elif not self.write_through and ori_data and ori_data != data:
                self.main_memory.write(address, ori_data)
        else:
            self.replace_entry(address, data)
        

    def update_lru(self, entry, address):
        if self.RP.name != 'lru':
            pass
        index = self.data.index(entry)
        row = int(index / (self.RP.size / self.RP.sets))
        col = int(index % (self.RP.size / self.RP.sets))
        self.RP.access_contrl[row][col] = datetime.now() 

    def get_exec_time(self):
        return self.exec_time + self.main_memory.exec_time


class ReplacePolicy:
    def __init__(self, size, sets):
        self.size = size
        self.access_contrl = [[datetime.now()] * int(size/sets)] * sets
        self.name = ''
        self.sets = sets
        self.indexes = self.init_indexes()
    
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

    def init_indexes(self):
        n_way = int(self.size / self.sets)
        indexes = [i * n_way for i in range(self.sets)]
        return indexes 

    def get_name(self):
        return self.name

    # get next index
    def fifo(self, set_number):
        index = self.indexes[set_number]
        nextIdx = index + 1
        if self.sets == 1:
            nextIdx %= self.size
        elif nextIdx >= self.size / self.sets * (set_number + 1):
            nextIdx = int(set_number * (self.size / self.sets))
        self.indexes[set_number] = nextIdx
        return index
    
    def rand(self, set_number):
        start = self.indexes[set_number]
        index = randint(start, start + self.sets - 1)
        return index

    def lru(self, set_number):
        row = self.access_contrl[set_number]
        col = row.index(min(row))
        self.access_contrl[set_number][col] = datetime.now()
        least_use_index = set_number * self.sets + col
        return least_use_index

    def __repr__(self):
        ans = [0] * self.size
        c = []
        for row in self.access_contrl:
            c += row
        timeCopy = [t.timestamp() for t in c]
        cur = 0
        for i in range(self.size):
            minIdx = timeCopy.index(min(timeCopy))
            ans[minIdx] = cur
            timeCopy[minIdx] = math.inf
            cur += 1
        res = 'Policy: '+ self.name + '\n' + 'Access time: ' + str(ans)
        return res

