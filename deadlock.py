import logging
from time import sleep
from threading import Thread, Semaphore

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

tenedor1 = Semaphore(1)
tenedor2 = Semaphore(1)

class Filosofo(Thread):
  def __init__(self, tenedorIzquierdo, tenedorDerecho, nombre):
    super().__init__()
    self.tenedorIzquierdo = tenedorIzquierdo
    self.tenedorDerecho = tenedorDerecho
    self.name = nombre

  def run(self):
    self.tenedorIzquierdo.acquire()
    logging.info('Agarré mi tenedor izquierdo')
    # Este sleep va para forzar el deadlock, pero podría ocurrir sin sleep también
    sleep(1) 
    self.tenedorDerecho.acquire()
    logging.info('Agarré mi tenedor derecho')
    logging.info('Morfando...')
    sleep(1)
    self.tenedorDerecho.release()
    logging.info('Dejé mi tenedor derecho')
    self.tenedorIzquierdo.release()
    logging.info('Dejé mi tenedor izquierdo')

marcos = Filosofo(tenedor1, tenedor2, 'Marcos')
juana = Filosofo(tenedor2, tenedor1, 'Juana')

marcos.start()
juana.start()
