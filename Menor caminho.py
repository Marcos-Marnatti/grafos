class Graph:
    def __init__(self, is_directed=False):
        self.vertices = []
        self.edges = {}
        self.is_weighted = False
        self.is_directed = is_directed

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        self.edges[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if self.is_directed:
            self.add_directed_edge(vertex1, vertex2, weight)
        else:
            self.add_directed_edge(vertex1, vertex2, weight)
            self.add_directed_edge(vertex2, vertex1, weight)

        if isinstance(weight, (int, float)):
            self.is_weighted = True

    def add_directed_edge(self, from_vertex, to_vertex, weight):
        self.edges[from_vertex].append({"node": to_vertex, "weight": weight})

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            self.vertices.remove(vertex)
            del self.edges[vertex]
            for v in self.edges:
                self.edges[v] = [edge for edge in self.edges[v] if edge["node"] != vertex]

    def remove_edge(self, vertex1, vertex2):
        self.edges[vertex1] = [edge for edge in self.edges[vertex1] if edge["node"] != vertex2]
        if not self.is_directed:
            self.edges[vertex2] = [edge for edge in self.edges[vertex2] if edge["node"] != vertex1]

    def depth_first_search(self, start_vertex, callback):
        visited = set()

        def dfs(vertex):
            if vertex not in visited:
                visited.add(vertex)
                callback(vertex)
                for edge in self.edges[vertex]:
                    dfs(edge["node"])

        dfs(start_vertex)

    def breadth_first_search(self, start_vertex, callback):
        visited = set()
        queue = [start_vertex]
        visited.add(start_vertex)

        while queue:
            vertex = queue.pop(0)
            callback(vertex)
            for edge in self.edges[vertex]:
                if edge["node"] not in visited:
                    visited.add(edge["node"])
                    queue.append(edge["node"])

    def dijkstra(self, start_vertex):
        if not self.is_weighted:
            print('O grafo deve ser ponderado para usar o algoritmo de Dijkstra.')
            return

        if start_vertex not in self.vertices:
            print('O vértice inicial não está presente no grafo.')
            return

        if any(edge["weight"] < 0 for edges in self.edges.values() for edge in edges):
            print('O algoritmo de Dijkstra não funciona com arestas de peso negativo.')
            return

        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0

        visited = set()

        while True:
            min_distance = float('inf')
            closest_vertex = None

            for vertex in self.vertices:
                if vertex not in visited and distances[vertex] < min_distance:
                    min_distance = distances[vertex]
                    closest_vertex = vertex

            if closest_vertex is None:
                break

            for edge in self.edges[closest_vertex]:
                potential = distances[closest_vertex] + edge["weight"]
                if potential < distances[edge["node"]]:
                    distances[edge["node"]] = potential

            visited.add(closest_vertex)

        print(f'Distâncias mínimas a partir de {start_vertex}: {distances}')

    def floyd_warshall(self):
        if not self.is_weighted:
            print('O grafo deve ser ponderado para usar o algoritmo de Floyd-Warshall.')
            return

        distances = {vertex1: {vertex2: 0 if vertex1 == vertex2 else float('inf') for vertex2 in self.vertices}
                     for vertex1 in self.vertices}

        for vertex1 in self.vertices:
            for vertex2 in self.vertices:
                if vertex1 != vertex2:
                    for edge in self.edges[vertex1]:
                        if edge["node"] == vertex2:
                            distances[vertex1][vertex2] = edge["weight"]

        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]

        print('Matriz de distâncias mínimas (Floyd-Warshall):', distances)

    def bellman_ford(self, start_vertex):
        if not self.is_weighted:
            print('O grafo deve ser ponderado para usar o algoritmo de Bellman-Ford.')
            return

        if start_vertex not in self.vertices:
            print('O vértice inicial não está presente no grafo.')
            return

        distances = {vertex: float('inf') for vertex in self.vertices}
        predecessors = {vertex: None for vertex in self.vertices}

        distances[start_vertex] = 0

        for _ in range(len(self.vertices) - 1):
            for vertex1 in self.vertices:
                for edge in self.edges[vertex1]:
                    new_distance = distances[vertex1] + edge["weight"]
                    if new_distance < distances[edge["node"]]:
                        distances[edge["node"]] = new_distance
                        predecessors[edge["node"]] = vertex1

        for vertex1 in self.vertices:
            for edge in self.edges[vertex1]:
                if distances[vertex1] + edge["weight"] < distances[edge["node"]]:
                    print('Há ciclos negativos no grafo!')
                    return

        print('Distâncias mínimas (Bellman-Ford):', distances)
        print('Predecessores (Bellman-Ford):', predecessors)

    def set_directed(self, is_directed):
        self.is_directed = is_directed


graph = Graph()

def add_vertex():
    vertex = input('Digite o nome do vértice: ')
    graph.add_vertex(vertex)
    menu()

def add_edge():
    vertex1 = input('Digite o primeiro vértice: ')
    vertex2 = input('Digite o segundo vértice: ')
    weight = float(input('Digite o peso da aresta: '))
    graph.add_edge(vertex1, vertex2, weight)
    menu()

def remove_vertex():
    vertex = input('Digite o nome do vértice a ser removido: ')
    graph.remove_vertex(vertex)
    menu()

def remove_edge():
    vertex1 = input('Digite o primeiro vértice da aresta a ser removida: ')
    vertex2 = input('Digite o segundo vértice da aresta a ser removida: ')
    graph.remove_edge(vertex1, vertex2)
    menu()

def show_graph():
    print('Vértices:')
    print(graph.vertices)
    print('Arestas:')
    for vertex in graph.edges:
        for edge in graph.edges[vertex]:
            print(f'{vertex} --({edge["weight"]})--> {edge["node"]}')
    menu()

def set_directed_option():
    is_directed = input('O grafo é direcionado? (Sim ou Não): ').lower() == 'sim'
    graph.set_directed(is_directed)
    menu()

def menu():
    print('\nEscolha uma opção:')
    print('    1. Adicionar vértice')
    print('    2. Adicionar aresta')
    print('    3. Remover vértice')
    print('    4. Remover aresta')
    print('    5. Busca em profundidade')
    print('    6. Busca em largura')
    print('    7. Dijkstra')
    print('    8. Floyd-Warshall')
    print('    9. Bellman-Ford')
    print('    10. Mostrar grafo')
    print('    11. Definir se o grafo é direcionado')
    print('    0. Sair')

    option = input('\nDigite o número da opção desejada: ')

    if option == '1':
        add_vertex()
    elif option == '2':
        add_edge()
    elif option == '3':
        remove_vertex()
    elif option == '4':
        remove_edge()
    elif option == '5':
        start_vertex = input('Digite o vértice inicial para a busca em profundidade: ')
        graph.depth_first_search(start_vertex, print)
        menu()
    elif option == '6':
        start_vertex = input('Digite o vértice inicial para a busca em largura: ')
        graph.breadth_first_search(start_vertex, print)
        menu()
    elif option == '7':
        start_vertex = input('Digite o vértice inicial para Dijkstra: ')
        graph.dijkstra(start_vertex)
        menu()
    elif option == '8':
        graph.floyd_warshall()
        menu()
    elif option == '9':
        start_vertex = input('Digite o vértice inicial para Bellman-Ford: ')
        graph.bellman_ford(start_vertex)
        menu()
    elif option == '10':
        show_graph()
    elif option == '11':
        set_directed_option()
    elif option == '0':
        exit()
    else:
        print('Opção inválida. Tente novamente.')
        menu()

if __name__ == "__main__":
    menu()


