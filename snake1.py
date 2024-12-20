import pygame
import random
import sys
import heapq

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Multiple Modes")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

# Directions
DIRECTIONS = {
    "UP": (0, -CELL_SIZE),
    "DOWN": (0, CELL_SIZE),
    "LEFT": (-CELL_SIZE, 0),
    "RIGHT": (CELL_SIZE, 0)
}

# Snake initialization
def init_snake():
    return [(100, 100), (80, 100), (60, 100)]

def generate_food(snake1, snake2=None):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake1 and (x, y) not in (snake2 or []):
            return (x, y)

# A* Algorithm for AI movement
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles):
    """Performs A* pathfinding."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction in DIRECTIONS.values():
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (neighbor[0] < 0 or neighbor[0] >= WIDTH or 
                neighbor[1] < 0 or neighbor[1] >= HEIGHT or 
                neighbor in obstacles):
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = DIRECTIONS[direction]
    new_head = (head_x + dx, head_y + dy)
    return [new_head] + snake[:-1]

def move_ai(snake_ai, food):
    """AI moves towards the food using A*."""
    head_x, head_y = snake_ai[0]
    path = a_star((head_x, head_y), food, snake_ai)
    
    if path:
        next_move = path[0]
        dx = next_move[0] - head_x
        dy = next_move[1] - head_y
        if dx == CELL_SIZE:
            return "RIGHT"
        elif dx == -CELL_SIZE:
            return "LEFT"
        elif dy == CELL_SIZE:
            return "DOWN"
        elif dy == -CELL_SIZE:
            return "UP"
    else:
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

def draw_game(snake, snake_ai, food, score, score_ai):
    # Draw snakes and food
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    for segment in snake_ai:
        pygame.draw.rect(screen, BLUE, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Draw scores
    score_text1 = font_small.render(f"Player Score: {score}", True, WHITE)
    score_text2 = font_small.render(f"AI Score: {score_ai}", True, WHITE)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (WIDTH // 2 + 10, 10))

# Difficulty Levels
DIFFICULTY_SETTINGS = {
    "easy": 10,
    "medium": 15,
    "hard": 20
}

# Select Game Mode
def game_mode_selection():
    screen.fill(BLACK)
    title_text = font_large.render("Select Game Mode", True, WHITE)
    manual_play_text = font_medium.render("1. Manual Play", True, YELLOW)
    manual_vs_ai_text = font_medium.render("2. Manual vs AI", True, YELLOW)
    ai_play_text = font_medium.render("3. AI Play", True, YELLOW)
    quit_text = font_medium.render("Q. Quit", True, YELLOW)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(manual_play_text, (WIDTH // 2 - manual_play_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(manual_vs_ai_text, (WIDTH // 2 - manual_vs_ai_text.get_width() // 2, HEIGHT // 2))
    screen.blit(ai_play_text, (WIDTH // 2 - ai_play_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

def get_game_mode():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "manual_play"
                elif event.key == pygame.K_2:
                    return "manual_vs_ai"
                elif event.key == pygame.K_3:
                    return "ai_play"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Game Over Handling
def game_over_screen(score, score_ai=None):
    screen.fill(BLACK)
    game_over_text = font_large.render("Game Over", True, RED)
    score_text = font_medium.render(f"Player Score: {score}", True, WHITE)
    
    if score_ai is not None:
        ai_score_text = font_medium.render(f"AI Score: {score_ai}", True, WHITE)
        winner_text = font_medium.render(f"Winner: {'Player' if score > score_ai else 'AI'}", True, YELLOW)
        screen.blit(ai_score_text, (WIDTH // 2 - ai_score_text.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3 + 100))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, YELLOW)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Restart game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def manual_play():
    snake = init_snake()
    food = generate_food(snake)
    score = 0
    direction = "RIGHT"

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        snake = move_snake(snake, direction)
        if snake[0] in snake[1:] or snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT:
            game_over_screen(score)
            return

        if snake[0] == food:
            snake.append(snake[-1])
            food = generate_food(snake)
            score += 1

        draw_game(snake, [], food, score, 0)
        pygame.display.flip()
        clock.tick(10)

def manual_vs_ai():
    snake_player = init_snake()
    snake_ai = init_snake()
    food = generate_food(snake_player, snake_ai)
    score_player = 0
    score_ai = 0
    direction_player = "RIGHT"

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction_player != "DOWN":
                    direction_player = "UP"
                elif event.key == pygame.K_DOWN and direction_player != "UP":
                    direction_player = "DOWN"
                elif event.key == pygame.K_LEFT and direction_player != "RIGHT":
                    direction_player = "LEFT"
                elif event.key == pygame.K_RIGHT and direction_player != "LEFT":
                    direction_player = "RIGHT"

        snake_player = move_snake(snake_player, direction_player)
        direction_ai = move_ai(snake_ai, food)
        snake_ai = move_snake(snake_ai, direction_ai)

        if snake_player[0] in snake_player[1:] or snake_player[0][0] < 0 or snake_player[0][0] >= WIDTH or snake_player[0][1] < 0 or snake_player[0][1] >= HEIGHT:
            game_over_screen(score_player, score_ai)
            return
        if snake_ai[0] in snake_ai[1:] or snake_ai[0][0] < 0 or snake_ai[0][0] >= WIDTH or snake_ai[0][1] < 0 or snake_ai[0][1] >= HEIGHT:
            game_over_screen(score_player, score_ai)
            return

        if snake_player[0] == food:
            snake_player.append(snake_player[-1])
            food = generate_food(snake_player, snake_ai)
            score_player += 1

        if snake_ai[0] == food:
            snake_ai.append(snake_ai[-1])
            food = generate_food(snake_player, snake_ai)
            score_ai += 1

        draw_game(snake_player, snake_ai, food, score_player, score_ai)
        pygame.display.flip()
        clock.tick(10)

def ai_play():
    snake_ai = init_snake()
    food = generate_food(snake_ai)
    score_ai = 0

    while True:
        screen.fill(BLACK)

        direction_ai = move_ai(snake_ai, food)
        snake_ai = move_snake(snake_ai, direction_ai)

        if snake_ai[0] in snake_ai[1:] or snake_ai[0][0] < 0 or snake_ai[0][0] >= WIDTH or snake_ai[0][1] < 0 or snake_ai[0][1] >= HEIGHT:
            game_over_screen(score_ai)
            return

        if snake_ai[0] == food:
            snake_ai.append(snake_ai[-1])
            food = generate_food(snake_ai)
            score_ai += 1

        draw_game([], snake_ai, food, 0, score_ai)
        pygame.display.flip()
        clock.tick(10)

def main():
    while True:
        game_mode_selection()
        game_mode = get_game_mode()

        if game_mode == "manual_play":
            manual_play()
        elif game_mode == "manual_vs_ai":
            manual_vs_ai()
        elif game_mode == "ai_play":
            ai_play()

if __name__ == "__main__":
    main()
