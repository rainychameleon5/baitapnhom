import pygame
import random

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch Mango, Orange, and Apple with Hearts")

# Định nghĩa tốc độ cập nhật
clock = pygame.time.Clock()

# Tải hình ảnh và thay đổi kích thước
background_img = pygame.transform.scale(pygame.image.load('bg2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))  # Thêm hình nền
mango_img = pygame.transform.scale(pygame.image.load('mango.png'), (50, 50))
orange_img = pygame.transform.scale(pygame.image.load('orange.png'), (50, 50))
bomb_img = pygame.transform.scale(pygame.image.load('bomb.png'), (50, 50))
apple_img = pygame.transform.scale(pygame.image.load('apple.png'), (50, 50))
player_img = pygame.transform.scale(pygame.image.load('player.png'), (100, 100))
heart_img = pygame.transform.scale(pygame.image.load('heart.png'), (30, 30))  # Thêm trái tim

# Kích thước đối tượng
PLAYER_WIDTH, PLAYER_HEIGHT = player_img.get_size()

# Định nghĩa các biến toàn cục
score = 0
lives = 3  # Số mạng ban đầu
game_over = False

# Tọa độ ban đầu của người chơi
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 10


# Tạo class cho đối tượng rơi (xoài, cam, táo, bom)
class FallingObject:
    def __init__(self, image, speed):
        self.image = image
        self.x = random.randint(0, SCREEN_WIDTH - image.get_width())
        self.y = -image.get_height()
        self.speed = speed

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Tạo các đối tượng rơi
mango = FallingObject(mango_img, 5)
orange = FallingObject(orange_img, 7)
bomb = FallingObject(bomb_img, 6)
apple = FallingObject(apple_img, 4)  # Đối tượng táo


# Hàm kiểm tra va chạm
def check_collision(player_x, player_y, obj):
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    obj_rect = pygame.Rect(obj.x, obj.y, obj.image.get_width(), obj.image.get_height())
    return player_rect.colliderect(obj_rect)


# Hàm hiển thị văn bản lên màn hình
def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Hàm hiển thị số mạng (trái tim)
def draw_lives(lives, img, x, y):
    for i in range(lives):
        screen.blit(img, (x + 40 * i, y))


# Vòng lặp chính của game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Kiểm tra game over
    if game_over:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        draw_text("GAME OVER!", font, BLACK, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30)
        draw_text("Press any key to play again", font, BLACK, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 30)
        pygame.display.update()

        # Chờ người chơi nhấn phím để chơi lại
        keys = pygame.key.get_pressed()
        if any(keys):
            score = 0
            lives = 3
            game_over = False

        continue

    # Lấy trạng thái các phím
    keys = pygame.key.get_pressed()

    # Điều khiển người chơi
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    # Cập nhật đối tượng rơi
    mango.update()
    orange.update()
    bomb.update()
    apple.update()  # Cập nhật táo

    # Kiểm tra va chạm với xoài
    if check_collision(player_x, player_y, mango):
        score += 20
        mango.reset()

    # Kiểm tra va chạm với cam
    if check_collision(player_x, player_y, orange):
        score += 10
        orange.reset()

    # Kiểm tra va chạm với táo
    if check_collision(player_x, player_y, apple):
        score += 5  # Bắt táo cộng 5 điểm
        apple.reset()

    # Kiểm tra va chạm với bom
    if check_collision(player_x, player_y, bomb):
        lives -= 1  # Mỗi lần chạm bom bị trừ 1 mạng
        bomb.reset()
        if lives == 0:
            game_over = True

    # Vẽ nền và các đối tượng
    screen.blit(background_img, (0, 0))  # Vẽ hình nền
    screen.blit(player_img, (player_x, player_y))
    mango.draw()
    orange.draw()
    bomb.draw()
    apple.draw()  # Vẽ táo

    # Hiển thị điểm số và số mạng
    font = pygame.font.SysFont(None, 35)
    draw_text(f"Score: {score}", font, BLACK, 10, 10)
    draw_lives(lives, heart_img, SCREEN_WIDTH - 150, 10)  # Vẽ số mạng còn lại

    # Cập nhật màn hình
    pygame.display.update()

    # Điều chỉnh tốc độ khung hình
    clock.tick(60)
