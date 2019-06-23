#!/usr/bin/env python
# coding: utf-8

# In[600]:


import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import time
import sys

# Classe para guardar as informações dos vértices do grafo, mais a frente será acrescentada a ela o atributo de grupo
# de forma que no momento que ela é construída, ainda não se sabe qual grupo o nó pertence
class Node: 

    def __init__(self, _id, x, y):
        self.x = x
        self.y = y
        self._id = _id
        # self.group = group
    
# Classe para guardar as informações dos grupos de vértices do grafo com suas [grupo] respectivas demandas, estas
# inseridas após a criação do objeto
class Group:
    
    def __init__(self, _id, nodes):
        self._id = _id
        self.nodes = nodes
        # self.demand = demand


# Classe que guarda os IDs dos vértices do grafo e as arestas, há também a possibilidade de criar um grafo direcional,
# o qual não é o caso deste problema
class Graph:

    def __init__(self, graph_dict={}):
        if (isinstance(graph_dict, Graph)):
            self.__graph_dict = copy.deepcopy(graph_dict.__graph_dict)
        else:
            self.__graph_dict = graph_dict

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.__generate_edges()

    def add_vertex(self, vertex): # Adiciona um vértice ao grafo caso ele já não exista
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge, bidirectional=True): # Desempacota uma aresta e adiciona os vértices que a compõe ao grafo e chama a função 
        (vertex1, vertex2, cost) = edge            # que insere um arco, caso seja um grafo não-direcionado, insere a volta
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.__add_edge_no_repetition(vertex1, vertex2, cost)
        if bidirectional:
            self.__add_edge_no_repetition(vertex2, vertex1, cost)

    def direct_cost(self, vertex1, vertex2): # Retorna o valor do peso que liga as duas arestas, caso ela não exista, retorna infinito
        list_v1 = self.__graph_dict[vertex1]
        for (v, cost) in list_v1:
            if v == vertex2:
                return cost
        else:
            return float('inf')

    def __add_edge_no_repetition(self, v1, v2, cost): # Insere uma aresta no grafo (não aceita arestas paralelas)
        list_v1 = self.__graph_dict[v1]
        for i, (v, _) in enumerate(list_v1):
            if v == v2:
                list_v1[i] = (v2, cost)
                break
        else:
            list_v1.append((v2, cost))

    def __generate_edges(self): # Monta e retorna as arestas em tuplas do grafo
        edges = []
        for vertex in self.__graph_dict:
            for (neighbour, cost) in self.__graph_dict[vertex]:
                if (neighbour, vertex) not in edges:
                    edges.append((vertex, neighbour, cost))
        return edges

    def __str__(self):
        return 'Vertices: {0}\nEdges: {1}'.format(sorted(self.vertices()), sorted(self.edges()))

# Classe para guardar as informações do veículo: capacidade total, capacidade momentânea, grupos separados para ele (
# usado apenas para o caso da demanda total ser igual a capacidade total do grafo) e o ID.
class Car:
    
    def __init__(self, _id, total_cap):
        self._id = _id
        self.total_cap = total_cap
        self.grupos = []
        self.cur_cap = 0
    
# ================================= EXTRAÇÃO DE DADOS =================================
outputNome = None
inputNome = None

if "-in" in sys.argv:
    inputNome = sys.argv[sys.argv.index("-in") + 1]

if "-out" in sys.argv:
    outputNome = sys.argv[sys.argv.index("-out") + 1]

nomeImagem = None
nomearquivoSol = None

if "-img" in sys.argv:
    nomeImagem = sys.argv[sys.argv.index("-img") + 1]
    
if "-sol" in sys.argv:
    nomearquivoSol = sys.argv[sys.argv.index("-sol") + 1]
    
if inputNome and outputNome:
    arquivoLeitura = open(inputNome,'r')
    arquivoEscrita = open(outputNome, 'a')

flagGroups = False # Sinalizador da seção dos nós pertecentes a um grupo
flagNodes = False # Sinalizador da seção das coordenadas dos nós
flagDemand = False # Sinalizador da seção das demandas dos grupos de vértices
nodes = [] # Vetor de nós
grupos = [] # Vetor de grupos
dimension = None # Número de nós
vehicles = None # Número de veículos
ewt = None # Tipo de peso nas arestas (padrão distância euclidiana)
capacity = None # Capacidade de cada veículo
sets_qtt = None # Quantidade de grupos
set_demands = [] # Demanda de cada grupo[i]

for linha in arquivoLeitura:
    if not ('EOF' in linha):
        if 'DIMENSION' in linha:
            novo = list(linha.split())
            dimension = novo[2]

        if 'VEHICLES' in linha:
            novo = list(linha.split())
            vehicles = int(novo[2])

        if 'SETS' in linha:
            novo = list(linha.split())
            sets_qtt = novo[2]

        if 'EDGE_WEIGHT_TYPE' in linha:
            novo = list(linha.split())
            ewt = novo[2]

        if 'CAPACITY' in linha:
            novo = list(linha.split())
            capacity = int(novo[2])

        if (flagDemand):
            novo = list(map(int, linha.split()))
            grupos[novo[0] - 1].demand = novo[1]
            set_demands.append(int(novo[1]))

        if 'DEMAND_SECTION' in linha:
            flagGroups = False
            flagDemand = True

        if(flagGroups): #criando grupos de nós e salvando
            novo = list(map(int, linha.split()))
            grupo = []
            id_aux = None
            for i in range(len(novo)):
                if i == 0:
                    id_aux = novo[i]
                else:
                    if novo[i] != -1:
                        grupo.append(novo[i])
                
            x = Group (novo[0], grupo) # novo[0] = 'id' 
            grupos.append(x)

        if 'SET_SECTION' in linha:
            flagNodes = False
            flagGroups = True

        if(flagNodes): #criando nós e salvando 
            novo = list(map(int, linha.split()))
            x = Node(novo[0], novo[1], novo[2])
            nodes.append(x)

        if 'NODE_COORD_SECTION' in linha:
            flagNodes = True
    
# ================================= FIM EXTRAÇÃO DE DADOS =================================

# ================================= PREPARAÇÃO DE DADOS =================================
def euclidian_distance (x1, x2, y1, y2):
    return math.sqrt(((x2-x1) ** 2) + ((y2-y1) ** 2))

def return_group(v, groups):
    group = None
    for c in groups:
        if v in c.nodes:
            group = c
            break
    return group

def retrieve_node_by_id (node_id, nodes):
    for n in nodes:
        if n._id == node_id:
            return n

def total_demand_in_groups (groups):
    total = 0
    for c in groups:
        total = c.demand + total
        
    return total

        
edges = []
g = Graph({})

# Criação das arestas pela distância euclidiana dos vértices
for n in nodes:
    for v in nodes:
        if (n._id != v._id):
            edges.append((n._id, v._id, euclidian_distance(n.x, v.x, n.y, v.y)))
            g.add_edge((n._id, v._id, euclidian_distance(n.x, v.x, n.y, v.y)))

nodes_dict = {} # Dicionário de Nós com {ID : (Coordenada X, Coordenada Y)} para impressão na NetworkX
for n in nodes: # Atualização do dicionário e atribuição de grupos
    nodes_dict.update({n._id : (n.x, n.y)})
    n.group = return_group(n._id, grupos)

# ================================= FIM PREPARAÇÃO DE DADOS =================================


# In[602]:


# ================================= HEURÍSTICA =================================

# Parâmetros: (lista de vértices, lista de arestas, lista de grupos, capacidade atual do veículo, capacidade total)
# Retorno: Aresta (v1, v2, distância) com melhor razão entre demanda e distância (maximiza demanda e minimiza distância)
def closest_vertex_neighbor(vertex, edges, groupList, cur_cap, capacity): 
    closest_cost = (-1)
    closest_edge = None
    v1_group = None
    v2_group = None
    
    temp = cur_cap
    
    for e in edges:
        (v1,v2,cost) = e
        v1_group = return_group(v1, groupList) # Grupos dos vértices da aresta
        v2_group = return_group(v2, groupList)
        
        # Se o vértice v1 possui grupo diferente do v2 e a (demanda do grupo do v2)/(distância (v1,v2)) é maior que a maior já encontrada, guarda este valor e a aresta
        if v1 == vertex._id  and v2_group != None and v1_group != v2_group and (v2_group.demand/cost) > closest_cost:
            if(v2_group.demand + temp <= capacity): # Se a demanda não ultrapassa a capacidade, pega, se sim, continua procurando outra que não
                closest_edge = e
                closest_cost = (v2_group.demand/cost)
                temp = cur_cap + v2_group.demand
                

    return closest_edge

# Parâmetros: (objeto do grafo, lista de arestas, lista de grupos, lista de nós, veículo fazendo o ciclo)
# Retorno: lista de arestas com maior razão (demanda/distância) que formam um ciclo
def nearest_neighbor_tour(G, edges, groupList, nodes, car):
    
    capacity = car.total_cap
    initial_vertex = retrieve_node_by_id(1, nodes) # Começando pelo depósito...
    random_v = initial_vertex
    path = []
    
    cur_cap = 0
    
    # Enquanto houverem arestas (apenas para confirmação, sempre terá arestas se tiverem grupos), grupos a serem visitados,
    # a função Closest_Vertex_Neighbor não retorna None e a capacidade atual do carro é menor que a máxima:
    # - Pegue a aresta que a função retorna
    # - Deleta a aresta do grafo e a contrária (v1 - v2, v2 - v1)
    # - Pega o nó que a aresta liga (v2)
    # - Remove o grupo já visitado da lista de grupos
    # - Atualiza a capacidade
    # - Adiciona a aresta ao caminho
    while edges and groupList and closest_vertex_neighbor(random_v, edges, groupList, cur_cap, capacity) != None and cur_cap <= capacity:
        closest_edge = closest_vertex_neighbor(random_v, edges, groupList, cur_cap, capacity)
        (v1, v2, cost) = closest_edge
        bidirecional = (v2, v1, cost)
        edges.remove(closest_edge)
        edges.remove(bidirecional)
        random_v = retrieve_node_by_id(v2, nodes)
        groupList.remove(random_v.group)
        cur_cap = cur_cap + random_v.group.demand
        path.append((v1,v2,cost))

    # - Adiciona a aresta de retorno ao depósito
    path.append((random_v._id, initial_vertex._id, G.direct_cost(random_v._id, initial_vertex._id)))
    car.cur_cap = cur_cap # Atualiza o atributo do objeto
    return path

# ================================= FIM HEURÍSTICA =================================


# In[586]:


# ================================= PARTIÇÃO DE DEMANDAS PARA CASO ESPECÍFICO =================================

# Parâmetro: sets com os grupos
# Retorno: index do grupo com menor soma de Demanda
def smallest_partition_index(sets):
    rIndex = -1
    smallest = float('inf')
    for s in sets:
        if total_demand_in_groups(s) < smallest:
            smallest = total_demand_in_groups(s)
            rIndex = sets.index(s)
            
    return rIndex
    
# Parâmetros: lista de grupos a serem divididos em k partições
# Retorno: lista com sublista de grupos com a mesma soma de demanda
def find_partition(groups, k):
    
    sets = []
    
    for i in range(k): # Inicializa k partições
        sets.append([])
    
    # Ordena em ordem decrescente os grupos pela demanda e adiciona, nesta ordem, no subgrupo com menor soma
    for n in sorted(groups, key=lambda x: x.demand, reverse=True): 
        index = smallest_partition_index(sets)
        sets[index].append(n)
        
        
    return sets

# ================================= FIM PARTICÃO =================================


# In[597]:


# ================================= IMPRESSÃO PNG DO GRAFO =================================

def print_graph (nodes_dict, cars, file):
    G = nx.Graph()

    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(vehicles)] # Cor aleatória para cada ciclo na solução
    
    for n, coord in nodes_dict.items():
        (x, y) = coord
        G.add_node(n, pos = (x, y))


    for i, c in enumerate(cars):
        for e in c.path:
            G.add_edge(e[0], e[1], weight = e[2])
        nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), c.path, edge_color= color[i])

    nx.draw_networkx_nodes(G, nx.get_node_attributes(G, 'pos'))
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'))
    
    plt.savefig(file)

# ================================= FIM IMPRESSÃO =================================


# In[604]:


# ================================= EXECUÇÃO E PROCESSAMENTO OUTPUT =================================
vehicles_iterator = 0

cars = []
total_demand = 0

final_groups = []

total_demand = total_demand_in_groups (grupos)
    

# Criando os objetos dos veículos
for i in range(vehicles):
    x = Car(i+1, capacity)
    cars.append(x)

time_start = time.perf_counter() # Início da contagem de tempo para a solução


# Verificação de caso para quando a capacidade total é igual a demanda total
if total_demand == vehicles * capacity:
    
    partitions = find_partition(grupos, vehicles)
    
    for v in range(vehicles):
        cars[v].grupos = partitions.pop()
    
# Para cada escolha, um preço, para cada veículo, um ciclo. (EINSTEN, 2019)
# Caso os veículos não possuem grupos designados a si, utilizam a lista de grupos geral.
while vehicles_iterator < vehicles:
    if (cars[vehicles_iterator].grupos):
        cars[vehicles_iterator].path = nearest_neighbor_tour(g, edges, cars[vehicles_iterator].grupos, nodes, cars[vehicles_iterator])
    else:
        cars[vehicles_iterator].path = nearest_neighbor_tour(g, edges, grupos, nodes, cars[vehicles_iterator])
    vehicles_iterator = vehicles_iterator + 1
        
        
time_elapsed = (time.perf_counter() - time_start)
bkv = 0

if nomearquivoSol:
    arquivoSol = open(nomearquivoSol, "w") # Arquivo com os ciclos
    
for c in cars:
    for e in c.path:
        (v1, v2, cost) = e
        bkv = bkv + cost
        if arquivoSol:
            arquivoSol.write(str(v1) + " ")
    if arquivoSol:
        arquivoSol.write("\n")

if arquivoSol:
    arquivoSol.close()
    
if nomeImagem:
    print_graph(nodes_dict, cars, nomeImagem) # Arquivo com a imagem
    
        
if arquivoLeitura and arquivoEscrita: # Arquivos de entrada e saída
    arquivoLeitura.close()
    arquivoEscrita.write(inputNome + " " + str(bkv) + " " + str(math.floor(time_elapsed)) + "\n")
    arquivoEscrita.close()
    
# =================================  FIM EXECUÇÃO =================================


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




