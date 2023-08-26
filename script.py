from cache import Cache


c = Cache(entryNum=4, sets=1)
c.set_replace_policy('fifo')
c.set_write_policy('back')



# c.write(1, '111')
# c.write(2, '')
# c.read(1)
# print(c.data)
# c.write(3, 'mmm')
# c.write(3, '333')
# c.write(4, '444')
# c.write(5, '555')
# c.write(6, '666')
# c.write(7, '777')
# c.write(8, '888')
# print(c.data)
# print(c.RP)
# print(c.RP.lru())
# print(c.RP)


for i in [1,4,6,2,1,4,7,4,1,4,7,0]:
    c.write(i, str(i))
print(c.get_exec_time())
# print(c.main_memory.get_exec_time())