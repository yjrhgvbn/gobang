import requests
import time

board = [[]]
blackTrun = True


def toInt(c):
    return ord(c) - ord('a')

def toChar(n):
    return chr(n + ord('a'))

def GetChess(x, y):
    if (x < 0 or x >= 15 or y < 0 or y >= 15):
        return '.'
    return board[x][y]


def Test(x, y):
    if blackTrun:
        targetChess = 'x'
    else:
        targetChess = 'o'
    print(targetChess)
    board[x][y] = '#'
    for i in range(15):
        l = ''
        for j in range(15):
            l += board[i][j] + ' '
        print(l)


def oneLineScore(line):
   # print(line)
    if blackTrun:
        targetChess = 'x'
    else:
        targetChess = 'o'
    count = len(line)
    headBlock = True
    if(line[0]!=line[1]):
        count-=1
        if(line[0]=='.'):
            headBlock = False
    tailBlock = True
    if (line[len(line)-1] != line[len(line)-2]):
        count -= 1
        if (line[len(line)-1] == '.'):
             tailBlock = False

    if(count>=5):
        if(line[1]==targetChess):   #1. 致胜棋型
            return 10000
        else:                       #2. 必须防守棋型
            return 6000
    elif count==4:
        if line[1]==targetChess and not headBlock and not tailBlock: #3. 两步致胜棋型
            return 5000
        elif line[1]!=targetChess and not headBlock and not tailBlock: #4. 两步防守棋型
            return 2500
        elif line[1]==targetChess and (not headBlock or not tailBlock): #5. 进攻棋型
            return 2000
        elif line[1]!=targetChess and (not headBlock or not tailBlock): #7. 预防棋型
            return 400
    elif count==3:
        if line[1]==targetChess and not headBlock and not tailBlock:#6. 两步进攻棋型
            return 400
        elif line[1]!=targetChess and not headBlock and not tailBlock:#7. 预防棋型
            return 400
        elif not headBlock or not tailBlock:  #8. 无效进攻防守棋型
            return 200
    elif count==2:
        if line[1]==targetChess and not headBlock and not tailBlock: #9. 布局棋型
            return 50
    return 20


def toalLineScore(line):
    if (line[3] == '.' and line[5] == '.'):
        return 0

    line1 = 'c'
    line2 = 'c'
    score = 0
    if line[3] == line[5]:
        line1=line[5]
        for i in range(3):
            if (line[5 + i] == line[6 + i]):
                line1 += line[5 + i]
            elif i == 2 or line[5 + i] != line[6 + i]:
                line1 += line[5 + i] + line[6 + i]
                break

    else:
        line1 = line[3]
        line1=line1+line[5]
        if line[5]!='.':
            line2=line[5]
            line2=line[3]+line2
            for i in range(3):
                if i == 2 or line[5 + i] != line[6 + i]:
                    line2 = (line2 + line[5 + i] + line[6 + i])
                    break
                elif (line[5 + i] == line[6 + i]):
                    line2 += line[5 + i]
            score+=oneLineScore(line2)
    if line[3] != '.':
        for i in range(3):
            if i == 2 or line[2 - i] != line[3 - i]:
                line1 = (line[2 - i] + line[3 - i] + line1)
                break
            elif (line[2 - i] == line[3 - i]):
                line1 = line[3 - i] + line1

        score+=oneLineScore(line1)
    return score



def pointscore(x,y):
    dir = [1, 0, -1, 1]
    score = 0
    for j in range(4):  # 一点的四条线
        if board[x][y] == '.':
            line = board[x][y]
            for k in range(1, 5):
                line = GetChess(x - dir[j] * k, y - dir[(j + 1) % 4] * k) + line + GetChess(x + dir[j] * k,
                                                                                            y + dir[(j + 1) % 4] * k)
            #print(line)
            #print(toalLineScore(line))
            score += toalLineScore(line)
        else:
            continue
    #print("")
    return score

#inputChesses = ["hhifhjigkhjghghiihjhkjjijjij", "hhigjhihjgiiifhgjijfkhkeli", "hhjhiijjkijijkjgjfkhijiflihegdlh", "hhkhlhihkgjimijfnjoklgjhjgigmgnglfli", "hhjhihjiijjjjgjkjliihigjkgigkflehf", "edfefdgdeeefhcdffccfffdddegbgcecicjchb", "gheifhiihhihhiijighg", "hhjhiijgghjjjkjijfkjig", "ggffhggfhffgiefhfeheidehdidhgheg", "hhjhiijgghjjjkjijfkjiggiijih", "hhjhiijgghjjjkjijfkjiggi", "ghhihhhggiggihfhigfjiiifjh", "hhggfhghifgigfgjgkhfhkhiijfgjikh", "hhihgihijgiiigjffjekgghggjghijhjgkiffijekdkfgl", "hhjhihjiijjjjgjkjlii", "hhjhihjiijjjjgjkjliihigjkgigkflehfhgifjf", "ghhihhhggiggihfhigfjiiifjhkhjgjfhfgekfijkg"]

def bestChess(inputChess):
    if inputChess=="":
        return 'ff'
    fin = ''
    if inputChess != "":
        for i in range(15):
            for j in range(15):
                board[i][j]=('.')
        global blackTrun
        for i in range(0, len(inputChess), 2):
            if (blackTrun):
                board[toInt(inputChess[i])][toInt(inputChess[i + 1])] = 'x'
            else:
                board[toInt(inputChess[i])][toInt(inputChess[i + 1])] = 'o'
            blackTrun = not blackTrun
        maxscore = 0
        for x in range(15):
            for y in range(15):
                score = pointscore(x,y)
                if score>maxscore:
                    px = x
                    py = y
                    maxscore =score
        #print(pointscore(px,py))
        #print(pointscore(8, 7))
        #Test(px,py)
        fin+=toChar(px)+toChar(py)
        #fin+=str(px)+str(py)+','

    return fin






def joinGame():
    import requests
    data = {
        'user': '辣鸡中的垃圾',
        'password': '0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14'
        , 'data_type': 'json'
    }
    response = requests.get("http://202.207.12.223:8000/join_game", params=data)
    print(response.json())
    return response.json()['game_id']

def playGame(game_id,c):
    straa = 'http://202.207.12.223:8000/play_game/' + str(
        game_id) + '/?user=辣鸡中的垃圾&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&coord=' + c

    response = requests.get(straa)
    #print(response.url)
    print(response.json())

def check_game(game_id):
    import requests
    response = requests.get("http://202.207.12.223:8000/check_game/"+str(game_id))
    #print(response.url)
    print(response.json())
    return response.json()


for i in range(15):
    board.append([])
    for j in range(15):
        board[i].append('.')

#print(bestChess("aabbcceeffgghh"))

#http://202.207.12.223:8000/play_game/14401/?user=0171123127&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&coord=%27aa%27
win = 0
los = 0
while True:
    game_id = joinGame()
    gjson = check_game(game_id)
    creator_name = gjson['creator_name']
    if str(creator_name) != '辣鸡中的垃圾':
        blackTrun=False
    else:
        blackTrun=True
    while True:
        time.sleep(6)
        gjson = check_game(game_id)
        #if gjson[]
        if (gjson['is_success'] == True):
            if gjson['current_turn'] == '辣鸡中的垃圾':
                if len(gjson['board'])==0:
                    playGame(game_id, 'hh')
                else:
                    c = bestChess(gjson['board'])
                    #print(c)
                    playGame(game_id,c)
            if gjson['winner'] != 'None':
                if gjson['winner'] == '辣鸡中的垃圾':
                    win += 1
                else:
                    los += 1
                print('win count:' + str(win) + '   los count:' + str(los))
                break
        else:
            break

