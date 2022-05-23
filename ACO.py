import random
import os
import matplotlib.pyplot as plt
from math import *

os.system('cls')

num_city = 26 # 城市数量
num_ant = 50 # 蚂蚁数量
rho = 0.5 # 信息素挥发率
kesai = 0.5 # 信息素负反馈调节率
alpha = 1 # 信息素重要程度
beta = 3 # 启发信息重要程度
q = 100 # 信息素增强系数
city = range(num_city) # 城市数组
distance = [] # 城市距离矩阵
pheromone = [] # 信息素矩阵
pheromone0 = q/(num_city*(num_city-1)) # 信息素含量基础值
maxiter = 20 # 最大迭代次数


def set_distance():
    """初始化距离矩阵"""
    fname = 'Data\\distance.txt'
    with open(fname, encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            l = line.split()
            for i in range(len(l)):
                l[i] = float(l[i])
            distance.append(l)

def set_pheromone():
    """初始化信息素矩阵"""
    for i in range(num_city):
        pheromone.append([])
        for j in range(num_city):
            p = 0 if i==j else pheromone0
            pheromone[i].append(p)

def roulette_select(current_city,unvisit_list):
    """轮盘赌选法"""
    possibility = []
    total_possibility = 0
    for next_city in unvisit_list:
        # 下一节点概率(未归一) = 信息素^alpha * (1/距离)^(beta) 
        p = pow(pheromone[current_city][next_city],alpha)*pow((1/distance[current_city][next_city]),beta)
        possibility.append(p)
        total_possibility += possibility[-1]
        possibility[-1] = total_possibility 

    city = [0 for i in range(len(unvisit_list))] # 记录轮盘赌选到某一城市的次数
    for num_rand in range(5): # 轮盘转动次数
        rand = random.uniform(0,total_possibility)
        for i in range(len(possibility)):
            if rand <= possibility[i]:
                city[i] += 1
                break
    m = max(city)
    next_city = unvisit_list[city.index(m)]
    return next_city

def update_pheromone(list):
    """信息素矩阵更新"""
    path_list = []
    for k in range(len(list)-1):
        path_list.append((list[k],list[k+1]))
    for i in range(num_city):
        for j in range(num_city):
            if (i,j) in path_list: # 该路径在最短路线里:信息素增强
                pheromone[i][j] = (1-rho)*pheromone[i][j] + q*rho/len(path_list)
            else:   # 该路径不在最短路线里:信息素挥发
                pheromone[i][j] = (1-rho)*pheromone[i][j]

def ant_optimize(best_list,min_distance):
    """蚁群优化"""
    for ant in range(num_ant):
        next_visit = city[0] # 下一个访问的城市,初始化为城市0
        unvisit_list = list(range(num_city)) # 未访问城市列表
        unvisit_list.remove(next_visit) 
        visit_list = [next_visit] # 已访问城市列表
        distance_sum = 0 # 走过的总路程
        while True:
            # 所有城市访问完,返回起始城市
            if len(unvisit_list) is 0:
                distance_sum += distance[visit_list[-1]][city[0]]
                visit_list.append(city[0])
                break
            # 存在未访问城市时,根据信息素量选择下一访问城市(轮盘赌选法)
            next_visit = roulette_select(visit_list[-1],unvisit_list)
            # 蚂蚁每走过一条路径,会由负反馈调整该路径上的信息素含量(防止蚁群只走一条路线,陷入局部极小值)
            pheromone[visit_list[-1]][next_visit] = (1-kesai)*pheromone[visit_list[-1]][next_visit] + kesai*pheromone0
            unvisit_list.remove(next_visit)
            visit_list.append(next_visit)
            distance_sum += distance[visit_list[-2]][visit_list[-1]]
        
        if distance_sum < min_distance:
            min_distance = distance_sum
            best_list = visit_list

    return (best_list,min_distance)

def plot(distance_list):
    """绘制搜索过程最短路程变化"""
    iter = range(len(distance_list))
    plt.title('Search Process')
    plt.xlabel('Iteration')
    plt.ylabel('Min distance')
    plt.plot(iter,distance_list,color='r')
    plt.show()



set_pheromone()
set_distance()

min_distance = 1e5 #  最短路程
best_list = [] # 最优路线
distance_list = [] # 记录最短路程变化
for iter in range(maxiter):
    (best_list,min_distance) = ant_optimize(best_list,min_distance)
    distance_list.append(min_distance)
    update_pheromone(best_list)

plot(distance_list)
print("最优路线:" + str(best_list))
print("最短路程:" + str(min_distance))
