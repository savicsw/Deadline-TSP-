
from tkinter import *
from random import *
from math import sqrt
import operator
import re


points_in = []
points = []
size = 550
deadline = []
TimeList = []
speed = 10
number = 50

def click(event):
    draw_point(event.x, event.y)
    points_in.append((event.x, event.y))

   # coordinate(points_in[len(points_in)-1])

    
def draw_point(x,y):
    c.create_oval(x-3, y-3, x+3, y+3, fill="black", tags = "point")


def coordinate(point):
    temp = re.findall(r'd+',point)
    print(temp)
    return temp

    
def draw_points():
    c.delete("point", "line");
    map(lambda point: draw_point(point[0], point[1]), points)
    
def draw_line():
    global points
    c.delete("line")
    c.create_line(points, tags="line")
  
def clear():
    global points
    global points_in
    points = []
    points_in = []
    c.delete("point", "line");
    
def randomise():
    global points
    global points_in
    points_in = []
    c.delete("point", "line")
    for i in range(number):
        x = randint(1,size)
        y = randint(1,size)
        draw_point(x, y)
        points_in.append((x, y))

    for i in range(number):
        temp = []
        deadline.append((randint(30,450),randint(540,960)))
        for j in range(number):
            temp.append(cost(points_in[i],points_in[j]))
        TimeList.append(temp)

   # print(deadline)
   # print(TimeList)
#     draw_points()

def Time_2_opt(points):
    CurrenTime = 0
    CurrenDistence = 0
    for i in range(len(points) - 1):
        for j in range(i + 2, len(points) - 1):
            if dist(points[i], points[i+1]) + dist(points[j], points[j+1]) > dist(points[i], points[j]) + dist(points[i+1], points[j+1]):          
                if cost(points[i],points[j]) + CurrenTime <= DT(points[j]):
                  # if cost(points[i+2],cost(i+1)) + cost(points[i],points[j]) + CurrenTime < DT(points[i+1]):
                        points[i+1:j+1] = reversed(points[i+1:j+1])
        CurrenTime = CurrenTime + cost(points[i],points[i+1])
    return points


def TimeSort(points):
    for i in range(len(points)-1) :
        for j in range(len(points)-i-1):
            if DT(points[j]) > DT(points[j+1]):
                points[j],points[j+1] = points[j+1],points[j]

    print(points)
    return points


def draw_red(points):
    CurrenTime = 0
    num = 0
    for i in range(len(points)):
       # print(i)
        if CurrenTime > DT(points[i]):
            c.create_oval(int(points[i][0])-3, int(points[i][1])-3, int(points[i][0])+3, int(points[i][1])+3, fill="red", tags = "point")
            num += 1
        if i < len(points)-1 :
            CurrenTime = CurrenTime + cost(points[i],points[i+1])

    return num


def DT(point):
    global deadline
    print(deadline[loc(point)][1])
    return  deadline[loc(point)][1]

def check(points):
    for point in points:
        if distence(points[:points.index(point)+1])/speed > DT(point):
            return False
    return True

def cost(a,b):
    d = dist(a,b)
    return d/speed

def loc(point):
    return points_in.index(point)

def delay(points):
    DelayTime = 0
    CurrenTime = 0
    for i in len(points)-1:
        if CurrenTime+cost(points[i],points[i+1]) <= deadline[loc[points[i+1]]]:
            CurrenTime = deadline[loc[points[i+1]]]
        else :
            DelayTime = DelayTime + (CurrenTime+cost(points[i],points[i+1]) - deadline[loc[points[i+1]]])
            CurrenTime = CurrenTime + cost(points[i],points[i+1])
    return DelayTime

def nearest_neighbour_algorithm(points):
    points = points_in[:]
    if len(points) == 0:
        return []
    #current = choice(points)
    current = points[0]
    nnpoints = [current]
    points.remove(current)
    while len(points) > 0:
        next = points[0]
        for point in points:
            if dist(current, point) < dist(current, next):
                next = point      
        nnpoints.append(next)
        points.remove(next)
        current = next
    return nnpoints

def two_opt(points):
    for i in range(len(points) - 1):
        for j in range(i + 2, len(points) - 1):
            if dist(points[i], points[i+1]) + dist(points[j], points[j+1]) > dist(points[i], points[j]) + dist(points[i+1], points[j+1]):          points[i+1:j+1] = reversed(points[i+1:j+1])
    return points


def time_insert(points):
    if len(points) <= 1: return points
    temp = [points[0]]
    D =  0
    list = []
    distence = 9999999999999999999
    state = False
    for point in points:
        for i in temp[:len(temp)-2]:
            if distance(temp[:temp.index(i)+1]) < DT(point):
                D = temp.index(i)
            else: break
        for j in range(D+2):
            list = temp[:len(temp)-2]
            list.insert(j,point)
            if check(list):
                state = True
                if distence > distence(list):
                    distence = didistence(list)
                    temp = list[:]
                continue
            else: continue

            



        




def three_opt(points):
    points = points_in[:]
    for i in range(len(points) - 1):
        for j in range(i + 2, len(points) - 1):
            for k in range(j + 2, len(points) - 1):
                way = 0
                current = dist(points[i], points[i+1]) + dist(points[j], points[j+1]) + dist(points[k], points[k+1])
                if current >  dist(points[i], points[i+1]) + dist(points[j], points[k]) + dist(points[j+1], points[k+1]):
                    current = dist(points[i], points[i+1]) + dist(points[j], points[k]) + dist(points[j+1], points[k+1])
                    way = 1
                if current >  dist(points[i], points[j]) + dist(points[i+1], points[j+1]) + dist(points[k], points[k+1]):
                    current = dist(points[i], points[j]) + dist(points[i+1], points[j+1]) + dist(points[k], points[k+1])
                    way = 2
                if current >  dist(points[i], points[j]) + dist(points[i+1], points[k]) + dist(points[j+1], points[k+1]):
                    current = dist(points[i], points[j]) + dist(points[i+1], points[k]) + dist(points[j+1], points[k+1])
                    way = 3
                if current >  dist(points[i], points[j+1]) + dist(points[k], points[i+1]) + dist(points[j], points[k+1]):
                    current = dist(points[i], points[j+1]) + dist(points[k], points[i+1]) + dist(points[j], points[k+1])
                    way = 4
                if current >  dist(points[i], points[j+1]) + dist(points[k], points[j]) + dist(points[i+1], points[k+1]):
                    current = dist(points[i], points[j+1]) + dist(points[k], points[j]) + dist(points[i+1], points[k+1])
                    way = 5
                if current >  dist(points[i], points[k]) + dist(points[j+1], points[i+1]) + dist(points[j], points[k+1]):
                    current = dist(points[i], points[k]) + dist(points[k], points[i+1]) + dist(points[j], points[k+1])
                    way = 6
                if current >  dist(points[i], points[k]) + dist(points[j+1], points[j]) + dist(points[i+1], points[k+1]):
                    current = dist(points[i], points[k]) + dist(points[j+1], points[j]) + dist(points[i+1], points[k+1])
                    way = 7
                if way == 1:
                    points[j+1:k+1] = reversed(points[j+1:k+1])
                elif way == 2:
                    points[i+1:j+1]= reversed(points[i+1:j+1])
                elif way == 3: 
                    points[i+1:j+1],points[j+1:k+1] = reversed(points[i+1:j+1]),reversed(points[j+1:k+1])
                elif way == 4:
                    points = points[:i+1] + points[j+1:k+1] + points[i+1:j+1] + points[k+1:]      
                elif way == 5:
                    temp = points[:i+1] + points[j+1:k+1]
                    temp += reversed(points[i+1:j+1])
                    temp += points[k+1:]
                    points = temp
                elif way == 6:
                    temp = points[:i+1]
                    temp += reversed(points[j+1:k+1])
                    temp += points[i+1:j+1]
                    temp += points[k+1:]
                    points = temp
                elif way == 7:
                    temp = points[:i+1]
                    temp += reversed(points[j+1:k+1])
                    temp += reversed(points[i+1:j+1])
                    temp += points[k+1:]
                    points = temp
                    
    return points

def dist(a, b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

def distance(points):
    if len(points) == 0:
        return 0
    distance = 0
    for i in range(len(points) - 1):
        distance += dist(points[i], points[i + 1])
    return distance

def optimisation_click(algorithm):
    global points
    global points_in
    points = points_in[:]
    for i in range(1):

        points = algorithm(points)
    
    draw_line()
    nnum = draw_red(points)
    v.set(int(distance(points)))
    num.set(len(points))
    noaccept.set(nnum)


if __name__ == '__main__':
    root = Tk()

    root.title("TSP - Visualizer [Nemanja Trifunovic br. ind.:346/2010]")
    root.resizable(0,0)

    c = Canvas(root, bg="white", width = size, height = size)

    c.configure(cursor="crosshair")
    c.pack()
    c.bind("<Button-1>", click)

    Button(root, text = "Clear", command = clear).pack(side = LEFT)
    Button(root, text = "Randomise", command = randomise).pack(side = LEFT)
    #Button(root, text = "Nearest Neighbour", command = lambda : optimisation_click(nearest_neighbour_algorithm)).pack(side = LEFT)
    Button(root, text = "2-OPT", command = lambda : optimisation_click(two_opt)).pack(side = LEFT)
    #Button(root, text = "3-OPT", command = lambda : optimisation_click(three_opt)).pack(side = LEFT)
    Button(root, text = "time-2-OPT", command = lambda : optimisation_click(Time_2_opt)).pack(side = LEFT)
    Button(root, text = "TimeSort", command = lambda : optimisation_click(TimeSort)).pack(side = LEFT)
    

    v = IntVar()
    num = IntVar()
    noaccept = IntVar()
    Label(root, textvariable = v).pack(side = RIGHT)
    Label(root, text = "dist:").pack(side = RIGHT)
    Label(root, textvariable = num).pack(side = RIGHT)
    Label(root, text = "num:").pack(side = RIGHT)
    Label(root, textvariable = noaccept).pack(side = RIGHT)
    Label(root, text = "noaccept:").pack(side = RIGHT)

    root.mainloop()
          
