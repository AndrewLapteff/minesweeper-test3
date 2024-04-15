import os
from time import sleep

import pygame

from board import Board  # Імпорт класу дошки
from piece import Piece  # Імпорт класу фішки
from solver import Solver  # Імпорт класу розв'язувача


class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)  # Ініціалізація дошки
        pygame.init()
        self.sizeScreen = 800, 800  # Розмір екрану
        self.screen = pygame.display.set_mode(self.sizeScreen)  # Створення екрану
        self.pieceSize = (
            self.sizeScreen[0] / size[1],
            self.sizeScreen[1] / size[0],
        )  # Розмір фішки
        self.loadPictures()  # Завантаження зображень
        self.solver = Solver(self.board)  # Ініціалізація розв'язувача

    def loadPictures(self):
        self.images = {}  # Словник для зображень
        imagesDirectory = "images"  # Директорія зображень
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):  # Ігнорувати файли, що не є .png
                continue
            path = imagesDirectory + r"/" + fileName  # Шлях до файлу
            img = pygame.image.load(path)  # Завантаження зображення
            img = img.convert()  # Конвертація зображення
            # Зміна розміру зображення
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1]))
            )
            # Додавання зображення до словника
            self.images[fileName.split(".")[0]] = img

    def run(self):
        running = True  # Змінна для визначення, чи триває гра
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Вихід з циклу, якщо натиснуто кнопку вихід
                if event.type == pygame.MOUSEBUTTONDOWN and not (
                    self.board.getWon() or self.board.getLost()
                ):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()
            self.screen.fill((0, 0, 0))  # Заповнення екрану чорним кольором
            self.draw()  # Виклик функції для малювання
            pygame.display.flip()  # Оновлення екрану
            if self.board.getWon():
                self.win()  # Виклик функції перемоги
                running = False  # Вихід з циклу після перемоги
        pygame.quit()  # Вимкнення Pygame

    def draw(self):
        topLeft = (0, 0)  # Початкова позиція
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]  # Отримання зображення
                self.screen.blit(image, topLeft)  # Виведення зображення на екран
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        """Функція повертає рядок-ідентифікатор зображення для фішки.

        Аргументи:
        - piece: об'єкт класу Piece, фішка, для якої потрібно отримати рядок-ідентифікатор.

        Пояснення:
        - Якщо фішка була клікнута (подія "click"), повертається кількість бомб навколо фішки або рядок "bomb-at-clicked-block", якщо це бомба.
        - Якщо гравець програв (виявлено, що є бомба), і фішка є бомбою, повертається "unclicked-bomb".
        Якщо фішка є підозрілою (помилково позначена прапорцем), повертається "wrong-flag".
        В іншому випадку повертається "empty-block".
        - У всіх інших випадках повертається "flag", якщо фішка має прапорець, або "empty-block" в іншому випадку.
        """
        if piece.getClicked():
            return (
                str(piece.getNumAround())
                if not piece.getHasBomb()
                else "bomb-at-clicked-block"
            )
        if self.board.getLost():
            if piece.getHasBomb():
                return "unclicked-bomb"
            return "wrong-flag" if piece.getFlagged() else "empty-block"
        return "flag" if piece.getFlagged() else "empty-block"

    def handleClick(self, position, flag):
        """Функція обробляє клік користувача на дошці.

        Аргументи:
        - position: кортеж з позицією кліку користувача на екрані.
        - flag: логічне значення, яке вказує, чи був клік правим кнопкою миші (позначення флагом).

        Пояснення:
        - Визначається індекс фішки на дошці, на яку був натиснутий користувач.
        - Викликається метод handleClick фішки з об'єкта дошки (Board) з визначеним індексом із параметром flag.
            Цей метод відповідає за обробку події кліку для фішки."""
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[
            ::-1
        ]
        self.board.handleClick(self.board.getPiece(index), flag)

    def win(self):
        sound = pygame.mixer.Sound("win.wav")  # Звук перемоги
        sound.play()  # Відтворення звуку
        sleep(3)  # Затримка перед завершенням програми
