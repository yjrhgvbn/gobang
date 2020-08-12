import role as R
import marrary as array
from Zbrist import z as zobrist
import scorePoint
import score as S
import Point
import functools

count = 0
total = 0


def fixScore(type):
    if type < S.FOUR and type >= S.BLOCKED_FOUR:
        if type >= S.BLOCKED_FOUR and type < (S.BLOCKED_FOUR + S.THREE):
            return S.THREE
        elif type >= S.BLOCKED_FOUR + S.THREE and type < S.BLOCKED_FOUR * 2:
            return S.FOUR
        else:
            return S.FOUR * 2
    return type

def starTo(point, points = False):
    if (not points or not len(points)):
        return False
    a = point
    for i in range(len(points)):
        b = points[i]
        if abs(a.x-b.x) > 4 or abs(a.y-b.y) > 4:
            return False
        if not(a.x == b.x or a.y == b.y or (abs(a.x-b.x) == abs(a.y-b.y))):
            return False
    return True

class Board:
    def init(self, size):
        self.scoreCache = [[], [
            array.create(size, size),
            array.create(size, size),
            array.create(size, size),
            array.create(size, size)
        ],[
            array.create(size, size),
            array.create(size, size),
            array.create(size, size),
            array.create(size, size)
        ]]
        self.evaluateCache = {}
        self.currentSteps = []
        self.allSteps = []
        self.stepsTail = []
        self.zobrist = zobrist
        zobrist.init(size)
        self._last = [False, False]
        self.count = 0
        self.board =[]
        for i in range(size):
            row =[]
            for j in range(size):
                row.append(0)
            self.board.append(row)
        self.comScore = array.create(size, size)
        self.humScore = array.create(size, size)
        self.initScore()

    def init2(self, tboard):
        size = 15
        self.scoreCache = [[], [
            array.create(size, size),
            array.create(size, size),
            array.create(size, size),
            array.create(size, size)
        ],[
            array.create(size, size),
            array.create(size, size),
            array.create(size, size),
            array.create(size, size)
        ]]
        self.evaluateCache = {}
        self.currentSteps = []
        self.allSteps = []
        self.stepsTail = []
        self.zobrist = zobrist
        zobrist.init(size)
        self._last = [False, False]
        self.count = 0
        self.board = tboard
        for i in range(len(self.board)):
            self.count += (self.board[i].count(1)+self.board.count(2))
        self.comScore = array.create(size, size)
        self.humScore = array.create(size, size)
        self.initScore()

    def initScore(self):
        tboard = self.board
        for i in range(len(tboard)):
            for j in range(len(tboard[i])):
                if (tboard[i][j] == R.empty):
                    if self.hasNeighbor(i, j, 2, 2):
                        cs = scorePoint.scorepoint(self, i, j, R.com)
                        hs = scorePoint.scorepoint(self, i, j, R.hum)
                        self.comScore[i][j] = cs
                        self.humScore[i][j] = hs
                elif tboard[i][j] == R.com: #对电脑打分，玩家此位置分数为0
                    self.comScore[i][j] = scorePoint.scorepoint(self, i, j, R.com)
                    self.humScore[i][j] = 0
                elif tboard[i][j] == R.hum: # 对玩家打分，电脑位置分数为0
                    self.humScore[i][j] = scorePoint.scorepoint(self, i, j, R.hum)
                    self.comScore[i][j] = 0

    def updateScore (self, p) :
        radius = 4
        mself = self
        mlen = len(self.board)

        def update(x, y, dir) :
            global scs
            global sms
            role = mself.board[x][y]
            if (role != R.reverse(R.com)):
                cs = scorePoint.scorepoint(mself, x, y, R.com, dir)
                mself.comScore[x][y] = cs
            else:
                mself.comScore[x][y] = 0
            if (role != R.reverse(R.hum)):
                hs = scorePoint.scorepoint(self, x, y, R.hum, dir)
                mself.humScore[x][y] = hs
            else:
                mself.humScore[x][y] = 0
        # 无论是不是空位 都需要更新
        # -
        for i in range(-radius,radius+1,1):
            x = p.x
            y = p.y+i
            if(y<0):
                continue
            if(y>=mlen):
                break
            update(x, y, 0)

        # |
        for i in range(-radius, radius + 1, 1):
            x = p.x+i
            y = p.y
            if(x<0):
                continue
            if(x>=mlen):
                break
            update(x, y, 1)

        # \
        for i in range(-radius, radius + 1, 1):
            x = p.x+i
            y = p.y+i
            if(x<0 or y<0):
                continue
            if(x>=mlen or y>=mlen):
                break
            update(x, y, 2)

        # /
        for i in range(-radius, radius + 1, 1):
            x = p.x+i
            y = p.y-i
            if(x<0 or y<0):
                continue
            if(x>=mlen or y>=mlen):
                continue
            update(x, y, 3)

    def put(self, tp, role):
        p=Point.point(tp.x,tp.y)
        if 'scoreHum' in tp.__dict__:
            p.scoreHum=tp.scoreHum
        if 'scoreCom' in tp.__dict__:
            p.scoreCom=tp.scoreCom
        if 'score' in tp.__dict__:
            p.score=tp.score
        p.role = role
        self.board[p.x][p.y] = role
        self.zobrist.go(p.x, p.y, role)
        self.updateScore(p)
        self.allSteps.append(p)
        self.currentSteps.append(p)
        self.stepsTail = []
        self.count +=1

    def remove(self, p):
        r = self.board[p.x][p.y]
        self.zobrist.go(p.x, p.y, r)
        self.board[p.x][p.y] = R.empty
        self.updateScore(p)
        self.allSteps.pop()
        self.currentSteps.pop()
        self.count -=1

    def evaluate(self, role):
        self.comMaxScore = 0
        self.humMaxScore = 0
        mboard = self.board
        for i in range(len(mboard)):
            for j in range(len(mboard[i])):
                if mboard[i][j] == R.com:
                    self.comMaxScore += fixScore(self.comScore[i][j])
                elif mboard[i][j] == R.hum:
                    self.humMaxScore += fixScore(self.humScore[i][j])

        result = (1 if role == R.com else -1) * (self.comMaxScore - self.humMaxScore)
        return result

    def hasNeighbor(self, x, y, distance, count):
        mboard = self.board
        mlen = len(mboard)
        startX = x-distance
        endX = x+distance
        startY = y-distance
        endY = y+distance
        for i in range(startX, endX + 1, 1):
            if i<0 or i>=mlen:
                continue
            for j in range(startY, endY + 1, 1):
                if j<0 or j>=mlen:
                    continue
                if i==x and j==y:
                    continue
                if(mboard[i][j] != R.empty):
                    count -=1
                    if(count <= 0):
                        return True
        return False

    def gen(self, role, onlyThrees=False, starSpread=False):
        if (self.count <= 0):
            return [7, 7]
        fives = []
        comfours = []
        humfours = []
        comblockedfours = []
        humblockedfours = []
        comtwothrees = []
        humtwothrees = []
        comthrees = []
        humthrees = []
        comtwos = []
        humtwos = []
        neighbors = []
        mboard = self.board[:]
        reverseRole = R.reverse(role)
        attackPoints = []
        defendPoints = []

        if starSpread:
            i = len(self.currentSteps) - 1
            while i >= 0:
                p = self.currentSteps[i]
                if (reverseRole == R.com and 'scoreCom' in p.__dict__ and p.scoreCom >= S.THREE) \
                        or (reverseRole == R.hum and 'scoreHum' in p.__dict__ and p.scoreHum >= S.THREE):
                    defendPoints.append(p)
                    break
                i -= 2

            i = len(self.currentSteps) - 2
            while i >= 0:
                p = self.currentSteps[i]
                if (role == R.com and 'scoreCom' in p.__dict__ and p.scoreCom >= S.THREE) \
                        or (role == R.hum and 'scoreHum' in p.__dict__ and p.scoreHum >= S.THREE):
                    attackPoints.append(p)
                    break
                i -= 2

            if not len(attackPoints):
                attackPoints.append(self.currentSteps[0] if self.currentSteps[0].role == role else self.currentSteps[1])
            if not len(defendPoints):
                defendPoints.append(self.currentSteps[0] if self.currentSteps[0].role == reverseRole else self.currentSteps[1])

        for i in range(len(mboard)):
            for j in range(len(mboard[i])):
                if (mboard[i][j] == R.empty):
                    if (len(self.allSteps) < 6):
                        if (not self.hasNeighbor(i, j, 1, 1)):
                            continue
                    elif (not self.hasNeighbor(i, j, 2, 2)):
                        continue
                    scoreHum = self.humScore[i][j]
                    scoreCom = self.comScore[i][j]
                    maxScore = max(scoreCom, scoreHum)
                    if (onlyThrees and maxScore < S.THREE) :
                        continue
                    p = Point.point(i,j)
                    p.scoreHum = scoreHum
                    p.scoreCom = scoreCom
                    p.score = maxScore
                    p.role = role
                    global total
                    total +=1
                    global count
                    if starSpread:
                        if maxScore >= S.FOUR:
                            count = count
                        elif maxScore >= S.BLOCKED_FOUR and starTo(self.currentSteps[len(self.currentSteps) - 1]):
                            count = count
                        elif starTo(p, attackPoints) or starTo(p, defendPoints):
                            count = count
                        else:
                            count +=1
                            continue

                    if scoreCom >= S.FIVE:
                        fives.append(p)
                    elif scoreHum >= S.FIVE:
                        fives.append(p)
                    elif scoreCom >= S.FOUR:
                        comfours.append(p)
                    elif scoreHum >= S.FOUR:
                        humfours.append(p)
                    elif scoreCom >= S.BLOCKED_FOUR:
                        comblockedfours.append(p)
                    elif scoreHum >= S.BLOCKED_FOUR:
                        humblockedfours.append(p)
                    elif scoreCom >= 2 * S.THREE:
                        comtwothrees.append(p)
                    elif scoreHum >= 2 * S.THREE:
                        humtwothrees.append(p)
                    elif scoreCom >= S.THREE:
                        comthrees.append(p)
                    elif scoreHum >= S.THREE:
                        humthrees.append(p)
                    elif scoreCom >= S.TWO:
                        comtwos.insert(0,p)#11 6
                    elif scoreHum >= S.TWO:
                        humtwos.insert(0,p)
                    else:
                        neighbors.append(p)

        if len(fives):
            return fives[:]

        if role == R.com and len(comfours):
            return comfours[:]
        if role == R.hum and len(humfours):
            return humfours[:]
        if role == R.com and len(humfours) and not len(comblockedfours):
            return humfours[:]
        if role == R.hum and len(comfours) and not len(humblockedfours):
            return comfours[:]
        fours = (comfours+humfours)[:] if role == R.com else (humfours+comfours)[:]
        blockedfours = (comblockedfours+humblockedfours)[:] if role == R.com else (humblockedfours+comblockedfours)[:]
        if len(fours):
            return (fours+blockedfours)[:]
        result = []
        if role == R.com :
            result =(comtwothrees+humtwothrees+comblockedfours+humblockedfours+comthrees+humthrees)[:]
        if role == R.hum:
            result =(humtwothrees+comtwothrees+humblockedfours+comblockedfours+humthrees+comthrees)[:]
        if len(comtwothrees) or len(humtwothrees):
            return result[:]
        if onlyThrees:
            return result[:]
        if role == R.com:
            twos = (comtwos+humtwos)[:]
        else:
            twos = (humtwos+comtwos)[:]

        def com(a, b):
                return (b.score - a.score)

        twos.sort(key=functools.cmp_to_key(com))
        result = (result+(twos if len(twos) else neighbors))[:]

        if (len(result) > 20):
            return result[0:20]
        return result[:]


board = Board()
#board.init(15)