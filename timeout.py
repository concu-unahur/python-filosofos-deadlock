import logging
from time import sleep
from threading import Thread, Semaphore
from random import randint

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

tenedor1 = Semaphore(1)
tenedor2 = Semaphore(1)

class Filosofo(Thread):
  def __init__(self, tenedorIzquierdo, tenedorDerecho, nombre):
    super().__init__()
    self.tenedorIzquierdo = tenedorIzquierdo
    self.tenedorDerecho = tenedorDerecho
    self.name = nombre
    self.tieneHambre = True # De alguna forma tengo que saber si ya comió

  def run(self):
    # Uso un while porque no sé cuántas veces voy a tener 
    # que intentar agarrar los tenedores hasta que logre comer
    while (self.tieneHambre):
      self.tenedorIzquierdo.acquire()
      logging.info('Agarré mi tenedor izquierdo')
      
      # Este sleep va para forzar el deadlock, pero podría ocurrir sin sleep también
      sleep(1) 

      # Espero un tiempo aleatorio entre 1 y 3, para que no lo suelten a la vez
      agarreElDerecho = self.tenedorDerecho.acquire(timeout=randint(1, 3))
      if (agarreElDerecho):
        logging.info('Agarré mi tenedor derecho')
        logging.info('Morfando...')
        self.tieneHambre = False
        self.tenedorDerecho.release()
        logging.info('Dejé mi tenedor derecho')
        self.tenedorIzquierdo.release()
        logging.info('Dejé mi tenedor izquierdo')
      else:
        logging.info('No pude agarrar el derecho, suelto el izquierdo')
        self.tenedorIzquierdo.release()
        # Le dejo un segundo al otro thread para que pueda agarrar el tenedor
        sleep(1)

marcos = Filosofo(tenedor1, tenedor2, 'Marcos')
juana = Filosofo(tenedor2, tenedor1, 'Juana')

marcos.start()
juana.start()
