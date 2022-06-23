import pygame #biblioteca de games
import os #biblioteca para ingrar arquivos do computador
import random #geração de numeros aleatórios

Tela_largura = 500 #variavel constante com largura da tela
Tela_altura = 800 #variavel constante com altura da tela

#Adicionando imagem as variaveis - utiliza blibioteca OS para carregar imagem.
#pygame.transform.scale2x aumenta a escala para ficar maior.
Imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
Imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))\
Imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
#O passaro possui tres posições com isso adicionamos um array com as 3 imagens.
Imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init() #inicializar a fonte
Fonte_pontos = pygame.font.SysFont('arial', 50) #define a fonte e tamanho para o texto de pontos

#Criação das classes, atributos e métodos.
class Passaro:
    IMGS = Imagens_passaro
    #animações da rotação
    Rotacao_maxima = 25
    Velocidade_rotacao = 20
    Tempo_animacao = 5

    #definir atributos
    def __init__(self, x, y): #função inicial, e seus atributos
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem= self.IMGS[0]

    def pular(self): #função pular
        self.velocidade = -10,5 #vai pular
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo   #formula usada para calcular S = so + vot + at²/2

        #Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento<0:
            deslocamento -= 2  #aumenta o tamanho do pulo
        self.y += deslocamento

        #o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.Rotacao_maxima:
                self.angulo = self.Rotacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.Velocidade_rotacao

    def desenhar(self, tela):
        #define qual imagen do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.Tempo_animacao:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.Tempo_animacao*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.Tempo_animacao*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.Tempo_animacao*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.Tempo_animacao*4 +1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Se o passaro estiver caindo nao vai bater asas
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.Tempo_animacao*2

        #Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

        #aplica mascara de pixel na imagem do passado, onde se em um pixel ficar passaro e cano no mesmo pixel
    def get_mask(self):
        pygame.mask.from_surface(self.imagem)

class Cano:
    Distancia = 200 # distancia entre os canos, variavel constante
    Velocidade = 5 #velocidade q os canos passam

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(Imagem_cano, False, True) #vira oi cano na possição Y
        self.cano_base = Imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get.height()
        self.cano_base = self.altura + self.Distancia

    def mover(self):
        self.x -= self.Velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = Imagem_chao.get.width()
    imagem = Imagem_chao

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.largura






