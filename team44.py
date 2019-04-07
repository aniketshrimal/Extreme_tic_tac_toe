from __future__ import print_function
import datetime
import copy
import random

INFINITY = 1e10
class Team44:
    def __init__(self):
        self.bonuscheck=0
        self.start= 0
        self.win = 0
        self.limit = 5
        self.terminal = INFINITY
        self.limitval = 0
        self.hash_array = {}
        self.dict = {'x':1,'o':-1,'-':0,'d':0}
        self.timeLimit = datetime.timedelta(seconds = 15)
        self.wt = [2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2]
        # self.blockwt = [6,4,4,6,4,3,3,4,4,3,3,4,6,4,4,6]

    def boardeval(self,blockx,blocky,board,temp):


    	diamond = [[3 for x in range(3)] for y in range(3)]
        for i in range (1,3):
            for j in range (1,3):
                mark = board.board_status[4*blockx+i-1][4*blocky+j]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16
                mark = board.board_status[4*blockx+i][4*blocky+j-1] 
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16
                mark = board.board_status[4*blockx+i+1][4*blocky+j]
                
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16
                mark = board.board_status[4*blockx+i][4*blocky+j+1]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16


        rowCnt = [3,3,3,3]
        colCnt = [3,3,3,3]
        value = 0
        for row in range(4):
            for col in range(4):
                val = self.dict[mark]
                mark = board.board_status[4*blockx+row][4*blocky+col]
                if val != 0:
                    value = value+val*self.wt[4*row+col]
                    if colCnt[col]==3:
                        colCnt[col] = 5*val
                    elif colCnt[col]*val<0:
                        colCnt[col] = 0
                    colCnt[col]*=16
                    if rowCnt[row]==3:
                        rowCnt[row] = val*5
                    elif rowCnt[row]*val < 0:
                        rowCnt[row]=0
                    rowCnt[row]*=16


        # now considering the condition of a draw
        draw = 12
        
        for i in range(4):
            if colCnt[i]==0:
                draw-=1
            if rowCnt[i]==0:
                draw-=1    

        for i in range(1,3):
            for j in range(1,3):
                if diamond[i][j]==0:
                    draw-=1

        #checking for draw
        if(draw==0):
            temp[blockx][blocky] = 'd'
            return 0
            
        #
        for i in range(1,3):
            for j in range(1,3):
                if diamond[i][j]!=3:
                    value+=diamond[i][j]

        for i in range(4):       
            if colCnt[i]!=3:
                value=value+colCnt[i]
            if rowCnt[i]!=3:
                value=value+rowCnt[i]


        return value
        


    def blockeval(self,tempBlock,board):
        
        diamond = [[3 for x in range(3)] for y in range(3)]
        for i in range (1,3):
            for j in range (1,3):
                mark = tempBlock[i-1][j]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16*dictVal*dictVal
                mark = tempBlock[i][j-1]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16*dictVal*dictVal
                mark = tempBlock[i+1][j]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16*dictVal*dictVal
                mark = tempBlock[i][j+1]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if (diamond[i][j] == 3):
                        diamond[i][j] = dictVal*5
                    elif(dictVal*diamond[i][j]<=0):
                        diamond[i][j]=0
                    diamond[i][j] = diamond[i][j]*16*dictVal*dictVal

        rowCnt = [3,3,3,3]
        colCnt = [3,3,3,3]
        value = 0
        for row in range(4):
            for col in range(4):
                val = self.dict[mark]
                mark = tempBlock[row][col]
                if mark != '-':
                    value= value + val*self.wt[4*row+col]
                    if colCnt[col]==3:
                        colCnt[col] = val*5
                    elif val*colCnt[col]<0 and colCnt[col]!=3:
                        colCnt[col] = 0
                    colCnt[col]=colCnt[col]*16
                    if rowCnt[row]==3:
                        rowCnt[row] = val*5
                    elif rowCnt[row]*val < 0 and rowCnt!=3:
                        rowCnt[row]=0
                    rowCnt[row]=rowCnt[row]*16


        for i in range(4):
            if(colCnt[i]!=3):
                value+=colCnt[i]
            if(rowCnt[i]!=3):
                value+=rowCnt[i]


        for i in range(1,3):
            for j in range(1,3):
                if diamond[i][j]!=3:
                    value+=diamond[i][j]

        return value
                

    def heuristic(self, board):
        final_value = 0
        temp_block_status = copy.deepcopy(board.block_status)
        for i in range(4):
            for j in range(4):
                fin_val = self.boardeval(i,j,board,temp_block_status)
                final_value = final_value + fin_val
        final_value = final_value + self.blockeval(temp_block_status,board)*120
        del(temp_block_status)
        return final_value

    def alphabetaprun(self,board,old_move,flag,depth,alpha,beta,bonuscheck):
        hashing = hash(str(board.board_status))
        if self.hash_array.has_key(hashing):
            val = self.hash_array[hashing]
            if val[1]<=alpha:
                return val[1],old_move
            if val[0]>=beta:
                return val[0],old_move
            if (val[1]<beta):
            	beta=val[1]
            if val[0]>alpha:
            	alpha = val[0]

        board_cells = board.find_valid_move_cells(old_move)
        random.shuffle(board_cells)
        prev_x = 0 
        prev_o = 0
        for i in range(4):
            for j in range(4):
                if(board.block_status[i][j] == 'x'):
                    prev_x += 1
                if(board.block_status[i][j] == 'o'):
                    prev_o += 1
                    
        if (flag == 'x'):
            node_val = -INFINITY, board_cells[0]
            new = 'o'
            temp = copy.deepcopy(board.block_status)
            a = alpha
            for values in board_cells :
                if datetime.datetime.utcnow() - self.start >= self.timeLimit :
                    self.limitval = 1
                    break
                board.update(old_move, values, flag)
                if (board.find_terminal_state()[0] == 'x' ):
                    board.board_status[values[0]][values[1]] = '-'
                    board.block_status = copy.deepcopy(temp)
                    node_val = self.terminal,values
                    break
                
                elif (board.find_terminal_state()[0] == 'o'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(temp)
                    continue
                elif(board.find_terminal_state()[0] == 'NONE'):
                    x = 0
                    d = 0
                    o = 0
                    temp1 = 0
                    for i in range(4):
                        for j in range(4):
                            if(board.block_status[i][j] == 'x'):
                                x += 1
                            if(board.block_status[i][j] == 'o'):
                                o += 1
                            if(board.block_status[i][j] == 'd'):
                                d += 1
                    if(x==o):
                        temp1 = 0
                    elif(x>o):
                        temp1 = INFINITY/2 + 10*(x-o)
                    else:
                        temp1 = -INFINITY/2 - 10*(o-x)
                elif( depth >= self.limit):
                    temp1 = self.heuristic(board)
                else:
                    new_x = 0
                    for i in range(4):
                        for j in range(4):
                            if(board.block_status[i][j] == 'x'):
                                new_x += 1            
                    if new_x - prev_x == 1  and bonuscheck ==0:
                        new='x'
                        bonuscheck = 1
                    temp1 = self.alphabetaprun(board, values, new, depth+1, a, beta,bonuscheck)[0]
                    bonuscheck=0
                board.board_status[values[0]][values[1]] = '-'
                board.block_status = copy.deepcopy(temp)
                if(node_val[0] < temp1):
                    node_val = temp1,values
                if temp1>a:
                	a=temp1
                if beta <= node_val[0] :
                    break
            del(temp)

        if (flag == 'o'):
            node_val = INFINITY, board_cells[0]
            new = 'x'
            temp = copy.deepcopy(board.block_status)
            b = beta
            for values in board_cells :
                if datetime.datetime.utcnow() - self.start >= self.timeLimit :
                    self.limitval = 1
                    break
                board.update(old_move, values, flag)
                if (board.find_terminal_state()[0] == 'o'):
                    board.board_status[values[0]][values[1]] = '-'
                    board.block_status = copy.deepcopy(temp)
                    node_val = -1*self.terminal,values
                    break
                
                elif (board.find_terminal_state()[0] == 'x'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(temp)
                    continue
                elif(board.find_terminal_state()[0] == 'NONE'):
                    bonuscheck=0
                    x = 0
                    d = 0
                    o = 0
                    temp1 = 0
                    for i in range(4):
                        for j in range(4):
                            if board.block_status[i][j] == 'x':
                                x += 1
                            if(board.block_status[i][j] == 'o'):
                                o += 1
                            if(board.block_status[i][j] == 'd'):
                                d += 1
                    if(x==o):
                        temp1 = 0
                    elif(x>o):
                        temp1 = INFINITY/2 + 10*(x-o)
                    else:
                        temp1 = -INFINITY/2 + 10*(x-o)
                elif depth >= self.limit:
                    temp1 = self.heuristic(board)
                else:
                    new_o = 0
                    for i in range(4):
                        for j in range(4):
                            if(board.block_status[i][j] == 'x'):
                                new_o += 1            
                    if new_o - prev_o == 1  and bonuscheck ==0:
                        new='o'
                        bonuscheck = 1
                    temp1 = self.alphabetaprun(board, values, new, depth+1, alpha, b,bonuscheck)[0]
                    bonuscheck=0
                   
                board.board_status[values[0]][values[1]] = '-'
                board.block_status = copy.deepcopy(temp)
                if(node_val[0] > temp1):
                    node_val = temp1,values
                if temp1<b:
                	b=temp1
                if alpha >= node_val[0] :
                    break
            del(temp)
        if(node_val[0] <= alpha):
            self.hash_array[hashing] = [-INFINITY,node_val[0]]
        if(node_val[0] > alpha and node_val[0] < beta):
            self.hash_array[hashing] = [node_val[0],node_val[0]]
        if(node_val[0]>=beta):
            self.hash_array[hashing] = [node_val[0],INFINITY]
        return node_val

    def move(self, board, old_move, flag):
        self.start = datetime.datetime.utcnow()
        self.limitval = 0
        self.hash_array.clear()
        mymove = board.find_valid_move_cells(old_move)[0]
        for i in range(3,100):
            self.hash_array.clear()
            self.limit = i
            tempval= self.bonuscheck
            alphabeta = self.alphabetaprun(board, old_move, flag, 1, -INFINITY, INFINITY,tempval)
            getval = alphabeta[1]
            if(self.limitval == 0):
               mymove = getval
            else:
                break   
        return mymove[0], mymove[1]