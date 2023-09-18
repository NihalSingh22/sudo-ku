import pygame
import time
pygame.font.init()

class Grid:
    board = [
    [0,4,8,0,1,0,5,0,0],
    [5,0,0,0,0,3,0,0,0],
    [0,0,0,7,0,0,2,9,0],
    [9,0,0,0,0,0,0,7,0],
    [0,0,4,3,0,9,6,0,0],
    [0,6,0,0,0,0,0,0,2],
    [0,5,6,0,0,4,0,0,0],
    [0,0,0,8,0,0,0,0,6],
    [0,0,3,0,7,0,1,5,0]
    ]

    def __init__(self,rows,cols,width,height,win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height 
        self.model = None
        self.modelUpdate()
        self.selected = None
        self.win = win 
    
    def modelUpdate(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def place(self,val):
        row , col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.modelUpdate()

            if check_valid(self.model , val , (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.modelUpdate()
                return False

    def sketch(self,val):
        row , col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        space = self.width / 9 
        for i in range(self.rows + 1):
            if i%3 == 0 and i!=0:
                lines = 4
            else:
                lines = 1

            pygame.draw.line(self.win , (0,0,0), (0,i*space) , (self.width, i*space),lines )
            pygame.draw.line(self.win , (0,0,0), (i*space,0) , (i*space,self.height),lines )

        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
    
    def select(self , row , col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row , col)

    def clear(self):
        row , col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            space = self.width / 9
            x = pos[0] // space
            y = pos[1] // space
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True 
    

    def solve(self):
        find = find_emptysquare(self.model)

        if not find:
            return True
        else:
            row,col = find 

        for i in range(1,10):
            if check_valid(self.model, i , (row,col)):
                self.model[row][col] = i 

                if self.solve():
                    return True
                self.model[row][col] = 0 

        return False
    

    def GUI(self):
        self.modelUpdate()
        find = find_emptysquare(self.model)

        if not find:
            return True
        else:
            row,col = find

        for i in range(1,10):
            if check_valid(self.model, i , (row,col)):
                self.model[row][col] = i 
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_changes(self.win , True)
                self.modelUpdate()
                pygame.display.update()
                pygame.time.delay(100)

                if self.GUI():
                    return True 
                
                self.model[row][col] = 0 
                self.cubes[row][col].set(0)
                self.modelUpdate()
                self.cubes[row][col].draw_changes(self.win , False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9


    def __init__(self , value , row , col , width , height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def draw(self , win):
        newfont = pygame.font.SysFont("comicsans" , 20)

        space = self.width / 9

        x = self.col * space 
        y = self.row * space 

        if self.temp != 0 and self.value ==0:
            temp_text = newfont.render(str(self.temp) , 1 , (128,128,128))
            win.blit(temp_text , (x+5 , y+5))
        elif not(self.value == 0):
            value_text = newfont.render(str(self.value) , 1 , (0,0,0))
            win.blit(value_text, (x+ (space/2 - value_text.get_width()/2) , y + (space/2 - value_text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0) , (x,y,space,space) , 3)

        
    def draw_changes(self , win , Boolean = True ):
        newfont = pygame.font.SysFont("comicsans" , 20)

        space = self.width / 9

        x = self.col * space 
        y = self.row * space 

        pygame.draw.rect(win, (255,255,255) , (x,y,space,space) , 0)
        temp_text = newfont.render(str(self.value) , 1 , (0,0,0))
        win.blit(temp_text, (x+ (space/2 - temp_text.get_width()/2) , y + (space/2 - temp_text.get_height()/2)))
        
        if Boolean:
            pygame.draw.rect(win, (0,255,0) , (x,y,space,space) , 3)
        else:
            pygame.draw.rect(win, (255,0,0) , (x,y,space,space) , 3)

    
    def set(self,val):
        self.value = val
    
    def set_temp(self,val):
        self.temp = val
    

def find_emptysquare(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return (i,j)
    
    return None


def check_valid(b , num , pos):
    #first we check the row
    for i in range(len(b[0])):
        if b[pos[0]][i] == num and pos[1]!=i:
            return False

    #now we check coloumn
    for i in range(len(b[0])):
        if b[i][pos[1]] == num and pos[0]!=i:
            return False

    #checking the 3x3 box

    xBox = pos[1] // 3
    yBox = pos[0] // 3

    #loop through all 9 elements in the box
    for i in range(yBox * 3 , yBox * 3 + 3):
        for j in range(xBox * 3 , xBox * 3 + 3):
            if b[i][j] == num and (i,j)!=pos:
                return False

    return True
    
def redraw(win , board , time , strikes):
    win.fill((255,255,255))

    newfont = pygame.font.SysFont("comicsans" ,15)
    temp_text = newfont.render("Time taken: " +format_time(time),1,(0,0,0))
    win.blit(temp_text , (540 - 160 , 560))

    value_text =newfont.render("X " *strikes , 1 , (255,0,0))
    win.blit(value_text,(20,560))

    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs // 60 
    hour = minute // 60

    formatted = " " + str(minute) + ":" + str(sec)

    return formatted


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("SUDOKU")
    board = Grid( 9 , 9 , 540 , 540 , win)
    run = True
    key = None
    start = time.time()
    strikes = 0
    while run:
        playing = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.GUI()
                if event.key == pygame.K_RETURN:
                    i , j = board.selected
                    if board.cubes[i][j].temp!=0:
                        if board.place(board.cubes[i][j].temp):
                            print("GREAT SUCCESS")
                        else:
                            print("WRONG")
                            strikes = strikes + 1
                        key = None

                        if board.is_finished():
                            print("GAME OVER!")
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                
        if board.selected and key!=None:
            board.sketch(key)
        
        redraw(win , board, playing , strikes)
        pygame.display.update()

main()
pygame.quit()
                