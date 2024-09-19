import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
orange = (255, 165, 0)  # Color for super food

# Display settings
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Clock and font
clock = pygame.time.Clock()
snake_block = 10
initial_snake_speed = 10  # Initial speed
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# Functions for score and snake drawing
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [10, 10])  # Display score in the top left corner


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, position)


# Pause Function
def pause():
    paused = True
    while paused:
        dis.fill(blue)
        message("Game Paused. Press SPACE to Resume", yellow, [dis_width / 6, dis_height / 3])
        message("Press Q to Quit or N for New Game", yellow, [dis_width / 6, dis_height / 3 + 40])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press 'Space' to resume
                    paused = False
                if event.key == pygame.K_q:  # Press 'Q' to quit
                    pygame.quit()
                    quit()
                if event.key == pygame.K_n:  # Press 'N' to start a new game
                    gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


# Game Loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    super_foodx = None
    super_foody = None
    super_food_timer = 15  # Time for super food to disappear in seconds
    super_food_start_time = None

    snake_speed = initial_snake_speed
    super_food_active = False

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red, [dis_width / 6, dis_height / 3])
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:  # Press 'Space' to pause the game
                    pause()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # Draw normal food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Check if super food should appear or disappear
        if super_food_active:
            pygame.draw.rect(dis, orange, [super_foodx, super_foody, snake_block, snake_block])
            # Check if the super food time has expired
            if pygame.time.get_ticks() - super_food_start_time >= super_food_timer * 1000:
                super_foodx = None
                super_foody = None
                super_food_active = False
        else:
            # Activate super food after a random interval
            if random.random() < 0.01:  # Adjust probability as needed
                super_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                super_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                super_food_active = True
                super_food_start_time = pygame.time.get_ticks()

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score = length_of_snake - 1

            # Increase snake speed every 5 points
            if score % 5 == 0:
                snake_speed += 2

        if super_food_active:
            if x1 == super_foodx and y1 == super_foody:
                super_foodx = None
                super_foody = None
                length_of_snake += 5  # Increase snake length more
                score += 10  # Increase score significantly
                snake_speed += 5  # Boost speed for a short period
                super_food_active = False
                super_food_start_time = None

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Start the game
gameLoop()
