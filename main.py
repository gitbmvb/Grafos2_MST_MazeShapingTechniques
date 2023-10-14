import pygame, sys
from celula import *
from botao import Botao
from time import sleep
from queue import Queue

pygame.font.init()
pygame.display.init()
pygame.mixer.init()

## GRID
WIDTH, HEIGHT = 1280, 720
TILE = 40
colunas, linhas = WIDTH // TILE, HEIGHT // TILE
matriz_celulas = [Celula(coluna, linha) for linha in range(linhas) for coluna in range(colunas)]

tela = pygame.display.set_mode((WIDTH + 300, HEIGHT))
pygame.display.set_caption("MazeShapingTechniques - Menu Principal")

## TAXA DE ATUALIZAÇÃO
FPS = 100
clock = pygame.time.Clock()


fundo_menu = pygame.image.load("assets/fundo_menu.png")

## FUNDO MUSICAL
music_files = ["assets/soundtrack.mp3"]
pygame.mixer.music.load(music_files[0])
# pygame.mixer.music.play()


def get_fonte(tamanho):
    return pygame.font.Font("assets/font.ttf", tamanho)


def menu_principal():
    while True:
        tela.blit(fundo_menu, (0, 0))

        posicao_mouse = pygame.mouse.get_pos()

        texto_menu = get_fonte(70).render("MazeShapingTechniques", True, "#ffffff")
        rect_menu = texto_menu.get_rect(center=(790, 75))

        botao_play = Botao(fundo=None, posicao=(790, 300), texto_base="JOGAR", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")
        botao_opcoes = Botao(fundo=None, posicao=(790, 450), texto_base="OPÇÕES", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")
        botao_sair = Botao(fundo=None, posicao=(790, 600), texto_base="SAIR", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")

        tela.blit(texto_menu, rect_menu)

        for botao in [botao_play, botao_opcoes, botao_sair]:
            botao.mudarCor(posicao_mouse)
            botao.atualizar(tela)

        opcao_escolhida = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_play.checarEntrada(posicao_mouse):
                    opcao_escolhida = 0
                    return opcao_escolhida
                if botao_opcoes.checarEntrada(posicao_mouse):
                    opcao_escolhida = 1
                    return opcao_escolhida
                if botao_sair.checarEntrada(posicao_mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def menu_algoritmo():
    while True:
        tela.blit(fundo_menu, (0, 0))

        posicao_mouse = pygame.mouse.get_pos()

        texto_menu = get_fonte(40).render("Selecione o algoritmo", True, "#ffffff")
        rect_menu = texto_menu.get_rect(center=(790, 75))

        botao_kruskal = Botao(fundo=None, posicao=(790, 300), texto_base="KRUSKAL", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")
        botao_prim = Botao(fundo=None, posicao=(790, 450), texto_base="PRIM", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")
        botao_dfs = Botao(fundo=None, posicao=(790, 600), texto_base="DFS", fonte=get_fonte(75), cor_base="#e3e3e3", cor_selecao="#ffffff")

        tela.blit(texto_menu, rect_menu)

        for botao in [botao_kruskal, botao_prim, botao_dfs]:
            botao.mudarCor(posicao_mouse)
            botao.atualizar(tela)

        algoritmo_escolhido = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_kruskal.checarEntrada(posicao_mouse):
                    algoritmo_escolhido = 0
                    return algoritmo_escolhido
                if botao_prim.checarEntrada(posicao_mouse):
                    algoritmo_escolhido = 1
                    return algoritmo_escolhido
                if botao_dfs.checarEntrada(posicao_mouse):
                    algoritmo_escolhido = 2
                    return algoritmo_escolhido
                
        pygame.display.update()

def gerar_labirinto(algoritmo):
    ready = False
    contador = 0
    celula_atual = matriz_celulas[0]
    pilha = []

    union = {celula: [celula] for celula in matriz_celulas}
    while not ready:
        # tela.blit(fundo_menu, (0, 0))
        # texto_menu = get_fonte(40).render("Gerando labirinto...({:-.2f}%)".format((contador * 100)/(colunas*linhas)), True, "#ffffff")
        # rect_menu = texto_menu.get_rect(center=(790, 360))
        # tela.blit(texto_menu, rect_menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        [celula.desenhar(tela, cor="white", TILE=TILE) for celula in matriz_celulas]
        if algoritmo == 0:
            if contador >= linhas * colunas - 1: ready = True
            celula_atual = choice(matriz_celulas)
            celula_atual.visitada = True
            proxima_celula = celula_atual.checar_vizinhos(matriz_celulas, linhas, colunas, estrito=False)
            if proxima_celula:
                proxima_celula.visitada = True
                remove_paredes(celula_atual, proxima_celula)
    
                contador += 1

        elif algoritmo == 1:
            if contador >= linhas * colunas - 1: ready = True
            celula_atual.visitada = True
            proxima_celula = celula_atual.checar_vizinhos(matriz_celulas, linhas, colunas)
            if proxima_celula:
                proxima_celula.visitada = True
                remove_paredes(celula_atual, proxima_celula)
                pilha.append(celula_atual)
                celula_atual = proxima_celula
                contador += 1
            elif pilha: celula_atual = pilha.pop()

        elif algoritmo == 2:
            pass
        
        pygame.display.update()
        clock.tick(FPS)

def jogar():
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MazeShapingTechniques - Jogo")

    while True:
        tela.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        [celula.desenhar(tela, cor="white", TILE=TILE) for celula in matriz_celulas]
        pygame.display.update()
        clock.tick(FPS)
        

if __name__ == "__main__":
    opcao_escolhida = menu_principal()
    if opcao_escolhida == 0:
        algoritmo = menu_algoritmo()
        gerar_labirinto(algoritmo)
        jogar()
    elif opcao_escolhida == 1:
        pygame.quit()
        sys.exit()