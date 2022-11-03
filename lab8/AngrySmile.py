import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

circle(screen, (220, 195, 177), (200, 200), 100)
line(screen, (0, 0, 0), [150, 150], [175, 175])
line(screen, (0, 0, 0), [250, 150], [225, 175])

circle(screen, (255, 255, 255), [155, 180], 10)
circle(screen, (255, 255, 255), [245, 180], 10)
circle(screen, (0, 0, 0), [155, 180], 2)
circle(screen, (0, 0, 0), [245, 180], 2)

lines(screen, (0, 0, 0), False, [[200, 200], [170, 230], [240, 230]])

line(screen, (0, 0, 0), [180, 270], [220, 270], width=3)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()