

class Memory:
    def __init__(self, name='', access_time=0):
        self.name = name
        self.access_time = access_time
        self.exec_time = 0
    
    def get_exec_time(self):
        return self.exec_time
    
    def read(self, output=True):
        if output:
            print(f'- {self.name} read ', end='')
        self.exec_time += self.access_time

    def write(self, output=True):
        if output:
            print(f' -{self.name} write ', end='')
        self.exec_time += self.access_time



class MainMemory(Memory):
    def __init__(self, blockNum):
        Memory.__init__(self, 'Main memory', 30)
        self.data = [''] * blockNum
        self.blockNum = blockNum

    def read(self, address):
        data = self.data[address]
        super().read()
        return data
    
    def write(self, address, data):
        self.data[address] = data
        super().write()
        print(data, end = '\n')

