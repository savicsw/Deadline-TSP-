from tkinter import *
from random import *
from math import sqrt
from point import *
import operator
import re
import numpy
import numpy as np
import os

class TSP:
    def __init__(self):
        #初始化points数据..
        self.start = point()    #起点
        self.start.loc = (110,136)
        self.start.deadline = (0,3600)
        self.end = point()      #终点
        self.end.deadline = (0,3600)
        self.end.loc = (487,535)
        self.list = []      #遍历点
        self.color = "black" #初始颜色 fill填充oval的颜色
        self.speed = 4    #速度
        for i in range(50):
            self.list.append(point())
            #print("第",i+1,"个点坐标：",self.list[i].loc,",deadline:",self.list[i].deadline)
        
        window = Tk() #创建窗口
        window.title("TSP Demo") #给窗口命名

        #在窗口画布
        self.canvas = Canvas(window, width = 650, height = 650, bg = "white")
        self.canvas.pack()

        Button(window, text = "Random", command = self.random).pack(side = LEFT)
        #Button(root, text = "Randomise", command = randomise).pack(side = LEFT)
        Button(window, text = "nearest_neighbour", command = self.nearest_neighbour).pack(side = LEFT)
        Button(window, text = "test", command = self.test).pack(side = LEFT)
        #Button(root, text = "display", command = display).pack(side = LEFT)
    

        #self.v = IntVar()
        #self.num = IntVar()
        self.accept = IntVar()
        #Label(window, textvariable = self.v).pack(side = RIGHT)
       # Label(window, text = "dist:").pack(side = RIGHT)
      #  Label(window, textvariable = self.num).pack(side = RIGHT)
      #  Label(window, text = "num:").pack(side = RIGHT)
        Label(window, textvariable = self.accept).pack(side = RIGHT)
        Label(window, text = "Acceptance").pack(side = RIGHT)





        #创建事件循环直到关闭主窗口
        window.mainloop()

    

    def random(self):
        self.list = []
        self.clear()
        os.system('cls')
        for i in range(50):
            self.list.append(point())
        self.color = "black"
        self.draw_points()
    
    def clear(self):
        self.canvas.delete("point","line")

    def draw_points(self):
        for point in self.list:
            self.canvas.create_oval(point.loc[0]-3, point.loc[1]-3, point.loc[0]+3, point.loc[1]+3, fill = self.color, tags = "point")

    def draw_line(self):
        temp = [self.start]
        temp = temp + self.list
        temp.append(self.end)
        for i in range(len(temp)-1):
            self.canvas.create_line(temp[i].loc,temp[i+1].loc)

    def finash_line(self,points,time):
        self.clear()
        self.canvas.create_oval(points[0].loc[0]-3, points[0].loc[1]-3, points[0].loc[0]+3, points[0].loc[1]+3, fill = "green", tags = "point")
        print("起点坐标（绿色）:",points[0].loc,"    Deadline说明：t1-t2中，t1为退房时间，t2为根据航班时间确定是行李最晚提取时间")
        self.canvas.create_oval(self.end.loc[0]-3, self.end.loc[1]-3, self.end.loc[0]+3, self.end.loc[1]+3, fill = "yellow", tags = "point")
        print("终点坐标（黄色）:",self.end.loc)
        time_arrival = time
        time_leave = time
        arrival = 0
        count = 0
        for i in range(len(points)):
            if i == 0 :continue
            if time_leave + self.dist(points[arrival],points[i])/self.speed < points[i].deadline[1]:
                self.color = "black"
                count = count + 1
                self.canvas.create_oval(points[i].loc[0]-3, points[i].loc[1]-3, points[i].loc[0]+3, points[i].loc[1]+3, fill = self.color, tags = "point")
                self.canvas.create_line(points[arrival].loc,points[i].loc,tags = "line")
                time_arrival = time_leave + self.dist(points[arrival],points[i])/self.speed
                time_leave = time_leave + self.cost(points[arrival],points[i],time_leave)
                arrival = i
                print("第",i,"个点坐标：",points[i].loc,",Deadline:",int(points[i].deadline[0]/60)+8,":",int(points[i].deadline[0]%60),"-",int(points[i].deadline[1]/60)+8,":",int(points[i].deadline[1]%60),"到达时间：",int(time_arrival/60+8),":",int(time_arrival%60),"离开时间：",int(time_leave/60+8),":",int(time_leave%60))

            else:
                self.color = "red"
                self.canvas.create_oval(points[i].loc[0]-3, points[i].loc[1]-3, points[i].loc[0]+3, points[i].loc[1]+3, fill = self.color, tags = "point")
                print("第",i,"个点不满足deadline，坐标：",points[i].loc,",Deadline:",int(points[i].deadline[0]/60)+8,":",int(points[i].deadline[0]%60),"-",int(points[i].deadline[1]/60)+8,":",int(points[i].deadline[1]%60))
        self.accept.set(int(count))

    def finash_line_end(self,points,time):
        self.clear()
        self.canvas.create_oval(points[0].loc[0]-3, points[0].loc[1]-3, points[0].loc[0]+3, points[0].loc[1]+3, fill = "green", tags = "point")
        print("起点坐标（绿色）:",points[0].loc,"    Deadline说明：t1-t2中，t1为退房时间，t2为根据航班时间确定是行李最晚提取时间")
        self.canvas.create_oval(self.end.loc[0]-3, self.end.loc[1]-3, self.end.loc[0]+3, self.end.loc[1]+3, fill = "yellow", tags = "point")
        print("终点坐标（黄色）:",self.end.loc)
        time_arrival = time
        time_leave = time
        arrival = 0
        count = 0
        for i in range(len(points)):
            if i == 0 :continue
            if time_leave > self.end.deadline[1]:
                self.canvas.create_line(points[arrival].loc,self.end.loc,tags = "line")
                self.color = "red"
                self.canvas.create_oval(points[i].loc[0]-3, points[i].loc[1]-3, points[i].loc[0]+3, points[i].loc[1]+3, fill = self.color, tags = "point")
                continue
            if time_leave + self.dist(points[arrival],points[i])/self.speed < points[i].deadline[1]:
                self.color = "black"
                count = count + 1
                self.canvas.create_oval(points[i].loc[0]-3, points[i].loc[1]-3, points[i].loc[0]+3, points[i].loc[1]+3, fill = self.color, tags = "point")
                self.canvas.create_line(points[arrival].loc,points[i].loc,tags = "line")
                time_arrival = time_leave + self.dist(points[arrival],points[i])/self.speed
                time_leave = time_leave + self.cost(points[arrival],points[i],time_leave)
                arrival = i
                print("第",i,"个点坐标：",points[i].loc,",Deadline:",int(points[i].deadline[0]/60)+8,":",int(points[i].deadline[0]%60),"-",int(points[i].deadline[1]/60)+8,":",int(points[i].deadline[1]%60),"到达时间：",int(time_arrival/60+8),":",int(time_arrival%60),"离开时间：",int(time_leave/60+8),":",int(time_leave%60))

            else:
                self.color = "red"
                self.canvas.create_oval(points[i].loc[0]-3, points[i].loc[1]-3, points[i].loc[0]+3, points[i].loc[1]+3, fill = self.color, tags = "point")
                print("第",i,"个点不满足deadline，坐标：",points[i].loc,",Deadline:",int(points[i].deadline[0]/60)+8,":",int(points[i].deadline[0]%60),"-",int(points[i].deadline[1]/60)+8,":",int(points[i].deadline[1]%60))
        self.accept.set(int(count))





    



    def get_LT(points):
        current_time = 0
        points.reverse()
        for i in range(len(points)-1):
            if i == 0 : current_time = points[i].deadline[1];continue
            if current_time - cost(points[i-1].loc,points[i].loc) < points[i].deadline[1] : current_time = current_time - cost(points[i-1].loc,points[i].loc);continue
            current_time = points[i].deadline[1]
        return current_time

    def cost(self,a,b,time):
        d1 = sqrt(pow(a.loc[0] - b.loc[0], 2) + pow(a.loc[1] - b.loc[1], 2))/self.speed
        if time + d1 < b.deadline[0]:
            return b.deadline[0] - time
        return d1

    def get_time(self,points,time):
        current_time = time
        for i in range(len(points)-1):
            current_time = cost(points[i].loc,points[i+1].loc) + current_time
            if current_time < points[i+1].deadline[0]: current_time = points[i+1].deadline[0]
        return current_time
        
    def quicksort(self,points):
        key = 0
        i = 0
        j = len(points)
        while i < j :
            while i < j and key <= j:
                if points[key].deadline[1] > points[j].deadline[1] :
                    points[i],points[j] = points[j],points[i]
                    i = i + 1
                    key = j
                    break
                j = j - 1
            while i < j and key >= i:
                if points[key].deadline[1] < points[i].deadline[1] :
                    points[i],points[j] = points[j],points[i]
                    j = j - 1
                    key = i
                    break
                i = i + 1
        return points

    def get_ETpoint(self,points):     #确定最早需要送达的订单
        i = 0
        for point in points:
            if point.deadline[1] < points[i].deadline[1]:
                i = points.index(point)
        return points[i]

    def get_points(points,time):
        temp = []
        for point in points:
            if point.deadline[0] < time: temp.append(point)
        return temp


    def deal_points(self):
        temp = []
        temp.append(self.start)
        temp.append(self.end)
        for i in range(len(self.list)):
            for j in range(1,len(temp)):
                temp.insert(j,self.list[i])
                if self.Accept(temp):
                    if len(temp) > 3:
                        temp = self.time_2_opt(temp)
                else: temp.remove(self.list[i])
        return temp




     

    def sumcost(self,points,time):
        sum = 0
        time_arrival = time
        time_leave = time
        for i in range(1,len(points)-1):
            time_arrival = self.cost(points[i-1],points[i]) + time_arrival
            sum = sum + self.cost(points[i-1],points[i])
            if time_arrival < points[i].deadline[0]:time_leave = points[i].deadline[0];sum = sum + time_leave - time_arrival
            else:time_leave = time_arrival
        return sum


    def Accept(self,points):
        time_arrival = 0
        time_leave = 0
        for i in range(1,len(points)-1):
            if time_leave + self.cost(points[i-1],points[i]) < points[i].deadline[1]:
                time_arrival = time_leave + self.cost(points[i-1],points[i])
                if time_arrival < points[i].deadline[0]: time_leave = points[i].deadline[0]
                else : time_leave = time_arrival
            else:
                return False
        return True

    def get_num(self,points,time):
        count = 0
        for i in range(len(points)-1):
            time = time + self.cost(points[i],points[i+1],time)
            if time <= points[i+1].deadline[1]: count = count + 1
        return count


    def dist(self,a,b):
        return sqrt(pow(a.loc[0] - b.loc[0], 2) + pow(a.loc[1] - b.loc[1], 2))

    def  DIST(self,a,b,time):
        d1 = sqrt(pow(a.loc[0] - b.loc[0], 2) + pow(a.loc[1] - b.loc[1], 2))/self.speed
        return d1+(self.cost(a,b,time)-d1)*0.5



    def nearest_neighbour(self):
        time = 0
        i = 0
        p = [self.start]
        points = self.list[:]
        for i in range(len(points)):
            temp = points[0]
            for point in points:
                if self.dist(p[i],point) < self.dist(p[i],temp): temp = point
            points.remove(temp)
            p.append(temp)
            
        self.clear()
        self.finash_line(p,0)

    def test(self):
        time = 0
        ETpoint = self.get_ETpoint(self.list)
        points = []
        for point in self.list:
            if point.deadline[0] < ETpoint.deadline[1]:
                points.append(point)
        print("最早要求送达时间为：",int(ETpoint.deadline[1]/60 + 10),":",int(ETpoint.deadline[0]%60),"在此之前可取得订单共",len(points),"件")
        self.end.deadline = (0,int(ETpoint.deadline[1]+60))
        p = [self.start]
        for i in range(len(points)):
            temp = points[0]
            for point in points:
                if self.dist(p[i],point) < self.dist(p[i],temp): temp = point
            points.remove(temp)
            p.append(temp)
            
        self.clear()
        self.finash_line_end(p,0)





            

    









TSP()