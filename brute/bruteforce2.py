#!/usr/bin/python
import itertools
import sys
import threading
import multiprocessing
import Queue
import gnupg

#threadLimiter = threading.BoundedSemaphore(value=500)

gpgt = gnupg.GPG()

class MyThread(threading.Thread):
    def __init__(self,passphrase,queue,gpg):
        self.passphrase = passphrase
        self.queue = queue
        self.gpg = gpg
        threading.Thread.__init__(self)
    def run(self):
        if gpgt.decrypt(self.gpg,passphrase=self.passphrase):
           self.queue.put(self.passphrase)

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
  f = open('secure.txt.gpg', 'r')
  gpg = f.read()
  f.close
  q = Queue.Queue()
  for i in bruteforce_char(characters, 3):
      #print i
      if q.empty():
        MyThread(i,q,gpg).start()
      else:
        print('the password is: %s' % q.get())
        sys.exit()

if __name__ == "__main__":
    main()
     
