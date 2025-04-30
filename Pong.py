import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de la pelota
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = 4
ball_speed_y = 4

# Configuración de las paletas
paddle_width, paddle_height = 20, 100
player1 = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
player2 = pygame.Rect(WIDTH - 10 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle_speed = 5

# Puntajes
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

# Función para reiniciar la pelota
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de las paletas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed

    # Movimiento de la pelota
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisiones con la parte superior e inferior
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Colisiones con las paletas
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # Puntos para jugadores
    if ball.left <= 0:
        score2 += 1
        reset_ball()
    if ball.right >= WIDTH:
        score1 += 1
        reset_ball()

    # Dibujar en la pantalla
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Dibujar los puntajes
    text1 = font.render(str(score1), True, WHITE)
    text2 = font.render(str(score2), True, WHITE)
    screen.blit(text1, (WIDTH // 4, 20))
    screen.blit(text2, (WIDTH - WIDTH // 4, 20))

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
