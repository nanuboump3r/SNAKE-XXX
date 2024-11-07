import pygame
import random


pygame.init()
pygame.mixer.init()  
screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)  


snake_block = 10
snake_speed = 10
snake_list = []
snake_length = 1


score = 0
level = 1
exp = 0


snake_x, snake_y = screen_width // 2, screen_height // 2
food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0


bonus_food_x, bonus_food_y = None, None
bonus_active = False
bonus_timer = 0


dx, dy = 0, 0


eat_sound = pygame.mixer.Sound(r"snakey\comer.wav")
bonus_sound = pygame.mixer.Sound(r"snakey\bonificacion.wav")
pygame.mixer.music.load(r"snakey\background.mp3") 
pygame.mixer.music.play(-1)  


def display_score_level(score, level, exp):
    score_text = font.render(f"Score: {score}  Level: {level}  Exp: {exp}", True, white)
    screen.blit(score_text, [10, 10])
def draw_progress_bar(exp, level):
    # Dimensiones de la barra de progreso
    bar_width = 200
    bar_height = 20
    bar_x = (screen_width - bar_width) // 2
    bar_y = 30

    # Calcular la longitud de la barra según la experiencia actual
    fill_width = (exp / 10) * bar_width  # Supongamos que se sube de nivel cada 10 puntos de exp

    # Dibujar fondo de la barra
    pygame.draw.rect(screen, (50, 50, 50), [bar_x, bar_y, bar_width, bar_height])
    # Dibujar barra de progreso actual
    pygame.draw.rect(screen, (0, 255, 100), [bar_x, bar_y, fill_width, bar_height])

    # Texto para nivel
    level_text = font.render(f"Nivel: {level}", True, white)
    screen.blit(level_text, [bar_x, bar_y - 25])  # Posición encima de la barra

def display_score_level(score, level, exp):
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])  # Posición del puntaje
    draw_progress_bar(exp, level)  # Llamada a la barra de progreso

def level_up():
    global level, snake_speed, exp
    if exp >= 10:
        level += 1
        snake_speed += 1
        exp = 0


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])


def activate_bonus():
    global bonus_food_x, bonus_food_y, bonus_active, bonus_timer
    if not bonus_active and random.randint(1, 20) == 1: 
        bonus_food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
        bonus_food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
        bonus_active = True
        bonus_timer = 300  


def game_loop():
    global snake_x, snake_y, dx, dy, food_x, food_y, snake_length, score, exp, bonus_active, bonus_timer
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx, dy = -snake_block, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = snake_block, 0
                elif event.key == pygame.K_UP:
                    dx, dy = 0, -snake_block
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, snake_block

        snake_x += dx
        snake_y += dy
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

      
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

      
        if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
            game_over = True

     
        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            snake_length += 1
            score += 10
            exp += 1
            eat_sound.play()
            level_up()

 
        if bonus_active and snake_x == bonus_food_x and snake_y == bonus_food_y:
            score += 50  
            snake_length += 3  
            exp += 5  
            bonus_sound.play()  
            bonus_active = False

       
        if bonus_active:
            bonus_timer -= 1
            if bonus_timer <= 0:
                bonus_active = False  

     
        activate_bonus()

      
        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])
        if bonus_active:
            pygame.draw.rect(screen, blue, [bonus_food_x, bonus_food_y, snake_block, snake_block])  
        draw_snake(snake_block, snake_list)
        display_score_level(score, level, exp)

        pygame.display.update()
        clock.tick(snake_speed)
                    

    pygame.quit()
    quit()

game_loop()
