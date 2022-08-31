import random, sys, pygame
from tkinter import * 
from PIL import Image, ImageTk

#Добавление фоновой музыки:
pygame.init()    
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(3)

class Cons:
    
    BOARD_WIDTH = 600
    BOARD_HEIGHT = 600
    DELAY = 100
    DOT_SIZE = 20
    MAX_RAND_POS = 27
       
class Board(Canvas):

    def __init__(self):
        super().__init__(
            width = Cons.BOARD_WIDTH, height = Cons.BOARD_HEIGHT,
            background = "#32CD7B", highlightthickness = 0
        )
        self.initGame()
        self.pack()
        
#Инициализация игры
    def initGame(self):
        self.inGame = True
        self.dots = 3
        self.score = 0
 ##Переменные для передвижения змеи:
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
 ##Изначальные стартовые координаты яблока:
        self.appleX = 100
        self.appleY = 190

        self.loadImages()
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)
#Подгружаем изображения для игры:
    def loadImages(self):
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)
            
        except IOError as e:
            print(e)
            sys.exit(1)
#Создание объектов на холсте:
    def createObjects(self):
        self.create_text(
            40, 20, text = "Счёт: {0}".format(self.score),
            font = ('time new roman', 15, 'bold'), tag = "score", fill = "white"
        )
        self.create_image(
            self.appleX, self.appleY, image = self.apple,
            anchor = NW, tag = "apple"
        )
        self.create_image(60, 60, image = self.head, anchor = NW, tag = "head")
        self.create_image(20, 60, image = self.dot, anchor = NW, tag = "dot")
        self.create_image(40, 60, image = self.dot, anchor = NW, tag = "dot")
        
#Проверяем, не столкнулась ли голова змеи с яблоком:
    def checkAppleCollision(self):
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:
            if apple[0] == ovr:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image = self.dot, anchor = NW, tag = "dot")
                self.locateApple()
                s = pygame.mixer.Sound("ukus-apple.wav")
                s.play()
#Меняем положение змеи на холсте:
    def moveSnake(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        items = dots + head
        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z + 1])
            self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1
        self.move(head, self.moveX, self.moveY)
#Проверка на столкновение змеи с другими объектами:
    def checkCollisions(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
        if x1 < 0:
            self.inGame = False
        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False
        if y1 < 0:
            self.inGame = False
        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.inGame = False
#Распределяем яблоки по холсту (canvas):
    def locateApple(self):
        apple = self.find_withtag("apple")
        self.delete(apple[0])
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE
        self.create_image(
            self.appleX, self.appleY, anchor=NW,
            image = self.apple, tag = "apple"
        )
#Управление змеёй стрелками клавиатуры:
    def onKeyPressed(self, e):
        key = e.keysym
        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = - Cons.DOT_SIZE
            self.moveY = 0
        RIGHT_CURSOR_KEY = "Right"    
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0
        UP_CURSOR_KEY = "Up"    
        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = - Cons.DOT_SIZE
        DOWN_CURSOR_KEY = "Down"    
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE
#Создаём игровой цикл для каждого события таймера:
    def onTimer(self):
        self.drawScore()
        self.checkCollisions()
        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(Cons.DELAY, self.onTimer)
        else:
            self.gameOver()
#Рисуем счёт игры:
    def drawScore(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text = "Счёт: {0}".format(self.score))
        
#Удаляем все объекты и выводим сообщение об окончании игры:
    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() /2,
            text = "Игра закончилась со счётом: {0}".format(self.score),
            font = ('time new roman', 15, 'bold'), fill = "black")
        pygame.mixer.music.stop()
        s = pygame.mixer.Sound("game-over.wav")
        s.play()

class Snake(Frame):

    def __init__(self):
        super().__init__()
        self.master.title('Змейка')
        self.board = Board()
        self.pack()
                               
def main():
    root = Tk()
    root.iconphoto(False, PhotoImage(file='icon.png'))
    nib = Snake()
    root.mainloop()
      
if __name__ == '__main__':
    main()
  














        
