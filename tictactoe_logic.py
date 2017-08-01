import random

#game state constants
IN_PLAY = 0
WIN = 1
TIE = 2
#player constants
PLAYER1 = 0
PLAYER2 = 1
#state description
GAMESTATE_DESCRIPTIONS = {
    0: 'in play',
    1: 'win',
    2: 'tie',
}
#player description
PLAYER_DESCRIPTIONS = {
    0: 'player 1',
    1: 'player 2',
}

class tictactoeGame:
    def __init__(self):
        self.gamestate = IN_PLAY #0=in play;1=win;2=tie
        self.player1_moves = set()
        self.player2_moves = set()
        self.current_player_turn = PLAYER1 #0=player1;1=player2
        print 'init'
    
    def validatemove(self, move):
        print 'validating move', move
        #is the 'move' in range?
        if not self.gamestate == IN_PLAY:
            print 'game is not in play'
            return False
        if move > 8 or move < 0:
            print 'move is not in range'
            return False
        if move in self.player1_moves | self.player2_moves:
            print 'play already made'
            return False
        print 'move', move, 'evaluated as legal'
        return True
        
    def getgamestate(self):
        return GAMESTATE_DESCRIPTIONS[self.gamestate]
            
    def getcurrentplayerturn(self):
        return PLAYER_DESCRIPTIONS[self.current_player_turn]
    
    def getopenmoves(self):
        allmoves = {0,1,2,3,4,5,6,7,8}
        return allmoves-(self.player1_moves | self.player2_moves)
        
    def playhumanmove(self, move):
        if self.validatemove(move) == True and self.current_player_turn == PLAYER1:
            print 'adding move', move, 'to player player', self.player1_moves
            self.player1_moves.add(move)
            self.current_player_turn = PLAYER2
            print 'human play made at', move
            return True
        else:
            print 'human play made at', move, 'was rejected'
            return False
    
    def evaluateWinState(self,movesetToEval):
        #012
        #345
        #678
        winStateList = [
            {0,1,2},{3,4,5},{6,7,8}, #horizantal win states
            {0,3,6},{1,4,7},{2,5,8}, #vertical win states
            {0,4,8},{2,4,6} #diagonal win states
            ]
        for winState in winStateList:
            if winState <= movesetToEval:
                return True
        return False
        
    def evaluateWinStateNext(self,movesetToEval):
        openmoves = self.getopenmoves()
        for move in openmoves:
            movesetToEval_wMove = movesetToEval.copy()
            movesetToEval_wMove.add(move)
            if self.evaluateWinState(movesetToEval_wMove):
                return move
        return None
    
    def playaimove(self):
        player1move_count = len(self.player1_moves)
        moveToMake = None
        #ai's first turn (human has made one move)
        if player1move_count == 1:
            #if human played to center, play a corner
            if 4 in self.player1_moves:
                moveToMake = random.choice((0,2,6,8))
            #if human not played in center, play in the center
            elif 4 not in self.player1_moves:
                moveToMake = 4
            else:
                raise AssertionError("unexpected ui state")
        #ai's second turn (human has made two moves)
        elif player1move_count == 2:
            #we can't win but we can prevent a win by player 1
            moveToMake = self.evaluateWinStateNext(self.player1_moves)
            #if the human player can win by making a move, let ai make it to block
            #if theh human player cannot win by making a move, then make a random move
            if moveToMake == None:
                moveToMake = random.choice(tuple(self.getopenmoves()))
        #ai's third turn going forward (human has made 3 moves)
        else:
            #can we win by making a play?
            moveToMake = self.evaluateWinStateNext(self.player2_moves)
            #can we prevent the human from winning by making a play?
            if moveToMake == None:
                moveToMake = self.evaluateWinStateNext(self.player1_moves)
            #make a random move
            if moveToMake == None:
                moveToMake = random.choice(tuple(self.getopenmoves()))
        print 'adding move', moveToMake, 'to player ai', self.player2_moves
        self.player2_moves.add(moveToMake)
        self.current_player_turn = PLAYER1
        print 'ai play made at', moveToMake
                
    def getBoardOut(self):
        return [list(self.player1_moves), list(self.player2_moves)]
    
    def makeplay(self, play):
        play1win = self.evaluateWinState(self.player1_moves)
        play2win = self.evaluateWinState(self.player2_moves)
        nomovesleft = len(self.getopenmoves()) == 0
        if play1win == True:
            self.gamestate = WIN #win
            return ['human won',self.getBoardOut()]
        elif play2win == True:
            self.gamestate = WIN #win
            return ['ai won',self.getBoardOut()]
        elif nomovesleft == True:
            self.gamestate = TIE #tie
            return ['tie',self.getBoardOut()]
        else:
            #human player 1's turn
            #prompt
            self.playhumanmove(int(play))
            nomovesleft = len(self.getopenmoves()) == 0
            if nomovesleft == False:
                self.playaimove()
            play1win = self.evaluateWinState(self.player1_moves)
            play2win = self.evaluateWinState(self.player2_moves)
            nomovesleft = len(self.getopenmoves()) == 0
            if play1win == True:
                self.gamestate = WIN #win
                return ['human won',self.getBoardOut()]
            elif play2win == True:
                self.gamestate = WIN #win
                return ['ai won',self.getBoardOut()]
            elif nomovesleft == True:
                self.gamestate = TIE #tie
                return ['tie',self.getBoardOut()]
            else:
                self.gamestate = IN_PLAY #still in play
                return ['in play',self.getBoardOut()]