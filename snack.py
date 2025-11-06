import pygame, sys, time
import random

# Inicialização
pygame.init()  # Inicializa todos os módulos Pygame

# Definições de Cores (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
# Uma cor para o alimento, por exemplo, vermelho
food_color = red

# Configurações da Janela
posicao_x = 280
posicao_y = 280
tamanho_bloco = 10  # Tamanho de cada bloco da cobrinha e do alimento
janela_jogo = pygame.display.set_mode((posicao_x, posicao_y))
pygame.display.set_caption('Jogo da Cobrinha')

# Controle de FPS
fps_controller = pygame.time.Clock()
velocidade_jogo = 10  # Velocidade inicial da cobrinha (FPS)

# Posição e Corpo da Cobrinha
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction


# Posição do Alimento
# Gera a posição inicial do alimento de forma aleatória, alinhada com a grade (múltiplos de 10)
def generate_food_pos():
    x = random.randrange(1, (posicao_x // tamanho_bloco)) * tamanho_bloco
    y = random.randrange(1, (posicao_y // tamanho_bloco)) * tamanho_bloco
    return [x, y]


food_pos = generate_food_pos()
food_spawn = True  # Flag para verificar se um novo alimento deve ser gerado


# Função Game Over
def game_over():
    # Isso poderia exibir uma mensagem na tela, mas por enquanto vamos apenas sair.
    print('GAME OVER!')
    pygame.quit()
    sys.exit()


# --- LOOP PRINCIPAL DO JOGO ---
while True:
    # 1. Lógica de Entrada de Comandos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'

    # Evita que a cobrinha volte na direção oposta (ex: de UP para DOWN imediatamente)
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    # 2. Lógica do Movimento da Cobrinha
    if direction == 'UP':
        snake_pos[1] -= tamanho_bloco
    if direction == 'DOWN':
        snake_pos[1] += tamanho_bloco
    if direction == 'LEFT':
        snake_pos[0] -= tamanho_bloco
    if direction == 'RIGHT':
        snake_pos[0] += tamanho_bloco

    # Adiciona um novo segmento à frente (simulando o movimento)
    snake_body.insert(0, list(snake_pos))

    # 3. Lógica de Colisão com o Alimento
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        # Cobrinha comeu o alimento:
        # A flag food_spawn é definida como True para gerar um novo alimento
        food_spawn = True
        # **IMPORTANTE:** O corpo da cobrinha NÃO É encurtado (ela cresce)
    else:
        # Cobrinha não comeu:
        # O último segmento do corpo é removido para dar a ilusão de movimento
        snake_body.pop()

    # 4. Reposicionamento do Alimento
    if food_spawn:
        food_pos = generate_food_pos()
        # Garante que o novo alimento não apareça dentro do corpo da cobrinha
        while food_pos in snake_body:
            food_pos = generate_food_pos()
        food_spawn = False

    # 5. Desenho dos Elementos
    janela_jogo.fill(black)

    # Desenha a Cobrinha
    for pos in snake_body:
        pygame.draw.rect(janela_jogo, green, pygame.Rect(pos[0], pos[1], tamanho_bloco, tamanho_bloco))

    # Desenha o Alimento
    pygame.draw.rect(janela_jogo, food_color, pygame.Rect(food_pos[0], food_pos[1], tamanho_bloco, tamanho_bloco))

    # 6. Condições de Game Over

    # Se bater na borda
    if snake_pos[0] < 0 or snake_pos[0] > posicao_x - tamanho_bloco:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > posicao_y - tamanho_bloco:
        game_over()

    # Se bater em si mesma (verifica se a cabeça está em alguma posição do corpo, excluindo o primeiro elemento que é a própria cabeça)
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # 7. Atualização da Tela e Controle de FPS
    pygame.display.update()
    fps_controller.tick(velocidade_jogo)