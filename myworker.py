import queue
from multiprocessing.managers import BaseManager

class QueueManger(BaseManager):
    pass

QueueManger.register('get_list_queue')
QueueManger.register('get_task_queue')
QueueManger.register('get_result_queue')

server_addr='127.0.0.1'
print('Connect to server %s...' %server_addr)
m=QueueManger(address=(server_addr,8888),authkey=b'password')
m.connect()

lists=m.get_list_queue()
lexicon=lists.get(timeout=2)
task=m.get_task_queue()
result=m.get_result_queue()
while True:
    try:
        string=task.get(timeout=1)
        if string in lexicon:
            result.put(True)
            print(string,end=' ')
        else:
            result.put(False)
            if string=='command:worker.close()':
                print('\ndone')
                break
    except queue.Empty:
        print('\ntask queue is empty now.')
        continue
print('worker exit.')