#-----------------------------------------------------------------------
# sudoku.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 21/12/2020
# Version: 1.0
#-----------------------------------------------------------------------
import random
import time
from typing import List
import pygame

BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
VIOLET = (98, 0, 255)
DARK_GRAY= (175,175,175)
LIGHT_GRAY = (150,150,150)
LIGHTER_GRAY = (200, 200, 200)

def arrange(board:List[int]) -> List[int]:
    #Establece los numeros que forman cada caja, fila y columna para poder checkearlo despues
    listRow = []
    listColumn = [[], [], [], [], [], [], [], [], []]
    listBox = [[], [], [], [], [], [], [], [], []]
    for i in range(len(board)):
        listRow += [board[i]]
        for j in range(len(board[i])):
            listColumn[j] += [board[i][j]]
            if i <= 2:
                if j <= 2:
                    listBox[0] += [board[i][j]] 
                elif 3<= j <= 5:
                    listBox[1] += [board[i][j]]    
                else:
                    listBox[2] += [board[i][j]]    
            elif 3 <= i <= 5:
                if j <= 2:
                    listBox[3] += [board[i][j]] 
                elif 3<= j <= 5:
                    listBox[4] += [board[i][j]]    
                else:
                    listBox[5] += [board[i][j]]    
            else:
                if j <= 2:
                    listBox[6] += [board[i][j]] 
                elif 3<= j <= 5:
                    listBox[7] += [board[i][j]]    
                else:
                    listBox[8] += [board[i][j]] 
    return listRow, listColumn, listBox 

def check(listRow:List[int], listBox:List[int], listColumn:List[int]) -> bool:                   
    #Comprueba que no coincide ningun numero, que se estan cumpliendo las normas del sudoku
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if j != k:
                    if listRow[i][j] == listRow[i][k] and listRow[i][j] != 0:
                        return False
                    if listColumn[i][j] == listColumn[i][k] and listColumn[i][j] != 0:
                        return False
                    if listBox[i][j] == listBox[i][k] and listBox[i][j] != 0:
                        return False 
    return True          

def fixedPositions(board:List[int], listFixedPositions0 = []) -> List[int]:
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                listFixedPositions0 += [[i,j]]  
    return listFixedPositions0        

def updatePosition(row:int, column:int, backtrack:bool) -> int and int:
    #Si necesitamos volver a una casilla anterior porque no hay respuesta en la que nosotros estamos backtrack será true y volvera 1 casilla para atras
    #Si esta en la posicion 0 o 8 de columna saltara o recedera a la siguente o anterior fila
    if backtrack == True:
        if column == 0:
            row += -1
            column = 8
        else:
            column += -1
    elif backtrack == False:
        if column == 8:
            row += 1
            column = 0
        else:
            column += 1
    return row, column

def checkBacktrack(backtrack:bool, listFixedPositions0:List[int], row:int, column:int) -> bool:
    if backtrack == True and [row, column] in listFixedPositions0:
        backtrack = True
    else:
        backtrack = False  
    return backtrack   

def drawBoard(screen, board:List[int], listCorrect:List[int], color_x:int, color_y:int, cambioColor_x:int, cambioColor_y:int) -> int:
    font = pygame.font.SysFont('arial', 30)
    screen.fill(WHITE)
    color_x += cambioColor_x
    color_y += cambioColor_y
    color = (98 + color_x, 12 + color_y, 255)
    if  250 < 98 + color_x or 98 + color_x < 5:
        cambioColor_x = cambioColor_x * -1
    elif  250 < 12 + color_y or 12 + color_y < 5:
        cambioColor_y = cambioColor_y * -1   
    pygame.draw.rect(screen, color, (0, 0, 110, 60))
    text = font.render('Sudoku', True, WHITE)
    screen.blit(text, [10, 10])
    font = pygame.font.SysFont('arial', 20)
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, BLACK, (65 + (40 * j), 105 + (40 * i), 40, 40), 1)
            #pygame.draw.line(screen, BLACK, ())
            buttonStart(screen)
            if board[i][j] == 0:
                pygame.draw.rect(screen, WHITE, (66 + (40 * j), 106 + (40 * i), 38, 38), 1)
            elif listCorrect[i][j] == 1:
                pygame.draw.rect(screen, GREEN, (66 + (40 * j), 106 + (40 * i), 38, 38), 1)
            elif listCorrect[i][j] == 2:
                pygame.draw.rect(screen, RED, (66 + (40 * j), 106 + (40 * i), 38, 38), 1)    
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text, [80 + (40 * j), 115 + (40 * i)]) 
    return color_x, color_y, cambioColor_x, cambioColor_y            

def buttonStart(screen, buttonColor = DARK_GRAY) -> None:
    pos = pygame.mouse.get_pos()
    if  350 <= pos[0] <= 425 and 75 <= pos[1] <= 100: 
        buttonColor = LIGHT_GRAY
    pygame.draw.rect(screen, buttonColor, (350, 75, 75, 25))
    font = pygame.font.SysFont('arial', 16)
    text = font.render('SOLVE', True, BLACK)
    screen.blit(text, [365, 80])

def correct(correctBoard:bool, row:int, column:int, listCorrect:List[int]) -> List[int]:
    if correctBoard == True:
        listCorrect[row][column] = 1
    else:
        listCorrect[row][column] = 2                 
    return listCorrect

def main():  
    #Iniciamos el juego
    pygame.init()
    #Variables para representar la fila y columna donde estamos
    row = 0
    column = 0
    #variables para cambiar el color del titulo
    color_x = 0
    color_y = 0
    cambioColor_x = 5
    cambioColor_y = 5
    #Los numeros que estan en cada fila del sudoku
    board = [[0, 0, 3, 0, 4, 2, 0, 9, 0], [0, 9, 0, 0, 6, 0, 5, 0, 0], [5, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 7, 0, 0, 2, 8, 5], [0, 0, 8, 0, 0, 0, 1, 0, 0],
             [3, 2, 9, 0, 0, 8, 7, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 1], [0, 0, 5, 0, 9, 0, 0, 2, 0], [0, 8, 0, 2, 1, 0, 6, 0, 0]]   
    # Establecemos las dimensiones de la pantalla [largo,altura]
    dimensions = [533,533]
    screen = pygame.display.set_mode(dimensions) 
    pygame.display.set_caption('sudoku')
    #El bucle se ejecuta hasta que el usuario decida
    done = False
    #booleano para empezar la resolucion del sudoku
    start = False
    #Inicializando el booleano que hace al algortimo retroceder
    backtrack = False
    #lista que almacena los datos de las casillas ya resueltas
    listCorrect = []
    for i in range(9):
        listCorrect += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]   
    # Se usa para establecer cuan rápido se actualiza la pantalla
    clock = pygame.time.Clock()

    # -------- Bucle principal del Programa -----------         
    listFixedPositions0 = fixedPositions(board)                                      
    listRow, listColumn, listBox = arrange(board)       
    correctBoard = check(listRow, listBox, listColumn)
    if not correctBoard: 
        None     
    else:  
        while not start:
            pos = pygame.mouse.get_pos()
            color_x, color_y, cambioColor_x, cambioColor_y = drawBoard(screen, board, listCorrect, color_x, color_y, cambioColor_x, cambioColor_y)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    start = True
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        start = True
                        done = True    
                elif event.type == pygame.MOUSEBUTTONDOWN and 350 <= pos[0] <= 425 and 75 <= pos[1] <= 100:
                    start = True
        while not done:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                        done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
            while row < 9 and column < 9 and not done: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        done = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            done = True 
                correctBoard = False
                number = 1 
                backtrack = checkBacktrack(backtrack, listFixedPositions0, row, column) 
                if [row, column] not in listFixedPositions0:
                    while not correctBoard:
                        if board[row][column] < number:
                            board[row][column] = number
                            listRow, listColumn, listBox = arrange(board)       
                            correctBoard = check(listRow, listBox, listColumn)
                            listCorrect = correct(correctBoard, row, column, listCorrect)
                            color_x, color_y, cambioColor_x, cambioColor_y= drawBoard(screen, board, listCorrect, color_x, color_y, cambioColor_x, cambioColor_y)
                            pygame.display.flip()
                            #time.sleep(0.01)
                        number += 1
                        if number == 10 and correctBoard == False:
                            board[row][column] = 0
                            correctBoard = True
                            backtrack = True            
                row, column = updatePosition(row, column, backtrack)    
            clock.tick(1000)    
    pygame.quit()

if __name__ == '__main__': main()