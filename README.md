# trabalhoDeGrafos
Repositório para trabalho da disciplina GCC218 do 1 período de 2019.

##Problema

Considere um conjunto de regiões em uma cidade, compostas por vários pontos de interesse.
A demanda de cada região deve ser atendida por um único ponto que faça parte dela, e cada
ponto pertence a apenas uma região. A situação brevemente descrita nesse contexto está presente na roteirização de embarcações de transporte marítimo, planejamento de atendimento
a pacientes na área da saúde, coleta de lixo urbano, e até em robótica. Sim: é verdade!
Alguns robôs ou veículos autônomos possuem tarefas a serem executadas que exigem a visita
a um único ponto de uma região, para que a transmissão de dados seja feita a outros pontos
via o ponto visitado. Essas regiões podem ser, nesse contexto, áreas com alcance de redes de
sensores sem fio.
O nosso estudo de caso consiste em uma empresa de entregas cujo objetivo é atender a
demanda de cada região pertencente a um conjunto de regiões, cada uma composta por
consumidores, através de exatamente um consumidor da respectiva região. Para tanto, considerando um número limitado de V veículos com capacidade C (cada um), encontre uma
roteirização de cada veículo que saia e retorne do único depósito, e minimize o custo total de
deslocamento entre os consumidores, considerando todos os veículos.

##Tarefas
###Tarefa 1: Extração dos Dados
A partir da descrição do contexto a ser resolvido, o grupo deverá extrair os dados de entrada do problema, identificar parâmetros e construir uma função de leitura dos dados. Os
problemas para teste serão disponibilizados no Campus Virtual.

###Tarefa 2: Implementação de um Algoritmo
Utilizando seus conhecimento em Algoritmos em Grafos, desenvolva um algoritmo que encontre uma solução viável para o problema descrito. Algoritmos de enumeração completa
ou força bruta não serão considerados como resposta.

##Relatório
Um relatório de no máximo 4 páginas (sem incluir a capa) deve ser confeccionado, com as
seguintes informações:
* Introdução: descrição do problema e apresentação das ideias gerais do algoritmo desenvolvido
Algoritmo: apresentação do pseudocódigo implementado e justificar porque essa estratégia foi adotada.
* Testes computacionais: o grupo deverá testar o algoritmo implementado com todas as
instâncias propostas para o trabalho. Para medir a qualidade das soluções, pede-se
que seja calculado o desvio da solução de cada instância i de seu algoritmo (sol[i]) em
relação à melhor solução conhecida de i (bkv[i], presente no arquivo bkv), dado por:

sol[i] − bkv[i]
bkv[i]
× 100 

