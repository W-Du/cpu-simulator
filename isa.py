
class ISA:
    def __init__(self):
        self.registers = [0] * 32
        self.index = 1

    def get_next_rd(self):
        index = self.index
        self.index += 1
        if self.index >= 32:
            self.index = 1
        return index

    def load_from_register(self, address):
        index = int(address, 2)
        value = self.registers[index]
        print(f'loading from register-{index}: value {value}')
        return value

    def store_to_register(self, index, value):
        self.registers[index] = int(value)
        print(f'store value {value} to register-{index}')
        
    def process_numbers(self, rs, rt, rd=None):
        num1 = self.load_from_register(rs)
        num2 = self.load_from_register(rt)
        if not rd or int(rd,2)==0:
            index = self.get_next_rd()
        else:
            index = int(rd,2)
        return num1, num2, index

    def add(self, rs, rt, rd=None):
        num1, num2, index = self.process_numbers(rs, rt, rd)
        value = num1 + num2
        self.store_to_register(index, value)
        
    def substract(self, rs, rt, rd=None):
        num1, num2, index = self.process_numbers(rs, rt, rd)
        value = num1 - num2
        self.store_to_register(index, value)
    
    def multiply(self, rs, rt, rd=None):
        num1, num2, index = self.process_numbers(rs, rt, rd)
        value = num1 * num2
        self.store_to_register(index, value)

    def divide(self, rs, rt, rd=None):
        num1, num2, index = self.process_numbers(rs, rt, rd)
        if num2 == 0:
            raise Exception("Invalide divisor 0")
            return
        value = num1 / num2
        self.store_to_register(index, value)




    def binary_reader(self, b_instruction):
        if len(b_instruction) != 32:
            print('Invalid length of binary instruction')
            return
        opcode = b_instruction[:6]
        rs = b_instruction[6:11]
        rt = b_instruction[11:16]
        rd = b_instruction[16:21]
        func = b_instruction[26:]
        # print(opcode, rs, rt, rd, shamt, func)
        if opcode == '000000':
            rd = b_instruction[16:21]
            if func == '100000':
                return self.add(rs, rt, rd)
            elif func == '100010':
                return self.substract(rs, rt, rd)
            elif func == '011000':
                return self.multiply(rs, rt, rd)
            elif func == '011010':
                return self.divide(rs, rt, rd)
            else:
                raise Exception("Invalid FUNC code")
        elif func == '000000':
            if opcode == '000001':
                store = b_instruction[16:26]
                index = self.get_next_rd()
                value = int(store, 2)
                print('value', value)
                return self.store_to_register(index, value)
            elif opcode == '100001':
                return self.load_from_register(rd)
            
            


            
            


isa = ISA()
isa.binary_reader("00000100000000000000000101000000")
isa.binary_reader("00000100000000000000001010000000")
 
# Adds/Subtracts/Multiplies/Divides 5 and 10 from registers
isa.binary_reader("00000000001000100000000000100000")
isa.binary_reader("00000000001000100000000000100010")
isa.binary_reader("00000000001000100000000000011000")
isa.binary_reader("00000000001000100000000000011010")
 
# Gets the last three calculations
isa.binary_reader("10000100000000000000000000000000")
isa.binary_reader("10000100000000000000000000000000")
isa.binary_reader("10000100000000000000000000000000")