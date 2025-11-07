import pygame
import random
import time


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sandwich Stacker")
BG = pygame.image.load("background.png")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed = 5

    def move(self,keys):
        if keys[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x + self.speed <= 700:
            self.rect.x += self.speed


    def draw(self, surface):
        surface.blit(self.image, self.rect)

def main():
    pygame.init()

    player_sprite = Player("player.png", 350, 425)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        keys = pygame.key.get_pressed()
        player_sprite.move(keys)

        WIN.blit(BG, (0,0))
        player_sprite.draw(WIN)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()