import pygame
import random

colors = [
        (255, 255, 0),
        (0, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 128, 0),
        (255, 0, 255)]

class Figure:
    figures = [
            [[0, 1, 4, 5]], 
            [[1, 5, 9, 13], [4, 5, 6, 7]], 
            [[6, 7, 9, 10], [1, 5, 6, 10]], 
            [[4, 5, 9, 10], [2, 6, 5, 9]], 
            [[1, 5, 9, 10], [2, 4, 5, 6], [0, 1, 5, 9], [4, 5, 6, 8]],
            [[2, 6, 9, 10], [5, 6, 7, 11], [2, 3, 6, 10], [1, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        rand = random.randint(0, 6)
        self.figure = rand
        self.color = rand
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.figure])

    def image(self):
        return self.figures[self.figure][self.rotation]

class Tetris:
    figure = Figure(3, 0)
    status = "game"
    x = 100
    y = 60
    size = 20

    def __init__(self, path_map, path_score, level, lvl_up):
        self.path_map = path_map
        self.path_score = path_score
        with open(path_map, 'r') as mapFile:
            self.tetris_map = [line.strip() for line in mapFile]
        with open(path_score, 'r') as scoreFile:
            self.highscore = int(scoreFile.readline())
            self.score = int(scoreFile.readline())
            self.lines = int(scoreFile.readline())
        self.height = len(self.tetris_map)
        self.width = len(self.tetris_map[0])
        self.level = level
        self.lvl_up = lvl_up

    def deleteFigure(self):
        self.figure = None

    def createFigure(self, x, y):
        self.figure = Figure(x, y)
        if self.isCollide():
            self.deleteFigure()
            self.status = "gameover"

    def isCollide(self):
        is_collide = False
        for i in range(4):
            for j in range(4):
                if j + i * 4 in self.figure.image():
                    if self.figure.x + j + 1 > self.width or self.figure.y + i >= self.height or self.figure.x + j < 0 or self.tetris_map[i + self.figure.y][j + self.figure.x] != '.':
                        is_collide = True
        return is_collide

    def breakLines(self):
        full_lines = 0
        for i in range(1, self.height):
            k_zero = 0
            for j in range(self.width):
                if self.tetris_map[i][j] == ".":
                    k_zero += 1
            if k_zero == 0:
                full_lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        string = ""
                        for k in range(j):
                            string += self.tetris_map[i1][k]
                        string += self.tetris_map[i1 - 1][j]
                        for k in range(j + 1, self.width):
                            string += self.tetris_map[i1][k]
                        self.tetris_map[i1] = string
        if full_lines == 1:
            self.score += 1
        if full_lines == 2:
            self.score += 3
        if full_lines == 3:
            self.score += 5
        if full_lines == 4:
            self.score += 9
        if self.score > self.highscore:
            self.highscore = self.score
        self.lines += full_lines
        self.level = self.lines // self.lvl_up + 1

    def stop(self):
        for i in range(4):
            for j in range(4):
                if j + i * 4 in self.figure.image():
                    string = ""
                    for k in range(j + self.figure.x):
                        string += self.tetris_map[i + self.figure.y][k]
                    string += str(self.figure.color)
                    for k in range(len(string), self.width):
                        string += self.tetris_map[i + self.figure.y][k]
                    self.tetris_map[i + self.figure.y] = string
        self.breakLines()
        self.createFigure(3, 0)

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.isCollide():
            self.figure.rotation = previous_rotation

    def left(self):
        self.figure.x -= 1
        if self.isCollide():
            self.figure.x += 1

    def right(self):
        self.figure.x += 1
        if self.isCollide():
            self.figure.x -= 1 

    def down(self):
        while True:
            if self.isCollide():
                self.figure.y -= 1
                self.stop()
                break
            self.figure.y += 1

    def step(self):
        self.figure.y += 1
        if self.isCollide():
            self.figure.y -= 1
            self.stop()

    def clear(self):
        self.deleteFigure()
        string = ""
        for i in range(self.width):
            string += "."
        for i in range(self.height):
            self.tetris_map[i] = string

    def save(self):
        f = open(self.path_score, "w")
        f.write(str(self.highscore) + "\n")
        f.write(str(self.score) + "\n")
        f.write(str(self.lines) + "\n")
        f.close()
        f = open(self.path_map, "w")
        for i in range(self.height):
            f.write(self.tetris_map[i] + "\n")
        f.close()

if __name__ == '__main__':
    pygame.init()

    size = width, height = 400, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    game = True

    fps = 25
    clock = pygame.time.Clock()
    counter = 0
    tetris = Tetris("data/map.txt", "data/highscore.txt", 1, 50)

    p_left = False
    p_right = False
    p_down = False

    while game:
        if tetris.figure is None:
            tetris.createFigure(3, 0)
        counter += 1
        if counter == 100000:
            counter = 0

        if tetris.status == "game":
            if counter % (fps // tetris.level // 2) == 0 or p_down:
                tetris.step()
            if p_left:
                if counter % 2 == 0:
                    tetris.left()
            if p_right:
                if counter % 2 == 0:
                    tetris.right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tetris.clear()
                    tetris.status = "game"
                    tetris.score = 0
                if tetris.status == "game":
                    if event.key == pygame.K_UP:
                        tetris.rotate()
                    if event.key == pygame.K_DOWN:
                        p_down = True
                        p_left = False
                        p_right = False
                    if event.key == pygame.K_LEFT:
                        p_left = True
                        p_right = False
                        p_down = False
                    if event.key == pygame.K_RIGHT:
                        p_right = True
                        p_left = False
                        p_down = False
                    if event.key == pygame.K_SPACE:
                        tetris.down()

        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    p_left = False
                if event.key == pygame.K_RIGHT:
                    p_right = False
                if event.key == pygame.K_DOWN:
                    p_down = False

        screen.fill((255, 255, 255))
        tetris.save()

        for i in range(tetris.height):
            for j in range(tetris.width):
                pygame.draw.rect(screen, (127, 127, 127), [tetris.x + tetris.size * j, tetris.y + tetris.size * i, tetris.size, tetris.size], 1)
                if tetris.tetris_map[i][j] != ".":
                    pygame.draw.rect(screen, colors[int(tetris.tetris_map[i][j])], [tetris.x + tetris.size * j + 1, tetris.y + tetris.size * i + 1, tetris.size - 2, tetris.size - 1])

        if tetris.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in tetris.figure.image():
                        pygame.draw.rect(screen, colors[tetris.figure.color], [tetris.x + tetris.size * (j + tetris.figure.x) + 1, tetris.y + tetris.size * (i + tetris.figure.y) + 1, tetris.size - 2, tetris.size - 2])

        font = pygame.font.SysFont('timesnewroman', 25, True)
        font1 = pygame.font.SysFont('timesnewroman', 65, True)

        text_score = font.render("Score: " + str(tetris.score), True, (0, 0, 0))
        text_highscore = font.render("Highscore: " + str(tetris.highscore), True, (0, 0, 0))
        text_game_over = font1.render("Game Over", True, (255, 125, 0))

        screen.blit(text_score, [0, 0])
        screen.blit(text_highscore, [0, 30])
        if tetris.status == "gameover":
            screen.blit(text_game_over, [20, 200])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()