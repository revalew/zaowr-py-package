from time import sleep
from tqdm import tqdm
from sys import stdout

def blabla():
  tqdm.write("Foo blabla", file=stdout)

for k in tqdm(range(10), file=stdout):
  blabla()
  sleep(.5)