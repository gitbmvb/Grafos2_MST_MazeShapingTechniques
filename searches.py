from queue import Queue

def prim(graph, startnode):
    q = Queue()
    q.put((startnode, None))
    visited, next = [], []
    while not q.empty():
        if len(visited) >= len(graph): break
        u = q.get()
        visited.append(u[0])
        next.extend([neigh for neigh in graph[u[0]] if not neigh[0] in visited])
        next.sort(key=lambda x:x[1])
        q.put(next.pop(0))
    print(visited)

graph = {
	"A": [("B", 2), ("C", 3)],
	"B": [("A", 2), ("C", 5), ("E", 4), ("D", 4)],
	"C": [("A", 3), ("B", 5), ("C", 5)],
	"D": [("B", 4), ("E", 2), ("F", 3)],
	"E": [("D", 2), ("F", 5), ("B", 4), ("C", 5)],
	"F": [("D", 3), ("E", 5)],
}
prim(graph, "E")



## Teste algoritmo de kruskal
def jogar(algoritmo: int):
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MazeShapingTechniques - Jogo")
    TILE = 40
    colunas, linhas = WIDTH // TILE, HEIGHT // TILE

    matriz_celulas = [Celula(coluna, linha) for linha in range(linhas) for coluna in range(colunas)]

    labels = [i for i in range(linhas * colunas)]
    while True:
        tela.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        [celula.desenhar(tela, cor="white", TILE=TILE) for celula in matriz_celulas]

        celula_atual = choice(matriz_celulas)
        celula_atual.visitada = True
        proxima_celula = celula_atual.checar_vizinhos(matriz_celulas, linhas, colunas)
        if proxima_celula:
            proxima_celula.visitada = True
            index_atual = matriz_celulas.index(celula_atual)
            index_prox = matriz_celulas.index(proxima_celula)
            remove_paredes(celula_atual, proxima_celula)
            if labels[index_atual] != labels[index_prox]:
                for i in range(len(labels)):
                    if labels[i] == labels[index_prox]:
                        labels[i] = labels[index_atual]
                # print(f"unindo {index_atual} e {index_prox}")
                # labels[index_prox] = index_atual
        # sleep(1)
        print(f"Conjuntos:", len(set(labels)))
        pygame.display.update()
        clock.tick(FPS)