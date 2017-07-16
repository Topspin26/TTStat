import datetime
import sys

class Logger:
    def __init__(self, filename=None):
        self.fout = sys.stdout
        if filename:
            self.fout = open('logs/' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + filename,
                             'w', encoding='utf-8')

    def print(self, *args, end='\n'):
        self.fout.write('\t'.join(str(s) for s in args) + end)
