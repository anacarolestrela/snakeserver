import pygame
from pygame.locals import *
from random import randint
import time

class Cobra:
    def __init__(self, x, y, cor, controles):
        self.x = x
        self.y = y
        self.cor = cor
        self.controles = controles
        self.velocidade = 10
        self.comprimento = 25
        self.x_controles = 0
        self.y_controles = 0
        self.lista_cobra = []

    def mover(self, largura, altura):
        self.x += self.x_controles
        self.y += self.y_controles

        if self.x > largura:
            self.x = 0
        elif self.x < 0:
            self.x = largura
        if self.y < 0:
            self.y = altura
        elif self.y > altura:
            self.y = 0

        self.lista_cobra.append([self.x, self.y])

        # Verificar colisão com o próprio corpo
        for segmento in self.lista_cobra[:-1]:
            if segmento == [self.x, self.y]:
                return True  # Cobra morta

        if len(self.lista_cobra) > self.comprimento:
            del self.lista_cobra[0]

        return False 
    def aumentar_comprimento(self):
        self.comprimento += 1

    def desenhar(self, tela):
        for posicao in self.lista_cobra:
            pygame.draw.rect(tela, self.cor, (posicao[0], posicao[1], 20, 20))

    def pontuacao(self):
        return len(self.lista_cobra) - 5

class Maca:
    def __init__(self, largura, altura):
        self.x = randint(40, largura - 40)
        self.y = randint(50, altura - 50)

    def reposicionar(self, largura, altura):
        self.x = randint(40, largura - 40)
        self.y = randint(50, altura - 50)

class Jogo:
    def __init__(self, largura, altura):
        pygame.init()

        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("COBRINHA")
        self.relogio = pygame.time.Clock()

        self.cobra_roxa = Cobra(largura // 2, altura // 2 - 25, (128, 0, 128), {'esquerda': K_a, 'direita': K_d, 'cima': K_w, 'baixo': K_s})
        self.cobra_roxa.x_controles = self.cobra_roxa.velocidade  # Definindo movimento inicial para direita
        self.cobra_verde = Cobra(largura // 2, altura // 2 + 25, (0, 128, 0), {'esquerda': K_LEFT, 'direita': K_RIGHT, 'cima': K_UP, 'baixo': K_DOWN})
        self.cobra_verde.x_controles = self.cobra_verde.velocidade  # Definindo movimento inicial para direita

        self.maca = Maca(largura, altura)

        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.load('snakeGame/BoxCat Games - CPU Talk.mp3')
        pygame.mixer.music.play(-1)

        self.colisao_som = pygame.mixer.Sound('snakeGame/smw_coin.wav')
        self.colisao_som.set_volume(1)

        self.pontos_roxa = 0
        self.pontos_verde = 0
        self.morreu = False

        self.tempo_inicial = time.time()
        self.tempo_limite = 10  # Tempo limite em segundos

    def reiniciar(self):
        self.pontos_roxa = 0
        self.pontos_verde = 0
        self.cobra_roxa = Cobra(self.largura // 2, self.altura // 2 - 25, (128, 0, 128), {'esquerda': K_a, 'direita': K_d, 'cima': K_w, 'baixo': K_s})
        self.cobra_verde = Cobra(self.largura // 2, self.altura // 2 + 25, (0, 128, 0), {'esquerda': K_LEFT, 'direita': K_RIGHT, 'cima': K_UP, 'baixo': K_DOWN})
        self.maca.reposicionar(self.largura, self.altura)
        self.morreu = False
        self.tempo_inicial = time.time()

    def executar(self):
        while True:
            self.relogio.tick(30)
            self.tela.fill((255, 255, 255))

            tempo_atual = time.time()
            tempo_decorrido = tempo_atual - self.tempo_inicial

            if tempo_decorrido >= self.tempo_limite:
                # Verificar quem ganhou baseado na pontuação
                if self.cobra_roxa.pontuacao() > self.cobra_verde.pontuacao():
                    vencedor = "Roxa"
                elif self.cobra_roxa.pontuacao() < self.cobra_verde.pontuacao():
                    vencedor = "Verde"
                else:
                    vencedor = None  # Empate

                mensagem = f"Tempo esgotado! Cobra {vencedor} venceu!" if vencedor  else "Empate! Tempo esgotado!"
                fonte = pygame.font.SysFont('arial', 20, True, True)
                texto_formato = fonte.render(mensagem, True, (0, 0, 0))
                ret_texto = texto_formato.get_rect()
                self.tela.blit(texto_formato, (self.largura // 4, self.altura // 2))
                pygame.display.update()
                time.sleep(5)  # Aguarda 2 segundos antes de reiniciar
                self.reiniciar()
                if vencedor:
                    break

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()  
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reiniciar()
                        break

            # Controle das cobras
            for cobra in [self.cobra_roxa, self.cobra_verde]:
                for event, controle in cobra.controles.items():
                    if pygame.key.get_pressed()[controle]:
                        if event == 'esquerda' and cobra.x_controles != cobra.velocidade:
                            cobra.x_controles = -cobra.velocidade
                            cobra.y_controles = 0
                        elif event == 'direita' and cobra.x_controles != -cobra.velocidade:
                            cobra.x_controles = cobra.velocidade
                            cobra.y_controles = 0
                        elif event == 'cima' and cobra.y_controles != cobra.velocidade:
                            cobra.x_controles = 0
                            cobra.y_controles = -cobra.velocidade
                        elif event == 'baixo' and cobra.y_controles != -cobra.velocidade:
                            cobra.x_controles = 0
                            cobra.y_controles = cobra.velocidade

            # Movimento das cobras
            morte_roxa = self.cobra_roxa.mover(self.largura, self.altura)
            morte_verde = self.cobra_verde.mover(self.largura, self.altura)

            # Game over
            if morte_roxa or morte_verde:
                vencedor = None
                if not morte_roxa:
                    vencedor = "Roxa"
                elif not morte_verde:
                    vencedor = "Verde"

                if vencedor:
                    fonte = pygame.font.SysFont('arial', 20, True, True)
                    mensagem1 = f'Parabéns, cobra {vencedor}!'
                    #mensagem2 = 'Pressione a tecla R para jogar novamente'
                else:
                    fonte = pygame.font.SysFont('arial', 20, True, True)
                    mensagem1 = 'Empate!'
                    #mensagem2 = 'Pressione a tecla R para jogar novamente'

                texto_formato1 = fonte.render(mensagem1, True, (0, 0, 0))
               # texto_formato2 = fonte.render(mensagem2, True, (0, 0, 0))
                ret_texto1 = texto_formato1.get_rect()
               # ret_texto2 = texto_formato2.get_rect()
                self.tela.blit(texto_formato1, (self.largura // 4, self.altura // 2))
                #self.tela.blit(texto_formato2, (self.largura // 4, self.altura // 2 + 30))
                pygame.display.update()
                time.sleep(5)
                break

            # Desenhar cobras e maçã
            self.cobra_roxa.desenhar(self.tela)
            self.cobra_verde.desenhar(self.tela)
            pygame.draw.rect(self.tela, (255, 0, 0), (self.maca.x, self.maca.y, 20, 20))

            # Verificar colisões com maçã
            if pygame.Rect(self.maca.x, self.maca.y, 20, 20).colliderect(pygame.Rect(self.cobra_roxa.x, self.cobra_roxa.y, 20, 20)):
                self.maca.reposicionar(self.largura, self.altura)
                self.pontos_roxa += 1
                self.colisao_som.play()
                self.cobra_roxa.aumentar_comprimento()
            elif pygame.Rect(self.maca.x, self.maca.y, 20, 20).colliderect(pygame.Rect(self.cobra_verde.x, self.cobra_verde.y, 20, 20)):
                self.maca.reposicionar(self.largura, self.altura)
                self.pontos_verde += 1
                self.colisao_som.play()
                self.cobra_verde.aumentar_comprimento()

            # Exibir pontuação das cobras
            fonte = pygame.font.SysFont('arial', 20)
            texto_roxo = fonte.render(f'Pontuação Roxa: {self.cobra_roxa.pontuacao()}', True, (128, 0, 128))
            texto_verde = fonte.render(f'Pontuação Verde: {self.cobra_verde.pontuacao()}', True, (0, 128, 0))
            self.tela.blit(texto_roxo, (10, 10))
            self.tela.blit(texto_verde, (10, 30))

            pygame.display.update()


if __name__ == "__main__":
    jogo = Jogo(640, 480)
    jogo.executar()
