import copy
import sys
import pygame
import random
import numpy as np

CROSS_WIDTH = 20
BG_COLOR = "#343434"
WIDTH = 600
HEIGHT = 600
LINE_COLOR = "#ffde57"
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS
radius = SQSIZE // 4
fig_color = "#646464"
LINE_WIDTH = 15
CIRC_WIDTH = 15
OFFSET = 50
color_blue = "#4584b6"
LINE_COLOR = "#ffde57"
BG_COLOR = "#343434"

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill( BG_COLOR )
class Board:
    def __init__(self):
        self.squares=np.zeros((3,3))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0
    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = color_blue if self.squares[0][col] == 2 else color_blue
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = color_blue if self.squares[row][0] == 2 else color_blue
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = color_blue if self.squares[1][1] == 2 else color_blue
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = color_blue if self.squares[1][1] == 2 else color_blue
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs+=1
    def empty_sqr(self,row,col):
        return self.squares[row][col]==0
    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in range(3):
            for col in range(3):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    def isfull(self):
        return self.marked_sqrs==9
    def is_empty(self):
        return self.marked_sqrs==0
class AI:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player
    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        index=random.randrange(0,len(empty_sqrs))
        return empty_sqrs[index]

    def minimax(self,board,maximizing): #return eval,best_move
        case=board.final_state()
        #terminal cases:
        if case==1:
            return case,None
        if case==2:
            return -1,None
        elif board.isfull():
            return 0,None
        
        if maximizing:
            max_eval=-99
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval=self.minimax(temp_board,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)
            return max_eval,best_move

        elif not maximizing:
            min_eval=99
            best_move=None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
            return min_eval,best_move
    def eval(self,main_board):
        if self.level==0:
            #random choise
            eval='random'
            move=self.rnd(main_board)
            pass
        else:
            eval,move=self.minimax(main_board,False)
        print(f'square{move}={eval}')
            
        return move
class game:
    def __init__(self):
            self.Board = Board()
            self.ai = AI()
            self.player = 1  
            self.running = True
            self.show_line()
    def make_move(self,row,col):
        self.Board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.switch_player()
    def show_line(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),15)
        pygame.draw.line(screen,LINE_COLOR,(2*SQSIZE,0),(2*SQSIZE,HEIGHT),15)
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(3*SQSIZE,SQSIZE),15)
        pygame.draw.line(screen,LINE_COLOR,(0,2*SQSIZE),(3*SQSIZE,2*SQSIZE),15)
    def draw_fig(self,row,col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, fig_color, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, fig_color, start_asc, end_asc, CROSS_WIDTH)
        elif self.player==2:
            #draw O
            center=(col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen,fig_color,center,radius,CIRC_WIDTH)
    def isover(self):
        return self.Board.final_state(show=True)
        
    def switch_player(self):
        self.player=self.player%2+1

    def reset(self):
        self.__init__()

def main():
    Game = game()
    board = Game.Board
    ai = Game.ai

    while True:
        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                if board.empty_sqr(row, col) and Game.running:
                    Game.make_move(row, col)
                    if Game.isover():
                        Game.running = False  # Stop the game if someone wins

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Game.reset()
                    board = Game.Board
                    ai = Game.ai
        # AI move
        if Game.player == ai.player and Game.running:  # Ensure AI only plays when game is running
            pygame.display.update()
            (row, col) = ai.eval(board)
            Game.make_move(row, col)
            if Game.isover():
                Game.running = False  # Stop the game if someone wins

        pygame.display.update()

main()
