# IMPORTS
# import random library
from random import randint
# import sound library
add_library("sound")
# colours
# dark gray - (108, 109, 113)
# blue - (4,179,213)
# yellow - (255, 204, 133)
##################################################################################################################################
# CLASSES
# class to set tile types for the game board
class Tile:
    def __init__(self):
        # initialize different tile types (different states a tile can be in)
        self.bomb = False # bomb
        self.label = None # number
        self.visible = False # already visited
        self.flagged = False # flagged
    
    def reset(self):
        # a function to reset tiles after game ends
        self.bomb = False # bomb
        self.label = None # number
        self.visible = False # already visited
        self.flagged = False # flagged
#################################################################
# A class to create the stopwatch on the gameboard
# tracks elapsed time of each round
class Timer:
    def __init__(self):
        # initialize values of timer class
        self.startTime = 0
        self.stopTime = 0
        self.running = False
        
    def start(self):
        # starts the timer when game begins
        self.startTime = millis()
        # the timer is running
        self.running = True
        
    def stop(self):
        # stops the timer when the player wins or loses
        self.stopTime = millis()
        # the timer isn't running anymore
        self.running = False
        
    def totalTime(self):
        # calculates current time and/or total time
        # set elapsed time as 0
        elapsed = 0
        if self.running:
            # if the timer is running, show how much time has elapsed so far
            # this runs when the game is ongoing
            elapsed = millis()-self.startTime
        else:
            # this runs when the game is over and we need to display how long the round was
            elapsed = self.stopTime - self.startTime
        return elapsed
    
    def seconds(self):
        # converts total time of milliseconds into seconds 
        # seconds is a better way to display time to the player
        seconds = (self.totalTime()//1000)%60
        return seconds
    
    def minutes(self):
        # converts total time of milliseconds into minutes
        # minutes is a better way to display time to the player
        minutes = (self.totalTime()//(1000*60))%60
        return minutes
    
    def draw(self):
        # function drawing the timer in the format of: 
        # mm:ss on the gameboard and win/lose screens
        text("Time:" + nf(sw.minutes(),2)+":"+nf(sw.seconds(),2),620,440)
    
    def reset(self):
        # resetting the timer after the game ends and restarts
        # startTime and stopTime return to 0
        self.startTime = 0
        self.stopTime = 0
        # timer is no longer running
        self.running = False
        # restart the timer
        self.start()
#################################################################
# class to create the high score/player object to be displayed on the scoreboard
class Score:
    def __init__(self,name,score):
        # initialize values of the score class
        self.name = name # player name
        self.score = score # player score
#################################################################
# class to store all player scores and display on the high score screen
class ScoreBoard:
    def __init__(self):
        # create list to store score/player objects
        self.players = []
    
    def add_players(self,player):
        # function adding players to list to display on scoreboard
        return self.players.append(player)
        
    def display(self):
        # function displaying + ranking all players and scores on the scoreboard
        rank = 0
        # first position of #1 player
        x = 100
        y = 145
        for player in self.players:
            # each time loop runs:
            # ranks increase by 1 and position goes lower
            # displaying rank, name, score
            text(rank+1,x,y+55)
            text(player.name,x+125,y+55)
            text(player.score,x+500,y+55)
            rank +=1
            y += 55

##################################################################################################################################
# GLOBALS
w = 40 # width of each square

bombs = 10 # number of bombs on board
flags = 0 # number of flags placed
click = 0 # number of clicks
# board dimensions
ROWS = 9
COLS = 9

# setting game mode
mode = "title" # modes: title, game-on, game-won, game-lost, high-score,instructions

sw = Timer() # creating stopwatch

# scoreboard player scores
p1 = Score("Jennifer", "00:18")
p2 = Score("Kristen", "00:28")
p3 = Score("Julian", "00:24")
p4 = Score("Steven", "00:32")
p5 = Score("Edith", "00:47")

# scoreboard instance
highscores = ScoreBoard()

# adding player scores to scoreboard list
highscores.add_players(p1)
highscores.add_players(p2)
highscores.add_players(p3)
highscores.add_players(p4)
highscores.add_players(p5)

#################################################################
# GAME SETUP
# DRAW THE 9X9 GRID
# assign tile object to each square on the grid
grid = [[Tile() for n in range(COLS)] for n in range(ROWS)] 

# function to PLACE MINES ON THE GRID RANDOMLY
def place_mines(): 
    for n in range(bombs): # placing 10 bombs
        # continue until all random mines have been placed
        while True:
            x = randint(0,8) # randomly select a bomb position
            y = randint(0,8)
            # if selected tile is not a bomb, add it there
            if grid[y][x].bomb == False: 
                grid[y][x].bomb = True
                # stop when all have been placed
                break
# calling the function
place_mines()
##################################################################################################################################
# MAIN FUNCTIONS
def setup():
    # declare global so that pictures and timer can be used anywhere
    global sw,covered,flagtile, one_bomb, two_bomb,three_bomb,four_bomb, winface,loseface
 
    # drawing canvas
    # 9 x 9 squares, 40 pixels/square = 360
    # add 100 for extra space: height of game window = 460
    size(800,460)
    
    # starting timer
    sw.start()
    
    # loading main game music
    bgm = SoundFile(this,"minesweeperbgm.wav")
    # looping it so that it plays continuously
    bgm.loop()
    
    # loading in all images to be used on game board tiles
    covered = loadImage("minesweepercoveredtile.png")
    flagtile = loadImage("minesweeperflag.png")
    one_bomb = loadImage("minesweeper1bomb.png")
    two_bomb = loadImage("minesweeper2bomb.png")
    three_bomb = loadImage("minesweeper3bomb.png")
    four_bomb = loadImage("minesweeper4bomb.png")
    winface = loadImage("minesweeperwin.jpg")
    loseface = loadImage("minesweeperlose.png")
#################################################################
def draw():
    # declare global variables
    global sw,level,mode, game_won,flags
    # setting background colour blue
    background(4,179,213)
    #############################################
    # WHEN ON TITLE SCREEN
    if mode == "title":
        # Title
        textSize(50)
        fill(255, 204, 133)
        text("MINESWEEPER", 240, 80)
        
        # mode buttons
        textSize(30)
        fill(255,255,255)
        text("Click to select screen", 250, 170)
        fill(255, 204, 133)
        stroke(255, 204, 133)
        rect(30,250,210,60)
        rect(295,250,210,60)
        rect(560,250,210,60)
        # screen options
        textSize(26)
        fill(108, 109, 113)
        text("PLAY", 100, 290)
        text("HIGH SCORE", 322, 290)
        text("INSTRUCTIONS", 575, 290)
    #############################################
    # WHEN ON INSTRUCTIONS SCREEN
    if mode == "instructions": # instruction screen
        # Title
        textSize(50)
        fill(255, 204, 133)
        text("INSTRUCTIONS", 230, 80)
        # Instructions
        textSize(20)
        fill(255,255,255)
        text("1. You are presented with a board of squares. Some",110,130) 
        text("squares contain mines (bombs), while others don't. ",110,155) 
        text("2. If you click on a square containing a BOMB, you LOSE.",110,185)
        text("3. If you AVOID all the bombs and CLEAR the board, you WIN.",110,215)
        text("4. Clicking a square which doesn't have a bomb reveals the",110,245)
        text("NUMBER of neighbouring squares containing bombs within a", 110, 270)
        text("9x9 area: above, below, left, right, and diagonal.", 110, 295)
        text("5. If you open a square with 0 neighboring bombs, all the", 110, 325)
        text("neighboring squares will automatically open.",110,350)
        text("6. To OPEN a square, LEFT-CLICK on it. To MARK a square you",110,380)
        text("think is a bomb, RIGHT-CLICK on it.",110,405)
         
        # back button
        textSize(20)
        fill(255,255,255)
        text("<- Back", 10,25)
    #############################################
    # WHEN ON HIGH SCORE SCREEN
    if mode == "high-score": # high scores
        # Title
        textSize(50)
        fill(255, 204, 133)
        text("HIGH SCORES", 240, 80)
        
        # back button
        textSize(20)
        fill(255,255,255)
        text("<- Back", 10,25)
        
        # headers
        textSize(25)
        fill(255, 204, 133)
        text("RANK",80,150)
        text("NAME",230,150) 
        text("SCORE",580,150) 
        
        # display player scores
        fill(255,255,255)
        highscores.display()
    #############################################
    # WHEN IN MAIN GAME MODE
    if mode == "game-on":
        
        # back button
        textSize(20)
        fill(255,255,255)
        text("<- Back", 10,25)
        
        # draw title
        textSize(35)
        strokeWeight(2)
        fill(255, 204, 133)
        text("MINESWEEPER",295,40)
        
        # draw timer
        textSize(30)
        fill(255,255,255)
        sw.draw()
        # draw number of remaining bombs aka flags placed
        text("Flags: " + str(flags),15,440)
        
        # draw game grid
        pushMatrix()
        # centering gameboard
        translate(230,50)
        # changing colour and increasing weight of stroke to match tile images
        stroke(100)
        strokeWeight(1.5)
        
        y=0
        for row in grid:
            x=0
            for tile in row:
                # draw BOMB tile
                if tile.bomb == True:
                    fill(255,0,0)
                    # load image of covered tile
                    image(covered,x,y,w,w)
                        
                # draw UNCOVERED tile
                elif tile.visible:
                    # fill w/ grey
                    fill(185,185,180)
                    rect(x,y,w,w) 
                    
                # draw COVERED tile
                elif not tile.visible: 
                    # load image of covered tile
                    image(covered,x,y,w,w)

                # flag tile
                if tile.flagged:
                    # load image of flag tile
                    image(flagtile,x,y,w,w)
                
                # draw num of adj bombs
                fill(0,0,0)
                if tile.label != None:
                    # adding in numbered tiles
                    if tile.label == 1:
                        image(one_bomb,x,y,w,w)
                    elif tile.label == 2:
                        image(two_bomb,x,y,w,w)
                    elif tile.label == 3:
                        image(three_bomb,x,y,w,w)
                    elif tile.label == 4:
                        image(four_bomb,x,y,w,w)
                # move onto the next column    
                x+=w
            # move onto the next row
            y+=w
            
        popMatrix()
    #############################################
    # WHEN ON GAME WON SCREEN
    if mode == "game-won":
        textSize(20)
        fill(255,255,255)
        textSize(30)
        text("You won!",350,100)
        textSize(25)
        # display elapsed time
        text("Time:" + nf(sw.minutes(),2)+":"+nf(sw.seconds(),2),350,200)
        # display total bombs found (i.e. flags placed)
        text("Bombs found:" + nf(flags),325,250)
        text("Press m to return to main menu",220,300)
        text("Press n to play again",270,350)
        image(winface,20,40,100,100)
        image(winface,680,40,100,100)
    #############################################
    # WHEN ON GAME LOST SCREEN
    if mode == "game-lost":
        textSize(20)
        fill(255,255,255)
        textSize(30)
        text("You lost!",350,100)
        textSize(25)
        # display elapsed time
        text("Time:" + nf(sw.minutes(),2)+":"+nf(sw.seconds(),2),350,200)
        # display total bombs found (i.e. flags placed)
        text("Bombs found:" + nf(flags),325,250)
        text("Press m to return to main menu",220,300)
        text("Press n to play again",270,350)
        image(loseface,20,40,100,100)
        image(loseface,680,40,100,100)
#################################################################
def keyPressed():
    global mode,level
        
    # game over, return to main menu
    if key == "m" and (mode == "game-won" or mode == "game-lost"): 
        mode = "title"
        # resetting game components
        reset_game()
        sw.reset()

    # game over, play again
    if key == "n" and (mode == "game-won" or mode == "game-lost"): 
        mode = "game-on"
        # resetting game components
        reset_game()
        sw.reset()
#################################################################
# function tracking the player's move
def mouse_coord():
    # -230 and -50 because we used pushMatrix and popMatrix 
    # to translate grid towards the center
    x=(mouseX-230)/w
    y=(mouseY-50)/w
    # return mouse coordinates
    return (x,y)
#################################################################
def mousePressed():
    global mode,flags,bombs,click
    # get mouse coordinates
    (x,y) = mouse_coord()
    
    # back button / return to main screen available on all screens
    if (0 < mouseX < 40) and (0 < mouseY < 40):
        mode = "title"
        # reset grid and stopwatch
        reset_game()
        sw.reset()
    
    # GAME MODE selection on TITLE screen
    if mode == "title":
        if (30 < mouseX < 240) and (250 < mouseY < 310):
            # go into game on mode
            mode = "game-on" 
        elif (295 < mouseX < 505) and (250 < mouseY < 310):
            # go into high score screen
            mode = "high-score"
        elif (560 < mouseX < 770) and (250 < mouseY < 310):
            # go into instruction screen
            mode = "instructions" 

    # WHEN NOT ON THE TITLE SCREEN
    else:
        # IF ON MAIN GAME MODE
        if mode == "game-on":
            # left click to uncover tiles
            if mouseButton == LEFT:
                # searching for neighbouring bombs on visible tiles
                search(x,y)
                
                # current tile is the spot on the grid that the player clicked
                tile = grid[y][x]
                # increase number of clicks each time
                click +=1
                # guarantee that the first move is never a mine
                # if the first move/click is a mine
                if tile.bomb and click == 1:
                    print(click)
                    # remove the mine from that tile
                    tile.bomb = False
                    
                    # place the mine somewhere else randomly
                    x = randint(0,8) # randomly select a bomb position
                    y = randint(0,8)
                    grid[y][x].bomb = True
                
                # check if the player has lost after each left click
                check_lose(tile)

            # right click mouse to flag tile
            elif mouseButton == RIGHT:
                '''
                NOTE: instead of setting the tile is flagged or unflagged, right clicking will simply set the tile to the opposite value
                If it is not flagged, then flag it. If it is flagged, and the player right-clicks, then unflag it.
                '''
                tile = grid[y][x]
                tile.flagged = not tile.flagged

            # check if there is a winner after each click
            check_win()
#################################################################
# function to look for number of bombs adjacent to the tile being looked at
# assigns the corresponding number to the tile to indicate how many bombs are neighbouring it
def search(x,y):
    # BASE CASES
    # already visited/bomb/off grid/adjacent bombs
    # BASE CASE 1: do not put a label if the tile is off grid
    if not ongrid(x,y):
        return 
    tile = grid[y][x]
    # BASE CASE 2: do not put a label if the tile is already visited
    if tile.visible:
        return
    
    # BASE CASE 3: do not put a label if the tile is a bomb
    if tile.bomb:
        return
    
    # reveal the tile
    tile.visible = True
    
    # check for number of bombs
    s = num_of_bombs(x,y)
    
    # assign tile a label (indicating the number of adjacent bombs)
    if s > 0:
        grid[y][x].label = s
        return 

    '''
    Cell-->Current Cell (row, col) 
    N - (row-1, col) / S - (row+1, col) / E - (row, col+1) / W - (row, col-1) 
    NE - (row-1, col+1) / NW- (row-1, col-1) / SE- (row+1, col+1) / SW- (row+1, col-1) 
    '''
    # RECURSIVE PART
    # checking up, down, left, right, diagonals
    for (dx,dy) in [(-1,0), (1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1) ]:
        search(x+dx,y+dy)
#################################################################
# function to count number of bombs in the adjacent cells of the tile
def num_of_bombs(x,y): # checking for number of bombs around the tile clicked
    # set number to 0
    s=0
    # looking through the 9x9 area for number of bombs
    for (dx,dy) in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1) ]:
        # if the tile is within bounds, and it is a bomb
        if ongrid(x+dx,y+dy) and grid[y+dy][x+dx].bomb:
            # tally it
            s+=1
    # return total number of bombs
    return s
#################################################################
# function to check whether cell is valid
def ongrid(x,y): 
    # returns true if click is within gameboard
    if x>=0 and x < COLS and y >= 0 and y < ROWS:
        return True
    return False
#################################################################
# function to reset gameboard at the end of each game
def reset_game(): 
    global grid,flags
    flags = 0
    click = 0
    # resetting all tiles to covered and unflagged
    for row in grid:
        for t in row:
            t.reset()
    grid = [[Tile() for n in range(COLS)] for n in range(ROWS)]
    # resetting mine placement
    place_mines()
#################################################################
# function to check if player has lost by clicking on a bomb
def check_lose(tile): 
    # if the player has lost, the game is over and the game over screen is displayed
    global mode
    if tile.bomb == True and tile.flagged == False: 
        # if player clicked on unflagged bomb tile, they lose
        game_won = False
        sw.stop()
        mode = "game-lost"
    
#################################################################
# function to check if player has won by clearing the board
def check_win(): 
    # if the player has won, the game is won and the game won screen is displayed
    global mode,flags
    
    # setting values
    game_won = True
    flags = 0
    # go through the grid
    for row in grid:
        for t in row:
            # if there is still a tile that isn't a bomb and hasn't been revealed 
            # the player did not win yet
            if t.bomb == False and t.visible == False:
                game_won = False
                
            # find the number of flagged tiles and tally it
            if t.bomb and t.flagged:
                flags += 1
    '''
    NOTE: I realized that this is not a proper method to win, because the player might but 10 flags in the wrong spot.
    This is not a win, but the condition that I stated here indicates as such as allows for the player to "cheat" by guessing in this way.        
    # if ALL BOMBS are FLAGGED, the player wins
    if flags == bombs:
        mode = "game-won"
        sw.stop()
   '''
   # if ALL TILES are REVEALED, the player wins         
    if game_won: 
        print("won")
        sw.stop()
        mode = "game-won"
##########################################################################################
# UNINCLUDED CONTENT
# DIFFICULTY SELECTION
'''
def chooseDifficulty():
    global ROWS,COLS, bombs,level
# BEGINNER = 9 * 9 Cells and 10 Mines 
# INTERMEDIATE = 16 * 16 Cells and 40 Mines 
# ADVANCED = 24 * 24 Cells and 99 Mines 
    if level == "BEGINNER":
        ROWS = 9
        COLS = 9 
        bombs = 10
        mode = "game-on" 
    elif level == "INTERMEDIATE":
        ROWS = 16
        COLS = 16
        bombs = 40  
        mode = "game-on"
    elif level == "ADVANCED": 
        ROWS = 24
        COLS = 24
        bombs = 99 
    return ROWS,COLS, bombs
chooseDifficulty()
# IN MAIN DRAW FUNCTION
    if mode == "difficulty": 
        textSize(20)
        fill(255,255,255)
        text("Enter the Difficulty Level",100,113); 
        text("Press 0 for BEGINNER (9 x 9 Cells and 10 Mines)",100,190)
        text("Press 1 for INTERMEDIATE (16 x 16 Cells and 40 Mines)",100,240)
        text("Press 2 for ADVANCED (24 x 24 Cells and 99 Mines)",100,290)
        
# IN KEYPRESSED
    # selecting difficulty
    if key == "0" and mode == "difficulty":
        level = "BEGINNER"
        mode = "game-on"
    elif key == "1" and mode == "difficulty":
        level = "INTERMEDIATE"
        mode = "game-on"
    elif key == "2" and mode == "difficulty":
        level = "ADVANCED"
        mode = "game-on"
        
#################################################################
# IN SCOREBOARD CLASS
# SORTING PLAYER SCORES IN ORDER
def insertion_sort(self):
    # sorting the players in ascending order
    for i in self.players: 
        current = self.players[i] # current player
        position = i-1 # keep moving down the list to the start to compare
        # Move numbers that are greater than the current number to one position ahead of their current position 
        while position >= 0 and current < self.players[position]:
            # swapping positions 
            temp = self.players[i]
            self.player[i] = self.player[i+1]
            self.player[i+1] = temp

    return self.players

'''
##########################################################################################
