# MONTE-CARLO-com-Threds---python
Trabalho do professor Frank de Alcantara de MONTE CARLO em python. O objetivo desse programa é calcular a aproximação da Integral de uma função usando o método de MONTE CARLO com 4 algoritmos de sincronização de threads diferentes, semaphores, locks, barriers e conditions. 

Cada algoritmo é executado após todas as threads concluírem o algoritmo anterior, e então, quando todas as threads tiverem terminado, o programa irá imprimir o tempo de execução de cada uma delas para servir como um benchmark dos métodos mais eficientes. 

Cada thread é parte da classe NovaThread que possui atributos comuns a todas e o método "run", que executa cada uma das funções de sincronização e calcula o tempo levado para o término.
