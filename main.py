import pygame
from pygame.locals import *
from random import choice
from sys import exit
pygame.init()
pygame.display.set_caption('Cube')
screen = pygame.display.set_mode((450, 600))
shape = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]
color = [
    (0, 255, 255),
    (255, 165, 0),
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
]


def choose_color():
    return choice(color)


def choose_shape():
    return choice(shape)


piese_color = choose_color()
piese_shape = choose_shape()


class Piece:
    def __init__(self):
        global piese_color, piese_shape
        self.shape = piese_shape
        self.color = piese_color
        self.x = 5
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def draw_piese(piese):
    for y, row in enumerate(piese.shape):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(screen, piese.color, (piese.x * 30 + x * 30, piese.y * 30 + y * 30, 30, 30))


def check_move(back, piece):
    for y, row in enumerate(piece.shape):
        for x, value in enumerate(row):
            if value:
                if piece.x + x < 0 or piece.x + x >= 10 or piece.y + y >= 20 or back[piece.y + y][piece.x + x]:
                    return True
    return False


def merge_piece(back, piece):
    for y, row in enumerate(piece.shape):
        for x, value in enumerate(row):
            if value:
                back[piece.y + y][piece.x + x] = piece.color


def clear_lines(back):
    lines_to_clear = [i for i, row in enumerate(back) if all(row)]
    for i in lines_to_clear:
        del back[i]
        back.insert(0, [None] * 10)
    return len(lines_to_clear)


def game():
    global piese_color, piese_shape
    piese = Piece()
    piese_shape = choose_shape()
    piese_color = choose_color()
    point = 0
    back = [[None for _ in range(10)] for _ in range(20)]
    game_over = False
    transparent_surface = pygame.Surface((300, 100), pygame.SRCALPHA)
    transparent_color = (255, 255, 255, 200)
    transparent_surface.fill(transparent_color)
    best = int(open('./files/best.txt', 'r').read())
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        game_over = False
                        point = 0
                        back = [[None for _ in range(10)] for _ in range(20)]
                        piese = Piece()
                if not game_over:
                    if event.key == K_UP:
                        piese.rotate()
                        if check_move(back, piese):
                            piese.rotate()
                    elif event.key == K_LEFT:
                        if piese.x * 30 >= 30:
                            piese.x -= 1
                            if check_move(back, piese):
                                piese.x += 1
                    elif event.key == K_RIGHT:
                        if piese.x * 30 <= 300 - (len(piese.shape[0]) + 1) * 30:
                            piese.x += 1
                            if check_move(back, piese):
                                piese.x -= 1
                    elif event.key == K_DOWN:
                        piese.y += 1
                        if check_move(back, piese):
                            piese.y -= 1
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 165, 0), (300, 0, 150, 600), 0)
        pygame.draw.rect(screen, (255, 255, 255), (300, 0, 10, 600), 0)
        pygame.draw.rect(screen, (0, 0, 0), (310, 150, 140, 180), 0)
        draw_piese(piese)
        for y in range(len(back)):
            for x in range(len(back[y])):
                if back[y][x]:
                    pygame.draw.rect(screen, back[y][x], (x * 30, y * 30, 30, 30), 0)
        for x in range(10):
            for y in range(20):
                pygame.draw.rect(screen, (255, 255, 255), (x * 30, y * 30, 30, 30), 1)
        screen.blit(pygame.font.SysFont('Amadeus', 25).render(f'Point: {point}', True, (255, 255, 255)), (315, 15))
        screen.blit(pygame.font.SysFont('Amadeus', 25).render(f'Best: {best}', True, (255, 255, 255)), (315, 50))
        screen.blit(pygame.font.SysFont('Amadeus', 25).render('Next:', True, (255, 255, 255)), (315, 120))
        screen.blit(pygame.font.SysFont('Amadeus', 20).render('\u00A9Kevin2024', True, (255, 255, 255)), (315, 560))
        for y, row in enumerate(piese_shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, piese_color, (330 + (x * 25), 200 + (y * 25), 25, 25))
        if not game_over:
            piese.y += 1
            if check_move(back, piese):
                piese.y -= 1
                merge_piece(back, piese)
                piese = Piece()
                piese_shape = choose_shape()
                piese_color = choose_color()
                point += clear_lines(back)
                if check_move(back, piese):
                    if point >= best:
                        open('./files/best.txt', 'w').write(str(point))
                        best = point
                    game_over = True
        else:
            screen.blit(transparent_surface, (0, 195))
            screen.blit(pygame.font.SysFont('Amadeus', 50).render('Game Over', True,
                                                                  (0, 0, 255)), (40, 200))
            screen.blit(pygame.font.SysFont('Amadeus', 25).render('Press "Enter" To Play Again', True,
                                                                  (0, 0, 255)), (5, 250))
        pygame.display.update()
        pygame.time.Clock().tick(3)


if __name__ == '__main__':
    game()
