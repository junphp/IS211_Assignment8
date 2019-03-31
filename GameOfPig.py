import random
import time
import argparse
import sys
import datetime

''' base class for player action '''
class Player():
    #variable initialize
    def __init__(self,type):
        self.score = 0
        self.runningScore = 0
        self.turn = True
        self.hold = False
        if (type=='h'):
            self.playerType = 'h'
        elif (type=='c'):
            self.playerType = 'c'

    #ask roll or hold to user
    def ask(self):
        if ((self.score + self.runningScore) >= 100):
            #game over if score is 100 or over
            self.win()
        else:
            if (self.playerType=='h'):
                if (self.score>0):
                    print('Your score is %s'%(self.score))
                decision = raw_input('Enter r is roll or Enter h is hold:    ')
                if (decision != 'r' and decision != 'h' and decision != 'e'):
                    print('Invaild Decision. Please try again')
                    self.ask()
                elif (decision == 'e'):
                    exit()
                else:
                    return decision
            else:
                return 'r'

    def roll(self):
        result = random.randint(1, 6) #get result random number of dice
        print('dice result is %s'%(result))
        if (self.score>=100 or (self.score + self.runningScore) >= 100):
            self.win()
        else:
            if (result==1):
                if (self.playerType == 'h'):
                    print('You lost your  %s accumulated score.'%(self.runningScore))
                self.runningScore = 0
                self.turn = False #end turn
                print('Change Turn')
                return False #notice if get 1
            else:
                self.runningScore += result
                self.showScore()
                return True

    #hold turn
    def holdf(self):
        if (self.playerType=='h'):
            print('You select hold')
            print('Current Total Score is %s'%(self.score+self.runningScore))
            #self.playerType=='c'
            #print('Total Your Score is %s'%(self.score))
        print('-------------------------------------')
        self.score += self.runningScore
        self.runningScore = 0
        self.turn = False


    def win(self):
        if (self.playerType == 'h'):
            print('Congratulations you win')
            exit()
        else:
            print('Computer win')
            exit()
    #show current accumulated turn score
    def showScore(self):
        if (self.playerType == 'c'):
            print('Current Computer Turn score is %s' % (self.runningScore))
        else:
            print('Current Your Turn score is %s' % (self.runningScore))

    #initial method: write at child class
    def hold_strategy(self):
        pass

    def changeTurn(self):
        if (self.turn == False):
            self.turn = True
            self.hold = False

    def lineChange(self):
        print('-------------------------------------')

    def getScore(self):
        return self.score


#computer strategy hold or keep dice
class ComputerPlayer(Player):
    '''inherited from player'''

    def hold_strategy(self):
        if (self.runningScore>=25 or self.runningScore>=(100 - self.score)):
            print('Computer select hold')
            print('Current Total Score is %s' % (self.score + self.runningScore))
            return True

#player class inherited from player
class HumanPlayer(Player):

    def play(self):
        pass

#instantiate human or computer
class PlayerFactory():

    def __init__(self):
        pass

    def playerType(self,userType):
        if (userType == 'h'):
            return HumanPlayer('h')
        elif(userType == 'c'):
            return ComputerPlayer('c')
        else:
            print('Invaild Player Value')
            exit()

#proxy base class
class TimeGameProxy(object):

    def startTimeMode(self):
        pass

    def setStartTime(self):
        pass

    def getCurrentTime(self):
        pass

    def getTimeGap(self):
        pass

#proxy real_subject
class TimeGameProxyAction(TimeGameProxy):

    def setStartTime(self):
        start_time = time.time()
        return start_time

    def getCurrentTime(self):
        current = time.time()
        return current

    def getTimeGap(self,start):
        current = time.time()
        if (current - start >= 60):
            return 'timeover'

#proxy exe class
class TimeGameProxyTrigger(TimeGameProxy):

    def __init__(self,real_subject):
        self._real_subject = real_subject

    def setStartTime(self):
        self._real_subject.setStartTime()

    def getCurrentTime(self):
        self._real_subject.getCurrentTime()

    def getTimeGap(self,start):
        return self._real_subject.getTimeGap(start)

class Game():

    def __init__(self,playtype1,playtype2,timed):
        self.factory1 = PlayerFactory()
        self.player1 = self.factory1.playerType(playtype1)
        self.factory2 = PlayerFactory()
        self.player2 = self.factory2.playerType(playtype2)
        if (timed=='y'):
            self.timeActivated = 'y'
        else:
            self.timeActivated = 'n'

    def showWinScore(self,score1,score2):
        if(score1>score2):
            print('Player1 is win')
        elif(score1<score2):
            print('Play2 is win')
        else:
            print('Tie')

    def terminateGame(self):
        sys.exit()

    def play(self):
        if (self.timeActivated == 'y'):
            timemode = TimeGameProxyAction()
            proxy = TimeGameProxyTrigger(timemode)
            start_time = time.time()
            proxy.setStartTime()
        while (True):
            if (self.timeActivated == 'y'):
                if (proxy.getTimeGap(start_time)=='timeover'):
                    p1_score = self.player1.getScore()
                    p2_score = self.player2.getScore()
                    self.showWinScore(p1_score,p2_score)
                    self.terminateGame()

            if (self.player1.turn == True):
                asking = self.player1.ask()
                if(asking == 'r'):
                    if (self.player1.playerType =='c'):
                        if (self.player1.hold_strategy()):
                            self.player2.changeTurn()
                            self.player1.holdf()
                        else:
                            if (self.player1.roll()==False):
                                self.player2.changeTurn()
                                self.player1.lineChange()
                                #self.player1.holdf()
                    else:
                        if (self.player1.roll() == False):
                            self.player2.changeTurn()
                            self.player1.lineChange()
                            #self.player1.holdf()
                elif(asking=='h'):
                    self.player2.changeTurn()
                    self.player1.holdf()
            elif (self.player2.turn == True):
                asking = self.player2.ask()
                if (asking == 'r'):
                    if (self.player2.playerType == 'c'):
                        if (self.player2.hold_strategy()):
                            self.player1.changeTurn()
                            self.player2.holdf()
                        else:
                            if (self.player2.roll()==False):
                                self.player1.changeTurn()
                                self.player2.lineChange()
                                #self.player2.holdf()
                    else:
                        if (self.player2.roll() == False):
                            self.player1.changeTurn()
                            self.player2.lineChange()
                            #self.player2.holdf()
                elif(asking=='h'):
                    self.player1.changeTurn()
                    self.player2.holdf()
                #self.nari.changeTurn()



''' ask player type before start game '''
parser = argparse.ArgumentParser()
parser.add_argument("--player1", help='select human with h, select computer with c', default='h')
parser.add_argument("--player2", help='select human with h, select computer with c', default='c')
parser.add_argument("--timed", help='activate with y', default='n')
args = parser.parse_args()
''' game start '''
newgame = Game(args.player1,args.player2,args.timed)
newgame.play()
