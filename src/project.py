import pygame
import random
import time

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitty Cafe Food Catcher")
MENU_BG = pygame.image.load("menu_bg.png")
BG = pygame.image.load("background.png")
clock = pygame.time.Clock()
FOOD_WIDTH = 20
FOOD_HEIGHT = 20
FOOD_VEL = 1

class Button():
    def __init__(self, text, x, y, width, height, font, base_color, hover_color):
        self.text = text
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
    
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 6
        self.caught_food = []
        self.max_stack = 5

    def move(self,keys):
        if keys[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x + self.speed <= WIDTH:
            self.rect.x += self.speed

    def pile_foods(self, food_image):
        if len(self.caught_food) < self.max_stack:
            self.caught_food.append(food_image)
            return True
        return False
    
    def serve_foods(self):
        points = len(self.caught_food)
        self.caught_food = []
        return points

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        stack_y = self.rect.top - 60
        for food_img in self.caught_food:
            surface.blit(food_img, (self.rect.centerx - food_img.get_width()//2, stack_y))
            stack_y -= 60

class Customer:
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Food(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, food_type = "fresh"):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 3
        self.food_type = food_type
    def update(self):
        self.rect.y += self.vel
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def is_offscreen(self):
        return self.rect.y > HEIGHT

def gameover_screen(score):
    font_large = pygame.font.Font("BoldPixels.ttf", 74)
    font_small = pygame.font.Font("BoldPixels.ttf", 36)

    gameover_text = font_large.render("Game over!", True, (200,10,0))
    score_text = font_small.render(f"score: {score}", True, (255,255,255))
    retry_text = font_small.render("Press SPACE to retry", True, (255,255,255))
    quit_text = font_small.render("Press Q to quit", True, (255,255,255))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_SPACE:
                    return True
        WIN.blit(BG, (0,0))
        WIN.blit(BG, (0,0))
        pygame.draw.rect(WIN, (255,105,180), (195,145,610,410))
        pygame.draw.rect(WIN, (255,182,193), (200,150,600,400))
        WIN.blit(gameover_text, (WIDTH//2 - gameover_text.get_width()//2, 200))
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 300))
        WIN.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, 400))
        WIN.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 450))

        pygame.display.flip()
        clock.tick(60)

def main_menu():
    font_title = pygame.font.Font("BoldPixels.ttf",90)
    font_subtitle = pygame.font.Font("BoldPixels.ttf", 30)
    font_instructions = pygame.font.Font("BoldPixels.ttf", 23)


    title_text = font_title.render("Kitty Cafe Food Catcher", True, (255,105,180))
    
    lines = [
        "Move around with the arrow keys and catch falling food!",
        "Catching food will give you points.",
        "Avoid the rotten fish!", 

    ]

    play_button = Button("PLAY", WIDTH//2 - 150, 600, 300, 80, font_subtitle, (255,105,180), (255,182,193))
    quit_button = Button("QUIT", WIDTH//2 - 150, 700, 300, 80, font_subtitle, (255,105,180), (255,182,193))

    while True:
        WIN.blit(MENU_BG, (0,0))
        menu_mouse_pos = pygame.mouse.get_pos()
        WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 200))

        box_y = 300 
        box_height = len(lines) * 40 + 60
        pygame.draw.rect(WIN, (255,105,180), (WIDTH//2 - 305, box_y - 5, 610, box_height + 10))
        pygame.draw.rect(WIN, (255,193,203), (WIDTH//2 - 300, box_y, 600, box_height))
      
        y_offset = box_y + 30
        for line in lines:
            inst_text = font_instructions.render(line, True, (255,105,180))
            WIN.blit(inst_text, (WIDTH//2 - inst_text.get_width()//2, y_offset))
            y_offset += 40

        play_button.draw(WIN)
        quit_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if play_button.is_clicked(event):
                return "play"
            if quit_button.is_clicked(event):
                return "quit"
            
        pygame.display.flip()
        clock.tick(60)

def gameplay():
    pygame.init()

    while True:
        player = Player("player.png", 350, 425)
        food_add_increment = random.randint(400,900)
        food_count = 0
        foods = []
        score = 0
        lives = 3
        game_over = False

        run = True
        while run:
            food_count += clock.tick(60)

            if food_count > food_add_increment:
                for _ in range(1):
                    food_x = random.randint(0, WIDTH - FOOD_WIDTH)
                    if random.random() < 0.1:
                        food = Food("fish.png", food_x, -50, "rotten")
                    else:    
                        food_type = ["donut.png", "toast.png", "cupcake.png", "croissant.png"]
                        food_image = random.choice(food_type)
                        food = Food(food_image, food_x, -20, "fresh")
                    foods.append(food)
                
                food_add_increment = random.randint(400,900)
                food_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return
        
            keys = pygame.key.get_pressed()
            player.move(keys)

            if keys[pygame.K_SPACE]:
                points = player.serve_foods()
                if points > 0:
                    score += points * 2


            for food in foods[:]:
                food.update()

                if food.is_offscreen():
                    if food.food_type == "fresh":
                        lives -= 1
                        print (f"lives remaining: {lives}")
                        if lives == 0:
                            game_over = True
                            run = False
                    foods.remove(food)
                elif food.rect.colliderect(player.rect):

                    if food.rect.bottom >= player.rect.top and food.rect.bottom <= player.rect.top + 20:

                        if food.food_type == "fresh":
                            hit = True
                            player.pile_foods(food.image)
                            foods.remove(food)
                            #print(f"score: {score}")
                            break
                        else:
                            hit = True
                            #print ("Game over!")
                            game_over = True
                            run = False
                            break

            WIN.blit(BG, (0,0))
            player.draw(WIN)  

            for food in foods:
                food.draw(WIN)  

            score_font = pygame.font.SysFont("BoldPixels.ttf", 36)
            score_text = score_font.render(f"Score: {score}", True, (255,255,255))
            WIN.blit(score_text, (10,10))
            lives_text = score_font.render(f"Lives: {lives}", True, (255,255,255))
            WIN.blit(lives_text, (10,50))

            pygame.display.flip()

        if game_over:
            restart = gameover_screen(score)
            if not restart:
                break
        else:
            break

    pygame.quit()

def main():
    pygame.init()
    
    current_state = "menu"
    
    while True:
        if current_state == "menu":
            result = main_menu()
            if result == "play":
                current_state = "play"
            elif result == "quit":
                break
        
        elif current_state == "play":
            result = gameplay()
            if result == "restart":
                current_state = "play"
            elif result == "menu":
                current_state = "menu"
            elif result == "quit":
                break
    
    pygame.quit()

if __name__ == "__main__":
    main()