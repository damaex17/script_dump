#!/usr/bin/python
import itertools
import pexpect
import sys
import threading
import Queue

#threadLimiter = threading.BoundedSemaphore(value=500)

class MyThread(threading.Thread):
    def __init__(self,passphrase,queue):
        self.passphrase = passphrase
        self.queue = queue
        threading.Thread.__init__(self)
    def run(self):
        self.p = pexpect.spawn('gpg --passphrase %s -d secure.txt.gpg' % self.passphrase)
        try:
          self.p.expect('failed')
          #self.queue.put('failed')#self.passphrase,'-->Failed')
        except:
          #printself.p.before
          print('the pw is: %s' % self.passphrase)
          self.queue.put(self.passphrase)#self.passphrase,'-->True')

def char_list():
  returner = []
  for i in map(chr, range(97, 123)):
    returner.append(i)
  for i in map(chr, range(65, 91)):
    returner.append(i)
  for i in range(0, 10):
    returner.append(str(i))
  return returner

def bruteforce_char(characters, length):
  return (''.join(candidate)
    for candidate in itertools.chain.from_iterable(itertools.product(characters, repeat=i)
    for i in range(1, length + 1)))

def main():
  characters = char_list()
  q = Queue.Queue()
  for i in bruteforce_char(characters, 3):
      #print i
      if q.empty():
        MyThread(i,q).start()
      else:
        sys.exit()

if __name__ == "__main__":
    main()
     
