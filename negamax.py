from board import board
import score as SCORE
import role as R
import mymath
import functools

MAX = SCORE.FIVE*10
MIN = -1*MAX
count=0
PVcut=0
ABcut=0
cacheCount=0
cacheGet=0
Cache={}
class Score:
    def __init__(self):
        self.score=0
        self.steps=[]
        self.step=0

class Obj:
    def __init__(self):
        self.deep=0
        self.board=[]

def negamax(candidates, role, deep, alpha, beta):
    board.currentSteps=[]
    for i in range(len(candidates)):
        p = candidates[i]
        board.put(p, role)
        steps = [p]
        v = r(deep-1, -beta, -alpha, R.reverse(role), 1, steps[:], 0)
        v.score *= -1
        alpha = max(alpha, v.score)
        board.remove(p)
        p.v = v
    return alpha


def r(deep, alpha, beta, role, step, steps, spread):
    global Cache
    global cacheGet
    if (board.zobrist.code in Cache):

        c = Cache[board.zobrist.code]
        if (c.deep >= deep):
            cacheGet +=1
            score = Score()
            score.score=c.score.score
            score.steps=steps
            score.step=step + c.score.step
            score.c=c
            return score
        #else:
        #    if (mymath.greatOrEqualThan(c.score.score, SCORE.FOUR) or mymath.littleOrEqualThan(c.score.score, -SCORE.FOUR)):
        #        cacheGet +=1
        #        return c.score

    _e = board.evaluate(role)
    leaf = Score()
    leaf.score= _e
    leaf.step= step
    leaf.steps=steps

    global count
    count +=1
    if deep <= 0 or mymath.greatOrEqualThan(_e, SCORE.FIVE) or mymath.littleOrEqualThan(_e, -SCORE.FIVE):
        return leaf


    best = Score()
    global MIN
    best.score=MIN
    best.step=step
    best.steps=steps
    points = board.gen(role, step > 1 if board.count > 10 else step > 3, step > 1)
    if not len(points):
        return leaf


    for i in range(len(points)):
        p = points[i]
        board.put(p, role)
        _deep = deep-1
        _spread = spread
        if (_spread < 1):
            if ( (role == R.com and p.scoreHum >= SCORE.FIVE) or (role == R.hum and p.scoreCom >= SCORE.FIVE)):
                _deep += 2
                _spread +=1
        _steps = steps[:]
        _steps.append(p)
        v = r(_deep, -beta, -alpha, R.reverse(role), step+1, _steps, _spread)
        v.score *= -1
        board.remove(p)
        if (v.score > best.score):
            best = v
        alpha = max(best.score, alpha)
        global ABcut
        if (mymath.greatOrEqualThan(v.score, beta)):
            ABcut +=1
            v.score = MAX-1
            v.abcut = 1
            return v
    cache(deep, best)
    return best

def cache (deep, score):  #有问题现在
  #if (score.abcut):
   #   return False
  obj = Obj()
  s =Score()
  s.score=score.score
  s.steps=score.steps
  s.step= score.step
  obj.deep=deep
  obj.board=str(board.board)
  obj.score = s
  global Cache
  Cache[board.zobrist.code] = obj
  global cacheCount
  cacheCount +=1

def deeping(candidates, role, deep):
    global Cache
    Cache = {}
    for i in range(2, deep+1,2):
        bestScore = negamax(candidates, role, i, MIN, MAX)
        if (mymath.greatOrEqualThan(bestScore, SCORE.FIVE)):
            break

    candidates2 = []
    for d in candidates:
        r = Score()
        r.x=d.x
        r.y=d.y
        r.score = d.v.score
        r.step = d.v.step
        r.steps = d.v.steps
        #if ('vct' in d.v.__dict__):
        #    r.vct = d.v.vct
        #if ('vcf' in d.v.__dict__):
         #   r.vcf = d.v.vcf
        candidates2.append(r)

    def com(a, b):
        if (mymath.equal(a.score, b.score)):
            if (a.score >= 0) :
                if (a.step !=  b.step):
                    return a.step - b.step
                else:
                    return b.score - a.score
            else:
                if (a.step != b.step):
                    return b.step - a.step
                else:
                    return b.score - a.score
        else:
            return (b.score - a.score)
    candidates2.sort(key= functools.cmp_to_key(com))

    result = candidates2[0]
    return result



def deepAll(role, deep):
  role = role if role else R.com
  candidates = board.gen(role)
  return deeping(candidates, role, deep)