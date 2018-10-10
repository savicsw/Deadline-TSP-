from tkinter import *
from random import *
from math import sqrt
import operator
import re
import numpy
import numpy as np

points_in = [] #输入点序列
size = 550  #地图尺寸
deadline = []   #deadline （开始时间，截止时间）
CostList = []   #cost列表-各点之间访问的cost
speed = 10      #速度，用于调整cost的参数
number = 50     #point的数量
deadline_range = [(30,450),(540,960)]   #deadline的随机范围（平均分布）
color = "black"     #颜色定义
red_points = []     #红点序列
destination = []    #目的地序列
StationLoc = [(500,300),(200,50)]   #机场/车站
variance = 100       #方差
mu = 300            #均值   


def click(event):
    draw_point(event.x, event.y)
    points_in.append((event.x, event.y))

def draw_point(x,y):
    if color == "black":
        c.create_oval(x-3, y-3, x+3, y+3, fill="black", tags = "black_point")
    if  color == "red" :
        c.create_oval(x-3, y-3, x+3, y+3, fill="red", tags = "red_point")


def draw_points(points):
    c.delete("point", "line");
    for point in points:
        draw_point(int(point[0]),int(point[1]))

def draw_line(points):
    c.delete("line")
    c.create_line(points, tags="line")



def clear():
    global points_in
    global deadline
    global TimeList
    global red_points
    c.delete("point", "line","black_point","red_point")
    points_in = []
    deadline = []
    TimeList = []
    red_points = []



def randomise_n(): #正态随机
    global points_in
    global deadline
    global color
    count = 0
    clear()
    for i in range(number):
        while TRUE :
            point = (variance*np.random.randn()+mu,variance*np.random.randn()+mu)
            count = count + 1
            if point[0] >= 0 and point[0] <= size and point[1] >= 0 and point[1] <= size:
                break
            if point[0] < 0 : point = (randint(0,5),point[1])
            if point[0] > 550 :point = (randint(545,550),point[1])
            if point[1] < 0 : point = (point[0],randint(0,5))
            if point[1] > 550 :point = (point[0],randint(545,550))
            break

        points_in.append(point)
        deadline.append((randint(int(deadline_range[0][0]),int(deadline_range[0][1])),randint(int(deadline_range[1][0]),int(deadline_range[1][1]))))
    color = "black"
    draw_points(points_in)
    #random_destination()
    print(count)




def random_destination(): #随机地点
    global destination
    destination = []
    for i in range(num):
        destination.append(randint(0.1))



def get_LT(points): #获取遍历序列要求的最晚开始时间
    current_time = 0
    points.reverse()
    for i in range(len(points)):
        if i == 0 :current_time = deadline[points_in.index(points[i])][1];continue
        if current_time - cost(points[i],points[i-1]) < deadline[points_in.index(points[i])][1]:
            current_time = current_time - cost(points[i],points[i-1])
            continue
        current_time = deadline[points_in.index(points[i])][1]
    return current_time


def get_time(points): #获取遍历序列的时间
    current_time = 0
    for i in range(len(points)-1):
        if i == 0 :current_time = deadline[points_in.index(points[i])][0];continue
        if current_time + cost(points[i-1],points[i]) < deadline[points_in.index(points[i])][0] :
            current_time = deadline[points_in.index(points[i])][0]
            continue
        current_time = current_time + cost(points[i-1],points[i])
    return current_time



def randomise(): #随机数据
    global points_in
    global deadline
    global color
    clear()
    for i in range(number):
        point = (randint(1,size),randint(1,size))
        points_in.append(point)
        deadline.append((randint(int(deadline_range[0][0]),int(deadline_range[0][1])),randint(int(deadline_range[1][0]),int(deadline_range[1][1]))))
    color = "black"
    draw_points(points_in)
    random_destination()


def dist(a,b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

def cost(a,b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))/speed

        


def deadline_sort(points):
    global points_in
    global deadline
    for i in range(len(points)-1):
        for j in range(len(points)-1-i):
            if deadline[points_in.index(points[j])][1] > deadline[points_in.index(points[j+1])][1]:
                points[j],points[j+1] = points[j+1],points[j]
    return points

def time_2_opt(points):
    for i in range(len(points) - 3):
        for j in range(i+2,len(points)-1):
            if cost(points[i],points[i+1]) + cost(points[j-1],points[j]) + cost(points[j],points[j+1]) > cost(points[i],points[j]) + cost(points[j],points[i+1]) + cost(points[j-1],points[j+1]):
                temp = points[:]
                temp.pop(j)
                temp.insert(i+1,points[j])
                if get_time(temp[:i+2]) <= get_LT(temp[i+1:]): points = temp
    return points
            
    return points


def depart_points(points):
    global red_points
    red_points = []
    currenttime = 0
    temp = []
    for i in range(len(points)-1):
            j = points_in.index(points[i])
            if currenttime <= deadline[j][1] :
                if currenttime < deadline[j][0] :
                    currenttime = deadline[j][0]
                else:
                    currenttime = currenttime + cost(points[i],points[i+1])
                temp.append(points[i])
                continue
            else:
                red_points.append(points[i])

    print("分类完成")
    return temp

def distance(points):
    if len(points) == 0:
        return 0
    distance = 0
    for i in range(len(points) - 1):
        distance += dist(points[i], points[i + 1])
    return distance



def optimisation_click(algorithm):
    global points_in
    global red_points
    global color
    c.delete("black_point", "line")
    points = points_in[:]
    points = deadline_sort(points)
    for i in range(5):

        points = algorithm(points)
    points = depart_points(points)
    print(points)
    color = "black"
    draw_points(points)
    color = "red"
    draw_points(red_points)
    draw_line(points)
    v.set(int(distance(points)))
    num.set(len(points_in))
    accept.set(len(points)/len(points_in))




if __name__ == '__main__':
    root = Tk()

    root.title("Deadline TSP")
    root.resizable(0,0)

    c = Canvas(root, bg="white", width = size, height = size)

    c.configure(cursor="crosshair")
    c.pack()
    c.bind("<Button-1>", click)

    Button(root, text = "Clear", command = clear).pack(side = LEFT)
    Button(root, text = "Randomise", command = randomise).pack(side = LEFT)
    Button(root, text = "time-2-OPT", command = lambda : optimisation_click(time_2_opt)).pack(side = LEFT)
    Button(root, text = "Randomise_n", command = randomise_n).pack(side = LEFT)
    

    v = IntVar()
    num = IntVar()
    accept = IntVar()
    Label(root, textvariable = v).pack(side = RIGHT)
    Label(root, text = "dist:").pack(side = RIGHT)
    Label(root, textvariable = num).pack(side = RIGHT)
    Label(root, text = "num:").pack(side = RIGHT)
    Label(root, textvariable = accept).pack(side = RIGHT)
    Label(root, text = "Acceptance rate:").pack(side = RIGHT)

    root.mainloop()