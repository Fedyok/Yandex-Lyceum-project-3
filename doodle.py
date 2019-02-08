#!/usr/bin/python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame и другие программы
import pygame
from pygame import *
from player import *
from blocks import *
import sys


pygame.init()
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 680  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Создаём экран по ширине и высоте
BACKGROUND_COLOR = "white"
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.play()  # включаем музыку


class Camera(object):  # класс камеры
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 30, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)                           # Не идёт дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не идёт дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не идёт дальше нижней границы
    t = min(0, t)                           # Не идёт дальше верхней границы

    return Rect(l, t, w, h)


def new_level(name):  # функция, подгружающая новые уровни из текстовых файлов
    level = []

    with open(name) as f:
        for line in f:
            level.append(line)

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "=":
                pp = Finish(x, y)
                entities.add(pp)
                platforms.append(pp)
            if col == "F":
                ff = Stop(x, y)
                entities.add(ff)
                platforms.append(ff)

            if col == "M":
                mm = Dimonster(x, y)
                entities.add(mm)
                platforms.append(mm)
                dimon.add(mm)
            x += 32  # блоки платформы ставятся на ширине блоков
        y += 32    # то же самое и с высотой
        x = 0


def game():  # основная функция игры
    class Menu:  # класс стартового меню
        def __init__(self,\
        punkts=[120, 140, u"punkt", (250, 250, 30), (250, 30, 250)]):

            self.punkts = punkts

        def render(self, poverhnost, font, num_punkt):
            for i in self.punkts:
                if num_punkt == i[5]:
                    poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
                else:
                    poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

        def menu(self):
            done = True
            font_menu = pygame.font.Font(None, 90)
            punkt = 0
            while done:
                bg.fill(Color(0, 100, 200))

                mp = pygame.mouse.get_pos()

                for i in self.punkts:

                    if mp[0] > i[0] and mp[0] < i[0] + 155 and\
                       mp[1] > i[1] and mp[1] < i[1] + 50:
                        punkt = i[5]
                self.render(bg, font_menu, punkt)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            sys.exit()
                        elif e.key == pygame.K_UP:
                            if punkt > 0:
                                punkt -= 1
                        elif e.key == pygame.K_DOWN:
                            if punkt < len(self.punkts) - 1:
                                punkt += 1
                    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if punkt == 0:
                            done = False
                            screen.blit(bg, (0, 0))
                            bg.fill(Color(BACKGROUND_COLOR))
                            pygame.display.flip()
                        elif punkt == 3:
                            sys.exit()
                        elif punkt == 2:
                            record_screen()
                        elif punkt == 1:
                            rul_screen()
                screen.blit(bg, (0, 0))
                pygame.display.flip()

    def die_screen():
        a = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load('loose.mp3')
        pygame.mixer.music.play()
        intro_text = ["            УВЫ, ВЫ ПРОИГРАЛИ!",
                      "         КОЛИЧЕСТВО ВАШИХ ЖИЗНЕЙ",
                      "               РАВНО НУЛЮ!",
                      "           ТЕПЕРЬ ИГРА ЗАКРОЕТСЯ(",
                      "",
                      "",
                      "         И НАЧНЕТСЯ С ПЕРВОГО УРОВНЯ..."]

        screen.fill(Color(100, 0, 100))
        font = pygame.font.Font(None, 50)
        text_coord = 150
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(250, 250, 30))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while a is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    new_level("level1.txt")
                    pygame.mixer.music.stop()
                    a = False
                pygame.display.flip()

    def rul_screen():
        pygame.mixer.music.stop()
        pygame.mixer.music.load('fon.mp3')
        pygame.mixer.music.play()
        a = True
        intro_text = ["                             ПРАВИЛА",
                      "                                     ",
                      "      УПРАВЛЕНИЕ:",
                      "        СТРЕЛКА ВЛЕВО = ДВИЖЕНИЕ ВЛЕВО",
                      "        СТРЕЛКА ВВЕРХ = ПРЫЖОК",
                      "        СТРЕЛКА ВПРАВО = ДВИЖЕНИЕ ВПРАВО",
                      "        ESCAPE = ПАУЗА, А ТАКЖЕ В МЕНЮ = ВЫЙТИ ИЗ ИГРЫ",
                      "        МОЖНО ОДНОВРЕМЕННО НАЖИМАТЬ ",
                      "        КНОПКИ ВВЕРХ И ВПРАВО/ВЛЕВО",
                      "      У ВАС ТРИ ЖИЗНИ",
                      "      ДОБЕРИТЕСЬ ДО САМОГО ВЕРХА",
                      "                                 ",
                      "                                 ",
                      "                          УДАЧИ!!!        "]

        screen.fill(Color(100, 100, 100))
        font = pygame.font.Font(None, 32)
        text_coord = 85
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(250, 250, 30))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while a is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game.menu()
                    a = False
                    pygame.mixer.music.stop()
                pygame.display.flip()

    def win_screen():
        a = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load('win.mp3')
        pygame.mixer.music.play()
        intro_text = ["     СПАСИБО ЗА ИГРУ!!!",
                      "     Вы выиграли!!!",
                      "     ваш результат: " + str(points)]

        screen.fill(Color(100, 100, 100))
        font = pygame.font.Font(None, 30)
        text_coord = 150
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(250, 250, 30))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while a == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    a = False
                    game.menu()
                pygame.display.flip()

    def record_screen():
        a = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load('fon.mp3')
        pygame.mixer.music.play()
        screen.fill(Color(100, 100, 100))
        intro_text = ["                 РЕКОРДЫ:",
                      "",
                      "",
                      "         5.  " + str(records[0]),
                      "         4.  " + str(records[1]),
                      "         3.  " + str(records[2]),
                      "         2.  " + str(records[3]),
                      "         1.  " + str(records[4])]

        font = pygame.font.Font(None, 50)
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(250, 250, 30))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while a == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    a = False
                    game.menu()

                pygame.display.flip()

    def end_screen(name):
        a = True

        pygame.mixer.music.stop()
        pygame.mixer.music.load('win.mp3')
        pygame.mixer.music.play()
        intro_text = ["                 СПАСИБО ЗА ИГРУ!!!",
                      "",
                      "",
                      "     Вы были великолепны!",
                      "     А теперь вас ждёт следующий уровень..."]

        screen.fill(Color(100, 100, 100))
        font = pygame.font.Font(None, 38)
        text_coord = 150
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(250, 250, 30))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while a == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    new_level(name)
                    a = False
                pygame.display.flip()

    records = []  # список для рекордов
    points = 0   # переменная очков
    try:
        with open('records.txt') as f:
            for line in f:
                records.append(int(line.strip()))
        if len(records) < 5:
            while len(records) != 5:
                records.append(0)
        records.sort()
    except Exception as e:
        print(e)
    f.close()

    pygame.init()  # Инициация PyGame, обязательная строчка 
    pygame.mixer.music.stop()
    pygame.mixer.music.load('fon.mp3')
    pygame.mixer.music.play()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Doodler Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH, 680))  # Создание видимой поверхности
    info_str = Surface((WIN_WIDTH,30))  # будем использовать как фон

    ''' Создаем Меню'''
    punkts = [(120, 100, u'Game',\
               pygame.Color(250, 250, 30), pygame.Color(250, 30, 250), 0),
              (130, 250, u'Rules',\
               pygame.Color(250, 250, 30), pygame.Color(250, 30, 250), 1),
              (120, 400, u'Record',\
               pygame.Color(250, 250, 30), pygame.Color(250, 30, 250), 2),
              (120, 550, u'Quit',\
               pygame.Color(250, 250, 30), pygame.Color(250, 30, 250), 3)]
    game = Menu(punkts)
    game.menu()



    l = 1  # переменная для уровней
    new_level("level1.txt")
    while l != 4:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('fon.mp3')
        pygame.mixer.music.play()
        bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

        info_str.fill(Color(45, 80, 40))
        #Шрифты
        pygame.font.init()
        life_font = pygame.font.Font(None, 32)


        hero = Player(55, 3296)  # создаем героя по (x, y) координатам
        left = right = False  # по умолчанию - стоим
        up = False
        shoot = False
        arrow = Arrow(-10, 300)

        entities.add(hero)
        entities.add(arrow)


         # то, во что мы будем врезаться или опираться


        total_level_width  = 35 * 32  # Высчитываем фактическую ширину уровня
        total_level_height = 108 * 32   # высоту

        timer = pygame.time.Clock()
        camera = Camera(camera_configure, total_level_width, total_level_height)
        rect = Rect(hero.rect)
        running = True

        while hero.winner == False and hero.life > 0:  # Основной цикл программы
            timer.tick(60)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True


                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                    game.menu()
                if (e.type == KEYUP or e.type == KEYDOWN) and e.key == K_SPACE:
                    if arrow.push == False:
                        shoot = True
                        arrow = Arrow(hero.rect[0] + 9, hero.rect[1] - 40)
                        entities.add(arrow)
                        arrow.push = True

            info_str.fill(Color(255, 255, 255))
            info_str.blit(life_font.render(u'Life: '\
                                           + str(hero.life)\
                                           + u'                     Score:'\
                                           + str(points),\
                                           True, (210, 120, 200)), (50, 5))

            screen.blit(info_str, (0, 0))
            screen.blit(bg, (0, 30))
            rect[0] = hero.rect[0]
            rect[1] = rect[1] - hero.speed
            if rect[1] < hero.rect[1] - 500 or hero.die == True:
                hero.retry()
                rect = Rect(hero.rect)
                hero.die = False



            camera.update(rect)  # центризируем камеру относительно персонажа


            hero.update(left, right, up, shoot, platforms)
            a = 1
            if arrow.push is True:
                shoot = True
                a = arrow.update(hero.rect[1], platforms)
            else:
                shoot = False
                entities.remove(arrow)
            if a == 0:
                points += 500
            for e in dimon:
                if e.rect.colliderect(arrow):
                    dimon.remove(e)
            dimon.update()  # передвижение
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            pygame.display.update()

        for e in entities:
            entities.remove(e)
        platforms.clear()
        for d in dimon:
            dimon.remove(d)

        for e in entities:
            screen.blit(e.image, camera.apply(e))
        screen.blit(info_str, (0, 0))
        screen.blit(bg, (0, 30))

        if hero.life == 0:
            l = 1
            if points > records[0]:
                records[0] = points
            records.sort()
            f = open('records.txt', 'w')
            for i in records:
                f.writelines(str(i) + '\n')
            points = 0
            die_screen()
        elif l != 3:
            l += 1
            points += 5000

            end_screen("level%s.txt"%l)
        elif l == 3:
            points += 5000
            if points > min(records):
                records[0] = points
            records.sort()
            f = open('records.txt', 'w')
            for i in records:
                f.writelines(str(i) + '\n')
            win_screen()
            points = 0
        pygame.display.update()     # обновление и вывод всех изменений на экран

dimon = pygame.sprite.Group()
entities = pygame.sprite.Group()  # Все объекты
platforms = []

if __name__ == "__main__":
    game()
pygame.quit()
