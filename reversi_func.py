import random

n = 8
minEvalBoard = -1 # min - 1
maxEvalBoard = n * n + 4 * n + 4 + 1 # max + 1

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def isValidMove(grid, tile, xstart, ystart):
    if grid[ystart][xstart] == 1 or grid[ystart][xstart] == 2 or not isOnBoard(xstart, ystart):
        return False
    
    if tile == 2:
        otherTile = 1
    else:
        otherTile = 2

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and grid[y][x] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while grid[y][x] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):  # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if grid[y][x] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    grid[ystart][xstart] = 0  # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

    
def getValidMove(grid, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(grid, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def makeMove(grid, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(grid, tile, xstart, ystart)
    if tilesToFlip == False:
        return False

    grid[ystart][xstart] = tile
    for x, y in tilesToFlip:
        grid[y][x] = tile
    return True

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def count_points(grid):
    whites = 0
    blacks = 0
    for i in grid:
        for z in i:
            if z == 1:
                blacks += 1
            elif z == 2:
                whites += 1
    return [blacks, whites]

def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([0] * 8)

    return board

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {1:xscore, 2:oscore}

def Minimax(board, tile, depth, maximizingPlayer):
    if depth == 0 or IsTerminalNode(board, tile):
        return getScoreOfBoard(board)[tile]
    possibleMoves = getValidMove(board, tile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    if maximizingPlayer:
        bestValue = minEvalBoard
        for y in range(n):
            for x in range(n):
                if isValidMove(board,tile, x, y):
                    dupeBoard = getBoardCopy(board)
                    makeMove(dupeBoard, tile, x, y)
                    v = Minimax(dupeBoard, tile, depth - 1, False)
                    bestValue = max(bestValue, v)
    else: # minimizingPlayer
        bestValue = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if isValidMove(board, tile, x, y):
                    dupeBoard = getBoardCopy(board)
                    makeMove(dupeBoard, tile, x, y)
                    v = Minimax(dupeBoard, tile, depth - 1, True)
                    bestValue = min(bestValue, v)
    return bestValue

def IsTerminalNode(board, tile):
    possibleMoves = getValidMove(board, tile)
    if possibleMoves.__len__ == 0:
        return False
    return True


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMove(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    #for x, y in possibleMoves:
    for y in range(n):
            for x in range(n):
                if isValidMove(board,computerTile, x, y):
                    dupeBoard = getBoardCopy(board)
                    makeMove(dupeBoard, computerTile, x, y)
                    score = Minimax(dupeBoard,computerTile,5,True)
                    if score > bestScore:
                        bestMove = [x, y]
                        bestScore = score            
    return bestMove

