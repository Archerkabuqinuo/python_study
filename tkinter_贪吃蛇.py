"""
项目分析
- 食物,蛇,世界均为独立
"""
import random
import threading
import time
from tkinter import *
import queue

class Food():
    """
    功能:
        1.出现
        2.被吃&给蛇加分
    """
    def __init__(self, queue):
        """
        生成一个食物
        queue:(一个中枢处理系统,主要用于传送当前类的信息),就是一个不能随意访问的元素,只能从头弹出一个元素
        并且只能从队列尾追加元素的list
        """
        self.queue = queue
        self.new_food()
    def new_food(self):
        """
        功能:随机生成一个食物
        即随机生成一个食物的坐标
        :return:
        """
        # x,y为食物的随机坐标
        x = random.randrange(50, 480)
        y = random.randrange(50, 960)
        self.pos = x, y
        self.queue.put({"food": self.pos})
class Snake(threading.Thread):
    """
    功能:
        1.上下左右按键控制run
        * 2.消灭食物
        3.每次运动需要计算舌头位置
        4.检测游戏是否结束
    """
    def __init__(self,world,queue):
        threading.Thread.__init__(self)

        self.world = world
        self.queue = queue
        self.grades = 0
        self.food = Food(queue)
        self.snake_pos = [(495,55),(485,55),(465.55),(455,55)]
        self.start()
    def run(self):
        if self.world.is_game_over:
            self._delete()
        while not self.world.is_game_over:
            self.queue.put({"move":self.snake_pos})
            time.sleep(0.2)
            self.move()
    def move(self):
        """
        负责蛇的移动
            1.计算舌头坐标
            2.舌头和食物相遇,这分数+1
            3.
        :return:
        """
        snake_new_pos = self.cal_new_pos()
        # 食物被吃,则分数加1
        if self.food.pos == snake_new_pos:
            self.grades += 1
            # 抛出食物被吃分数加1的信息
            self.queue.put({"grade":self.grades})
            # 食物被吃
            self.food.new_food()
        else:
            self.snake_pos.pop(0)
            self.check_game_over(snake_new_pos)
            self.snake_pos.append(snake_new_pos)
    def cal_new_pos(self):
        """
        计算👅的新位置
        :return:
        """
        last_x,last_y = self.snake_pos[-1]
        if self.direction == "UP":
            snake_new_pos = last_x, last_y-10
        elif self.direction == "DOWN":
            snake_new_pos = last_x ,last_y+10
        elif self.direction == "LEFT":
            snake_new_pos = last_x + 10, last_y
        elif self.direction == "RIGHT":
            snake_new_pos = last_x + 10, last_y
        else:
            exit()
        return snake_new_pos
    def key_pressed(self,e):
        # self.direction = e.keysym2
        pass
    def check_game_over(self,snake_pos):
        x, y = snake_pos[0],snake_pos[1]
        if not -5<x<505 or not -5<y<950 or snake_pos in self.snake_pos:
            self.queue.put({"game_over": True})
class World(Tk):
    """
    用来模拟整个游戏画板
    """
    def __init__(self,queue):
        Tk.__init__(self)

        self.queue = queue
        self.is_game_over = False

        #定义画板
        self.canvas = Canvas(self,width=500,height=1000,bg='blue')


        self.snake = self.canvas.create_line((0,0),(0,0),fill='white',width=10)
        self.food = self.canvas.create_rectangle(0,0,0,0,fill='#FFCC4C',outline='#FFCC4C')

        self.grades = self.canvas.create_text(450,20,fill='white',text='score:0')
        self.canvas.pack()
        for i in range(10000):
            self.queue_handler()

    def queue_handler(self):
        """
        消息处理函数,需要不断从中枢队列中拿取
        :return:
        """
        try:
            while True:
                task = self.queue.get(block=False)

                if task.get("game_over"):
                    self.game_over()
                if task.get("move"):
                    grades = [x for grades in task['move'] for x in grades]
                    self.canvas.coords(self.snake,*grades)
        except queue.Empty:
            #self.queue_handler()
            """
            if not self.is_game_over:
                self.canvas.after(100,self.queue_handler())
                # self.canvas.create_text(20,20,fill='red',text=' ')
            
            """
    def game_over(self):
        self.is_game_over = True
        self.canvas.create_text("Game Over")
        qb = Button(self,text="Quit",command=self.destory)
        rd = Button(self,text="Again",command=self.__init__)
if __name__ == "__main__":
    q = queue.Queue()
    world = World(q)

    snake = Snake(world,q)
    world.bind('<Key-Left>',snake.key_pressed(e=LEFT))

    world.mainloop()