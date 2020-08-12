#from math import *
#import numpy as np
import  requests
import time

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

list1 = []  # AI
list2 = []  # human
list3 = []  # all

list_all = []  # 整个棋盘的点
next_point = [0, 0]

ratio = 1
DEPTH = 3
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


def ai():
    global cut_count
    cut_count = 0
    global search_count
    search_count = 0
    negamax(True, DEPTH, -99999999, 99999999)
    print("本次共剪枝次数：" + str(cut_count))
    print("本次共搜索次数：" + str(search_count))
    return next_point[0], next_point[1]


def negamax(is_ai, depth, alpha, beta):
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)
    for next_step in blank_list:

        global search_count
        search_count += 1

        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:

            #print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            #print(list3)
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝点
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


def order(blank_list):
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False


# 评估函数
def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    score_all_arr = []
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score


def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0
    max_score_shape = (0, None)

    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                #if tmp_shap5 == (1,1,1,1,1):
                #    print('wwwwwwwwwwwwwwwwwwwwwwwwwww')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False

def toChar(n):
    return chr(n + ord('a'))

def toInt(c):
    return ord(c) - ord('a')


import requests
def joinGame():
    data = {
        'user': '0171123127',
        'password': '0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14'
        , 'data_type': 'json'
    }
    response = requests.get("http://202.207.12.223:8000/join_game", params=data)
    print(response.json())
    print(response.url)
    return response.json()['game_id']

def playGame(game_id,c):
    straa = 'http://202.207.12.223:8000/play_game/'+str(game_id)+'/?user=0171123127&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&coord='+c
    response = requests.get(straa)
    print('input'+c)
    print(response.url)
    print(response.json())
    return response.json()
def check_game(game_id):
    import requests
    response = requests.get("http://202.207.12.223:8000/check_game/"+str(game_id))
    #print(response.url)
    print(response.json())
    return response.json()

def main():

    for i in range(COLUMN+1):
        for j in range(ROW+1):
            list_all.append((i, j))

    change = 0  #0 o : 1 x
    m = 0
    n = 0

    game_id = joinGame()
    gjson = check_game(game_id)
#a b c d e f g h i j k l n m
#0 1 2 3 4 5 6 7 8 9
    size = -1
    while True:
        time.sleep(6)
        # if gjson[]
        gjson = check_game(game_id)
        if size != len(gjson['board']):
            if gjson['current_turn'] == '0171123127':
                #print("(len(gjson['board']):"+str(len(gjson['board'])))
                last_step = gjson['last_step']
                if (len(last_step) != 0):
                    list2.append((toInt(last_step[0]), toInt(last_step[1])))
                    list3.append((toInt(last_step[0]), toInt(last_step[1])))
                if(len(gjson['board'])==0):
                    c=(7,7)
                else:
                    c = ai()
                print(c)

                if playGame(game_id, toChar(c[0])+toChar(c[1]))['is_success'] == True:
                    list1.append(c)
                    list3.append(c)
                    print(list1)
                    print(list2)
            else:

                print(list1)
                print(list2)
            size = len(gjson['board'])




main()