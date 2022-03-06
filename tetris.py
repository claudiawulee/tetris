from tkinter import *
import random, copy


# lowkeyclaud

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return [rows, cols, cellSize, margin]


def getTetrisPieces():
    # Seven "standard" pieces

    iPiece = [
        [True, True, True, True]
    ]

    jPiece = [
        [True, False, False],
        [True, True, True]
    ]

    lPiece = [
        [False, False, True],
        [True, True, True]
    ]

    oPiece = [
        [True, True],
        [True, True]
    ]

    sPiece = [
        [False, True, True],
        [True, True, False]
    ]

    tPiece = [
        [False, True, False],
        [True, True, True]
    ]

    zPiece = [
        [True, True, False],
        [False, True, True]
    ]
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]


def init(data):
    # Set up simulation components

    data.rows, data.cols, data.cellSize, data.margin = gameDimensions()
    data.board = []
    data.isGameOver = False
    data.score = 0
    for x in range(data.rows):
        data.emptyColor = ["blue"]
        data.emptyColorRows = data.emptyColor * data.cols
        #print(data.emptyColorRows)
        data.board.append(data.emptyColorRows)

    # pre-load cells - testing
    # data.board[0][0] = "red" # top-left is red
    # data.board[0][data.cols-1] = "white" # top-right is white
    # data.board[data.rows-1][0] = "green" # bottom-left is green
    # data.board[data.rows-1][data.cols-1] = "gray" # bottom-right is gray
    # print(data.board)

    data.tetrisPieces = getTetrisPieces()
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    newFallingPiece(data)


def redrawAll(canvas, data):
    # simulation view
    drawBoard(canvas, data)
    drawScore(canvas, data)
    drawFallingPiece(canvas, data)
    if data.isGameOver == True:
        drawGameOver(canvas, data)



def drawBoard(canvas, data):
    canvas.create_rectangle(0, 0, data.margin * 2 + data.cols * data.cellSize,
                            data.margin * 2 + data.rows * data.cellSize, fill="orange")
    for x in range(data.rows):
        for y in range(data.cols):
            drawCell(canvas, data, x, y, data.board[x][y])


def drawCell(canvas, data, row, col, fillColor):
    canvas.create_rectangle(col * data.cellSize + data.margin, row * data.cellSize + data.margin,
                            col * data.cellSize + data.cellSize + data.margin,
                            row * data.cellSize + data.cellSize + data.margin, fill=fillColor)



def newFallingPiece(data):
    data.fallingPieceNum = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[data.fallingPieceNum]
    # print(data.fallingPiece)

    # print(data.fallingPieceColorNum)
    data.fallingPieceColor = data.tetrisPieceColors[data.fallingPieceNum]
    # print(data.fallingPieceColor)

    data.fallingPieceRow = 0
    data.numFallingPieceRows = len(data.fallingPiece)
    data.numFallingPieceCol = len(data.fallingPiece[0])
    data.fallingPieceCol = data.cols // 2 - data.numFallingPieceCol // 2



def drawFallingPiece(canvas, data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[0])):
            if data.fallingPiece[x][y] and data.board[x][y] == 'blue':
                drawCell(canvas, data, data.fallingPieceRow + x, data.fallingPieceCol + y, data.fallingPieceColor)


def fallingPieceIsLegal(data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[x])):
            if data.fallingPiece[x][y] == True:
                newCol = data.fallingPieceCol + y
                newRow = data.fallingPieceRow + x
                # print(newCol)
                # print(newRow)
                if newCol < 0 or newCol >= data.cols or newRow < 0 or newRow >= data.rows:
                    return False
                if data.board[newRow][newCol] != "blue":
                    return False
    return True


def moveFallingPiece(data, drow, dcol):
    # location give by data.fallingPieceRow/Col change by drow and dcol
    data.fallingPieceRow += drow  # standards
    data.fallingPieceCol += dcol
    # print(data.fallingPieceCol)
    # print(fallingPieceIsLegal(data))
    moveOccurred = True
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        moveOccurred = False
    return moveOccurred



def rotateFallingPiece(data):
    oldPiece = copy.deepcopy(data.fallingPiece)
    tmpRow = data.fallingPieceRow  # where on the board piece is
    tmpCol = data.fallingPieceCol
    tmpDimRow = len(data.fallingPiece)  # actual dimensions of columns and rows
    tmpDimCol = len(data.fallingPiece[0])
    tempPiece = data.fallingPiece

    newDimRow = tmpDimCol
    newDimCol = tmpDimRow
    outerLst = []
    for item in range(newDimRow):
        innerLst = []
        for item2 in range(newDimCol):
            innerLst.append(None)
        outerLst.append(innerLst)
    # print(outerLst)

    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            outerLst[len(data.fallingPiece[row]) - 1 - col][row] = data.fallingPiece[row][col]
    # print(outerLst)
    data.fallingPiece = outerLst

    data.centerRow = tmpRow + tmpDimRow // 2 - len(data.fallingPiece) // 2
    data.centerCol = tmpCol + tmpDimCol // 2 - len(data.fallingPiece[0]) // 2
    data.fallingPieceRow = data.centerRow
    data.fallingPieceCol = data.centerCol
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = oldPiece
        # bug: rotating block near edge cause edge piece (not the center) to go out of bounds
        # fixed with the copy.deepcopy to save OldPiece
        data.fallingPieceRow = tmpRow
        data.fallingPieceCol = tmpCol


def placeFallingPiece(data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[0])):
            if data.fallingPiece[x][y] == True:
                data.board[data.fallingPieceRow + x][data.fallingPieceCol + y] = data.fallingPieceColor
    removeFullRows(data)

def drawGameOver(canvas, data):
    for x in range(1, 4):
        for y in range(data.cols):
            data.board[x][y] = "black"  # bug: the next new falling piece appears and covers part of game over message (Fixed)
    canvas.create_text(data.width / 2, data.height / 5.5, text='Game over!',
                       font='Arial 24 bold',
                       fill='ghost white')
    canvas.create_text(data.width / 2, data.height / 6 + 28,
                       text='Press r to restart!',
                       font='Arial 18 bold',
                       fill='ghost white')


def removeFullRows(data):
    #move rows above down that do not contain
    newBoard = []
    numRowsRemoved = 0
    rowsKept = 0
    #create new board and copy unfilled rows to it in correct order by checking if emptyColor occurs in the row
    for row in data.board:
        #print(row)
        #means blue is in row and row is not filled (needs to be copied over to new board)
        if data.emptyColor[0] in row: #original mistake was checking data.emptyColor which returns ['blue'] so this if statement would always be false
            newBoard.append([])
            for col in row:
                newBoard[rowsKept].append(col)
            rowsKept+=1
            #print(newBoard)
        else:#clear rows  empty color (blue)
            numRowsRemoved +=1 #keep track of full rows removed

    #fill top with empty rows
    while len(newBoard) < data.rows:
        newBoard = [data.emptyColor*data.cols] + newBoard

    # set new board to data.board
    data.board = newBoard

    #keep score
    data.score += numRowsRemoved**2

def drawScore(canvas, data):
    canvas.create_text(data.width / 2, data.cellSize - 5, text = 'Score: ' + str(data.score), font = 'Arial 15 bold')


def timerFired(data, canvas):
    # Write your simulation rules here, by changing data
    if data.isGameOver == True:
        return
    moveFallingPiece(data, 1, 0)
    if (moveFallingPiece(data, 1, 0) == False):
        placeFallingPiece(data)
        #redrawAll(canvas,data)
        newFallingPiece(data)
    if fallingPieceIsLegal(data) == False:
        data.isGameOver = True


def keyPressed(canvas, event, data):  # added canvas variable
    # Use event.char to get the character pressed
    if event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    elif event.keysym == "Right":
        moveFallingPiece(data, 0, 1)
    elif event.keysym == "Down":
        moveFallingPiece(data, 1, 0)
    elif event.keysym == "w":
        rotateFallingPiece(data)
    elif event.keysym == "r":
        init(data)
    elif data.isGameOver == True:
        return


def mousePressed(event, data):
    # Use event.x and event.y to get the (x,y) location of the clicked pixel
    pass


#done

def timeLoop(data, canvas):
    timerFired(data,canvas)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()

    canvas.after(data.timeRate, timeLoop, data, canvas)


def keyEventHandler(data, canvas, event):
    keyPressed(canvas, event, data)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()


def mouseEventHandler(data, canvas, event):
    mousePressed(event, data)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()


class Model:
    pass


def runSimulation(w, h, rate):
    data = Model()
    data.width = w
    data.height = h
    data.timeRate = int(rate * 1000)  # call will be in ms
    init(data)

    root = Tk()
    canvas = Canvas(root, width=w, height=h)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    redrawAll(canvas, data)

    canvas.after(data.timeRate, timeLoop, data, canvas)

    root.bind("<Key>", lambda event: keyEventHandler(data, canvas, event))
    root.bind("<Button-1>", lambda event: mouseEventHandler(data, canvas, event))

    root.mainloop()


def playTetris():
    [rows, cols, cellSize, margin] = gameDimensions()
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
    runSimulation(width, height, 0.7)


playTetris()
