board = [
    [8,7,0,6,0,0,0,2,0],
    [0,0,0,0,8,0,0,0,3],
    [0,0,9,0,0,5,0,1,0],
    [7,5,0,0,0,9,0,8,6],
    [0,6,0,0,0,0,0,3,0],
    [4,2,0,8,0,0,0,5,1],
    [0,4,0,2,0,0,1,0,0],
    [5,0,0,0,9,0,0,0,0],
    [1,9,0,4,7,8,0,6,5]
]



def backtrackingAlgo(b):
    find = find_emptysquare(b)
    if not find:
        return True
    else:
        row , col = find
    
    for i in range(1,10):
        if check_valid(b,i,(row,col)):
            b[row][col] = i 

            if backtrackingAlgo(b):
                return True
            b[row][col] = 0
    
    return False



#find if the current board is valid or not 

def check_valid(b , number , position):
    #first we check the row
    for i in range(len(b[0])):
        if b[position[0]][i] == number and position[1]!=i:
            return False

    #now we check coloumn
    for i in range(len(b[0])):
        if b[i][position[1]] == number and position[0]!=i:
            return False

    #checking the 3x3 box

    xBox = position[1] // 3
    yBox = position[0] // 3

    #loop through all 9 elements in the box
    for i in range(yBox * 3 , yBox * 3 + 3):
        for j in range(xBox * 3 , xBox * 3 + 3):
            if b[i][j] == number and (i,j)!=position:
                return False

    return True



#first we pick an empty square ( which has 0 )

def boardprint(b):
    for i in range(len(b)):
        if i%3==0 and i!=0:
            #everytime we're on the third row it just prints a horizontal line ()
            print(" - - - - - - - - - - - - - - ")

        #gets the length of our rows 
        for j in range(len(b[0])):
            #if its the 3rd element then it draws a vertical line 
            if j%3 == 0 and j!=0:
                print(" | ", end = "")
            if j==8:
                print(b[i][j])
            else:
                print(str(b[i][j]) + " ", end="")


#finds an empty space and return the position of it 
def find_emptysquare(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                #returns ( row , col )
                return (i,j)
    return None






boardprint(board)

backtrackingAlgo(board)

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

boardprint(board)
