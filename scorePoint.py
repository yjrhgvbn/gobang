import score as score
import role as R

def countToScore (count, block, empty):
    if(empty <= 0):
        if(count >= 5):
            return score.FIVE
        if(block == 0):
            if count==1:
                 return score.ONE
            elif count==2:
                 return score.TWO
            elif count == 3:
                return score.THREE
            elif count == 4:
                return score.FOUR
        if block == 1:
            if count==1:
                return score.BLOCKED_ONE
            elif count==2:
                return score.BLOCKED_TWO
            elif count == 3:
                return score.BLOCKED_THREE
            elif count == 4:
                return score.BLOCKED_FOUR
    elif empty == 1 or empty == count-1:
        #第1个是空位
        if(count >= 6):
            return score.FIVE
        if block == 0:
            if count == 2:
                return score.TWO/2
            elif count == 3:
                return score.THREE
            elif count == 4:
                return score.BLOCKED_FOUR
            elif count == 5:
                return score.FOUR
        if block == 1:
            if count == 2:
                return score.BLOCKED_TWO
            elif count == 3:
                return score.BLOCKED_THREE
            elif count == 4:
                return score.BLOCKED_FOUR
            elif count == 5:
                return score.BLOCKED_FOUR
    elif empty == 2 or empty == count-2:
        #第二个是空位
        if count >= 7:
            return score.FIVE
        if block == 0:
            if count == 3:
                return score.THREE
            elif count == 5 or count == 4:
                return score.BLOCKED_FOUR
            elif count == 6:
                return score.FOUR
        if block == 1:
            if count == 3:
                return score.BLOCKED_THREE
            elif count == 4:
                return score.BLOCKED_FOUR
            elif count == 5:
                return score.BLOCKED_FOUR
            elif count == 6:
                return score.FOUR
        if block == 2:
            if count == 6 or count == 5 or count == 4:
                return score.BLOCKED_FOUR
    elif empty == 3 or empty == count-3:
        if count >= 8:
            return score.FIVE
        if block == 0:
            if count == 4 or count == 5:
                return score.THREE
            elif count == 6:
                return score.BLOCKED_FOUR
            elif count == 7:
                return score.FOUR
        if(block == 1):
            if count == 4 or count == 5 or count == 6:
                return score.BLOCKED_FOUR
            elif count == 7:
                return score.FOUR
        if(block == 2) :
            if count == 4 or count == 5 or count == 6 or count == 7:
                return score.BLOCKED_FOUR
    elif empty == 4 or empty == count-4:
        if(count >= 9):
            return score.FIVE
        if block == 0:
            if count == 5 or count == 6 or count == 7 or count == 8:
                return score.FOUR
        if block == 1:
            if count == 4 or count == 5 or count == 6 or count == 7:
                return score.BLOCKED_FOUR
            elif count == 8:
                return score.FOUR
        if block == 2:
            if count == 5 or count == 6 or count == 7 or count == 8:
                return score.BLOCKED_FOUR
    elif empty == 5 or empty == count-5:
        return score.FIVE
    return 0

def scorepoint(b,px,py,role,dir=-1):
    board = b.board
    result = 0
    mlen = len(board)


    #-方向
    if dir==0 or dir == -1:
        count = 1
        block = 0
        empty = -1
        secondCount = 0  # 另一个方向的count
        for i in range(py + 1, mlen + 2, 1):
            if i >= mlen:
                block +=1
                break
            t = board[px][i]
            if t == R.empty:
                if empty == -1 and i < mlen - 1 and board[px][i + 1] == role:
                    empty = count
                    continue
                else:
                    break
            if t == role:
                count +=1
                continue
            else:
                block +=1
                break
        for i in range(py-1,-2,-1):
            if i < 0:
                block +=1
                break
            t = board[px][i]
            if t == R.empty:
                if empty == -1 and i >0 and board[px][i - 1] == role:
                    empty = 0
                    continue
                else:
                    break
            if t == role:
                secondCount +=1
                if empty!=-1:
                    empty+=1
                continue
            else:
                block +=1
                break
        count += secondCount
        b.scoreCache[role][0][px][py] = countToScore(count, block, empty)
    result += b.scoreCache[role][0][px][py]

    #|方向
    if dir==1 or dir ==-1:
        count = 1
        block = 0
        empty = -1
        secondCount = 0  # 另一个方向的count
        for i in range(px+1,mlen + 2,1):
            if i >= mlen:
                block +=1
                break
            t = board[i][py]
            if t == R.empty:
                if empty == -1 and i < mlen - 1 and board[i+1][py] == role:
                    empty = count
                    continue
                else:
                    break
            if t == role:
                count +=1
                continue
            else:
                block +=1
                break
        for i in range(px-1,-2,-1):
            if i < 0:
                block +=1
                break
            t = board[i][py]
            if t == R.empty:
                if empty == -1 and i >0 and board[i-1][py] == role:
                    empty = 0
                    continue
                else:
                    break
            if t == role:
                secondCount +=1
                if empty!=-1:
                    empty+=1
                continue
            else:
                block +=1
                break
        count += secondCount
        b.scoreCache[role][1][px][py] = countToScore(count, block, empty)
    result += b.scoreCache[role][1][px][py]

    # \方向
    if dir==2 or dir ==-1:
        count = 1
        block = 0
        empty = -1
        secondCount = 0  # 另一个方向的count
        for i in range(1, mlen + 2, 1):
            x = px + i
            y = py + i
            if x >= mlen or y>=mlen:
                block += 1
                break
            t = board[x][y]
            if t == R.empty:
                if empty == -1 and (x<mlen-1 and y < mlen-1) and board[x + 1][y + 1] == role:
                    empty = count
                    continue
                else:
                    break
            if t == role:
                count += 1
                continue
            else:
                block += 1
                break
        for i in range(1, mlen + 2, 1):
            x = px - i
            y = py - i
            if x < 0 or y < 0:
                block += 1
                break
            t = board[x][y]
            if t == R.empty:
                if empty == -1 and (x>0 and y>0) and board[x - 1][y - 1] == role:
                    empty = 0
                    continue
                else:
                    break
            if t == role:
                secondCount += 1
                if empty != -1:
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        b.scoreCache[role][2][px][py] = countToScore(count, block, empty)
    result += b.scoreCache[role][2][px][py]

    # /方向
    if dir==3 or dir==-1:
        count = 1
        block = 0
        empty = -1
        secondCount = 0  # 另一个方向的count
        for i in range(1, mlen + 2, 1):
            x = px + i
            y = py - i
            if x<0 or y<0 or x>=mlen or y>=mlen:
                block += 1
                break
            t = board[x][y]
            if t == R.empty:
                if empty == -1 and (x < mlen - 1 and y > 0) and board[x + 1][y - 1] == role:
                    empty = count
                    continue
                else:
                    break
            if t == role:
                count += 1
                continue
            else:
                block += 1
                break
        for i in range(1,mlen + 2,1):
            x = px - i
            y = py + i
            if x<0 or y<0 or x>=mlen or y>=mlen:
                block += 1
                break
            t = board[x][y]
            if t == R.empty:
                if empty == -1 and (x > 0 and y < mlen - 1) and board[x - 1][y + 1] == role:
                    empty = 0
                    continue
                else:
                    break
            if t == role:
                secondCount += 1
                if empty != -1:
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        b.scoreCache[role][3][px][py] = countToScore(count, block, empty)
    result += b.scoreCache[role][3][px][py]
    return result
