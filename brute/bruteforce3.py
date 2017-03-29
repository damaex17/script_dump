#!/usr/bin/python
import itertools
import sys
import multiprocessing
from multiprocessing import Process, Queue
import gnupg

gpgt = gnupg.GPG()

def work(passphrase,gpg,q):
  if gpgt.decrypt(gpg,passphrase=passphrase):
     q.put(passphrase)

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
  f = open('n26-secure.txt', 'r')
  gpg = f.read()
  f.close
  q = Queue()
  for i in bruteforce_char(characters, 4):
    if q.empty():
      p = Process(target=work, args=(i,gpg,q))
      p.start()
    else:
      print('the password is: %s' % q.get())
      sys.exit()
         

if __name__ == "__main__":
    main()
     
