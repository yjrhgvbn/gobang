from board import board
from negamax import deepAll as m
import role
import Point
import role as R
import requests
import time

def test(b):
    for i in b:
        s = ''
        for j in i:
            s+=str(j)+' '
        print(s)
    print('----------------------------')

def cp(x,y):
    p=Point.point
    p.x=x
    p.y=y
    board.put(p,R.com)
    test(board.board)
def hp(x,y):
    p = Point.point
    p.x=x
    p.y=y
    board.put(p,R.hum)
    test(board.board)
def cs():
    if (len(board.allSteps) > 1):
        p = m(R.com, 8)
        board.put(p, R.com)
    test(board.board)

def joinGame():
    data = {
        'user': '我是小号',
        'password': '0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14'
        , 'data_type': 'json'
    }
    response = requests.get("http://202.207.12.223:8001/join_game", params=data)
    #print(response.json())
    #print(response.url)
    return response.json()['game_id']

def playGame(game_id,c):
    straa = 'http://202.207.12.223:8001/play_game/'+str(game_id)+'/?user=我是小号&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&coord='+c
    response = requests.get(straa)
    #print('input'+c)
    #print(response.url)
    #print(response.json())
    return response.json()
def check_game(game_id):
    import requests
    response = requests.get("http://202.207.12.223:8001/check_game/"+str(game_id))
    #print(response.url)
    print(response.json())
    return response.json()
def toChar(n):
    return chr(n + ord('a'))

def toInt(c):
    return ord(c) - ord('a')


def main():
    e=False
    winname =[]
    win = 0
    los = 0
    while True:
        if e:
            break
        board.init(15)
        #print(board.board)
        game_id = joinGame()
        size = -1
        while True:
            time.sleep(6)
            gjson = check_game(game_id)
            if (gjson['is_success'] == True):
                if gjson['current_turn'] == '我是小号':
                    #print("(len(gjson['board']):"+str(len(gjson['board'])))
                    p = Point.point
                    last_step = gjson['last_step']
                    if (len(last_step) != 0):
                        p.x=toInt(last_step[0])
                        p.y =toInt(last_step[1])
                        board.put(p,R.hum)
                    if(len(gjson['board'])==0):
                        p.x = 7
                        p.y = 7
                    #elif len(gjson['board'])==2:
                    #    p.x = toInt(last_step[0])+1
                    #    p.y = toInt(last_step[1])+1
                    else:
                        s=time.time()
                        p = m(R.com, 7)
                        print('spend time:'+str(time.time()-s))
                    if playGame(game_id, toChar(p.x)+toChar(p.y))['is_success'] == True:
                        board.put(p, R.com)
                if gjson['winner']!='None':
                    winname.append(gjson['winner'])
                    if gjson['winner'] == '我是小号':
                        win+=1
                    else:
                        los+=1
                    e=True
                    print('win count:'+str(win) +'   los count:'+str(los))
                    print('winplyers:' + str(winname))
                    break
            else:
                break


main()