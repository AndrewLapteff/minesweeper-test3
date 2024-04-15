class Piece:
    # Стани: Не клікнуто, клікнуто, позначено прапорцем
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb  # Чи має фішка бомбу
        self.around = 0  # Кількість бомб навколо фішки
        self.clicked = False  # Чи клікнуто на фішку
        self.flagged = False  # Чи позначено фішку прапорцем
        self.neighbors = []  # Сусіди фішки

    def __str__(self):
        return str(self.hasBomb)  # Повертає рядок, представлення стану бомби

    def getNumAround(self):
        return self.around  # Повертає кількість бомб навколо фішки

    def getHasBomb(self):
        return self.hasBomb  # Повертає стан наявності бомби

    def getClicked(self):
        return self.clicked  # Повертає стан клікнутості фішки

    def getFlagged(self):
        return self.flagged  # Повертає стан позначення прапорцем фішки

    def toggleFlag(self):
        self.flagged = not self.flagged  # Змінює стан позначення прапорцем фішки

    def handleClick(self):
        self.clicked = True  # Позначає фішку як клікнуту

    def setNumAround(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.getHasBomb():
                num += 1
        self.around = num  # Встановлює кількість бомб навколо фішки

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors  # Встановлює сусідів фішки

    def getNeighbors(self):
        return self.neighbors  # Повертає сусідів фішки
