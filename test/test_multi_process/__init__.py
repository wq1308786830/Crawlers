import time
from multiprocessing import Process, cpu_count
import os


# 子进程要执行的代码
def run_proc(name):
    time.sleep(30)
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    print('cpu_count:', cpu_count())
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Process will start.')
    p.start()
    p.join()
    print('Process end.')
