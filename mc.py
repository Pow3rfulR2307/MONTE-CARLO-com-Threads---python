from sympy import symbols, integrate
from random import random
from time import time
import threading


class NovaThread(threading.Thread):

  def __init__(self, chave, dict_funcoes):

    super().__init__()
    self.chave = chave
    self.c = 0
    self.QUANT_PONTOS = 1000000
    self.dict_funcoes = dict_funcoes

  def run(self):

    global trava, barreira, estimativa_final

    for func in self.dict_funcoes:

      inicio = time()
      self.c = calcular_pontos(self.QUANT_PONTOS, self.chave)
      func(self.c, self.QUANT_PONTOS, self.chave, self.dict_funcoes[func])
      final = time()

      trava.acquire()
      self.dict_funcoes[func]["tempo"] += final - inicio
      trava.release()

      barreira.wait()
      estimativa_final = 0.0

def usar_lock(c, QUANT_PONTOS, chave, func):

  global trava
  with trava:
    print(f"---{chave} USANDO LOCK---")
    func["ef"] += c/QUANT_PONTOS

def usar_conditions(c, QUANT_PONTOS, chave, func):

  global condicao, threads_finalizadas

  with condicao:
    print(f"---{chave} USANDO CONDITION---")
    threads_finalizadas+=1
    if threads_finalizadas == NUMERO_THREADS:
      condicao.notify_all()
    else:
      condicao.wait()
    func["ef"] += c/QUANT_PONTOS


def usar_barrier(c, QUANT_PONTOS, chave, func):

  global barreira

  barreira.wait()
  print(f"---{chave} USANDO BARRIER---")
  func["ef"] += c/QUANT_PONTOS

def usar_semaphore(c, QUANT_PONTOS, chave, func):

  global semaforo
  with semaforo:
    print(f"---{chave} USANDO SEMÁFORO---")
    func["ef"] +=c/QUANT_PONTOS

def calcular_pontos(QUANT_PONTOS, chave):

  c = 0
  for i in range(int(QUANT_PONTOS/NUMERO_THREADS)):
    ponto_x = random()
    ponto_y = random()

    if ponto_y < (ponto_x**2):
      c+=1
  return c


if __name__=="__main__":

  NUMERO_THREADS = 30

  threads_finalizadas = 0

  x = symbols("x")

  trava = threading.Lock()
  barreira = threading.Barrier(NUMERO_THREADS)
  condicao = threading.Condition()
  semaforo = threading.Semaphore(NUMERO_THREADS)

  funcoes = {
        usar_lock: {'tempo': 0.0, 'ef': 0.0},
        usar_conditions: {'tempo': 0.0, 'ef': 0.0},
        usar_barrier: {'tempo': 0.0, 'ef': 0.0},
        usar_semaphore: {'tempo': 0.0, 'ef': 0.0}
    }

  integral_fixa = integrate(x**2,(x, 0, 1))

  threads = []
  for i in range(NUMERO_THREADS):

    thread = NovaThread(f"Thread{i+1}", funcoes)
    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

  print(f"\nA ÁREA COM A INTEGRAL DA FUNÇÃO É: {integral_fixa}")
  for func, dados in funcoes.items():
    print(f"FUNÇÃO: {func.__name__} --- TEMPO: {dados['tempo']} SEGUNDOS --- ESTIMATIVA : {dados['ef']}")