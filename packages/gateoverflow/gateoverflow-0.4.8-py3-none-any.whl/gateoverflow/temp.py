from notifypy import Notify
import threading
import time


class Scheduler:
    def __init__(self):
        self.tasks = []

    def add(self, f, interval):
        try:
            time_in_mins = float(interval)
            res = {}
            res['f'] = f
            res['interval'] = time_in_mins
            self.tasks.append(res)
        except:
            print("time is invalid")


while True:
    a = input(">> ")
    if(a == 'quit'):
        break
