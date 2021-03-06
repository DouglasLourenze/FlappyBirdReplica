import pygame #biblioteca de games
import os #biblioteca para ingrar arquivos do computador
import random #geração de numeros aleatórios

Tela_largura = 500 #variavel constante com largura da tela
Tela_altura = 800 #variavel constante com altura da tela

#Adicionando imagem as variaveis - utiliza blibioteca OS para carregar imagem.
#pygame.transform.scale2x aumenta a escala para ficar maior.
Imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
Imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
Imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
#O passaro possui tres posições com isso adicionamos um array com as 3 imagens.
Imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]
Imagem_fimjogo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bgfim.png')))

pygame.font.init() #inicializar a fonte
Fonte_pontos = pygame.font.Font('fonts/Sunday Morning ttf.ttf', 35) #define a fonte e tamanho para o texto de pontos
Fonte_Msgfinal = pygame.font.Font('fonts/Sunday Morning ttf.ttf', 25)
#Criação das classes, atributos e métodos.
class Passaro:
    IMGS = Imagens_passaro
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(Imagem_cano, False, True)
        self.CANO_BASE = Imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap_area(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap_area(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = Imagem_chao.get_width()
    imagem = Imagem_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0 :
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0 :
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(Imagem_background, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = Fonte_pontos.render(f"Pontos: {pontos}", 1, (255,255,255))
    tela.blit(texto, (Tela_largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def fimdojogo (tela, pontos, chao):
    tela.blit(Imagem_fimjogo, (0,0))

    texto0 = Fonte_Msgfinal.render("VOCÊ TA MORTO!!!!", 1, (255, 255, 255))
    texto0rect = texto0.get_rect()
    texto0rect.center = (Tela_largura // 2, Tela_altura // 10)
    tela.blit(texto0, texto0rect)
    texto = Fonte_Msgfinal.render(f"Pontos marcados: {pontos}", 1, (255,255,255))
    tela.blit(texto, (Tela_largura // 5, 170))
    texto1 = Fonte_Msgfinal.render("DIGITE 'R' PARA REINICIAR", 1, (255,255,255))
    texto1rect = texto1.get_rect()
    texto1rect.center = (Tela_largura // 2, Tela_altura // 2.5)
    tela.blit(texto1, texto1rect)
    texto2 = Fonte_Msgfinal.render("OU CLIQUE NO 'X' PARA SAIR", 1, (255, 255, 255))
    texto2rect = texto2.get_rect()
    texto2rect.center = (Tela_largura //2, Tela_altura //2)
    tela.blit(texto2, texto2rect)
    chao.desenhar(tela)
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
               main()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_x:
               pygame.quit()
               quit()
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((Tela_largura, Tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()


    rodando = True
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    main()

        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > (cano.x + cano.CANO_BASE.get_width()):
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        #for i, passaro in enumerate(passaros):
        if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0 or cano.colidir(passaro):
            #passaros.pop(i)
            #return main()
            acabou = True
            pygame.time.wait(800)
            break

            #main()


        desenhar_tela(tela, passaros, canos, chao, pontos)

    while acabou:
        fimdojogo(tela, pontos, chao)
       # input("Escreva seu nome: ")


if __name__ == '__main__':
    main()

