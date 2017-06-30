my_name = "Pygame"
import pygame
import sys
pygame.init()
my_font = pygame.font.SysFont("arial",100)
name_surface=my_font.render(my_name,True,(0,0,0),(255,255,255))
name_rect = name_surface.get_rect()
screen = pygame.display.set_mode((1200,800))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((230,230,230))
    screen.blit(name_surface,name_rect)
    pygame.display.flip()
