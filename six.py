import datetime
import time

time_start = datetime.datetime.now()
print time_start
# time.sleep(5)

time_end = datetime.datetime.now()
print time_end

zong = time_end - time_start
print zong

print zong.seconds

myd = {'ni':98,'hao':98}
good = [1,2,3,4]
myset = set([1,2,3,4,4])
a = myd.pop('ni')
b = good.pop()

myset.add(4)
print a
print b
print myset