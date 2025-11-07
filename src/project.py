import pygame
import random
import time


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sandwich Stacker")
BG = pygame.image.load("background.png")
clock = pygame.time.Clock()
FOOD_WIDTH = 20
FOOD_HEIGHT = 20
FOOD_VEL = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def move(self,keys):
        if keys[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x + self.speed <= WIDTH:
            self.rect.x += self.speed


    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Food(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 3
    def update(self):
        self.rect.y += self.vel
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def is_offscreen(self):
        return self.rect.y > HEIGHT

def main():
    pygame.init()

    player = Player("player.png", 350, 425)

    food_add_increment = 2000
    food_count = 0
    foods = []
    score = 0

    run = True
    while run:
        food_count += clock.tick(60)

        if food_count > food_add_increment:
            for _ in range(3):
                food_x = random.randint(0, WIDTH - FOOD_WIDTH)
                food_type = ["donut.png", "toast.png", "cupcake.png", "croissant.png"]
                food_image = random.choice(food_type)
                food = Food(food_image, food_x, -20)
                foods.append(food)
            
            food_add_increment = max(30, food_add_increment - 5)
            food_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        keys = pygame.key.get_pressed()
        player.move(keys)


        for food in foods[:]:
            food.update()

            if food.is_offscreen():
                foods.remove(food)
            elif food.rect.colliderect(player.rect):
                foods.remove(food)
                hit = True
                score += 1
                print(f"score: {score}")
                break

        WIN.blit(BG, (0,0))
        player.draw(WIN)  

        for food in foods:
            food.draw(WIN)  

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()