from multiprocessing import Pool
import time
from itertools import repeat
from concurrent.futures import process
import time


def task1(NO):
    print(NO)

def main(test0,test1):
    if 8>test0>3:
        print("OK")
    else:
        print("NG")

start_time=time.time()
test=[i for i in range(10**5)]
with process.ProcessPoolExecutor(max_workers=3) as executor: 
    result=executor.map(task1,test)
end_time=time.time()
print(f'{end_time-start_time}s')