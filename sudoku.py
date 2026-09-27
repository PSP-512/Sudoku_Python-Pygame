import numpy as np
import random
import pygame
import pathlib
import time

#generation du sudoku et de sa solution
def is_valid(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in random.sample(range(1, 10), 9):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate_sudoku():
    grid = np.zeros((9, 9), dtype=int)
    solve_sudoku(grid)
    return grid

def remove_numbers(grid, count):
    while count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            count -= 1
    return grid


#mise en place de l'interface
pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
icone = pygame.image.load("sudoku.png")
pygame.display.set_icon(icone)
pygame.display.set_caption("Sudoku Game")
 
CELL = 38
OX = (W - 9 * CELL) // 2
OY = 55
BTN_H = 44
NUM_Y = OY + 9 * CELL + 15
BTN_Y = NUM_Y + BTN_H + 15

puzzle = None
solution = None
user_grid = None
fixed = None
sel_r, sel_c = -1, -1
errors = None
solved = False
difficult = 1
settings = False
life = 0
life_nb = 5
timer = False
end = False
time_open_menu = 0
start_pause = None

def new_party():
    global  settings, end
    settings = False
    end = False
    new_game()

def new_game():
    global puzzle, solution, user_grid, fixed, sel_r, sel_c, errors, solved, sudoku_solved, time_open_menu, start_pause, life_nb
    if difficult == 1 : 
        number_removed = random.randint(20, 30)
    elif difficult == 2:
        number_removed = random.randint(30, 40)
    elif difficult == 3:
        number_removed = 50
    elif difficult == 4:
        number_removed = 60
    sudoku_solved = generate_sudoku()
    print(sudoku_solved)

    sudoku_grid = remove_numbers(sudoku_solved.copy(), number_removed)
    print(sudoku_grid)

    puzzle = [row[:] for row in sudoku_grid]
    solution = [row[:] for row in sudoku_solved]
    user_grid = [row[:] for row in puzzle]

    fixed = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
    sel_r, sel_c = -1, -1
    errors = [[False] * 9 for _ in range(9)]
    solved = False
    time_open_menu = 0
    if life == 1 :
        life_nb = 5
    elif life == 2 :
        life_nb = 3
    elif life == 3 :
        life_nb = 1
    if timer == True :
        start_pause = pygame.time.get_ticks()
 
def check_errors():
    global errors, solved,life_nb
    errors = [[False] * 9 for _ in range(9)]
    full = True
    for r in range(9):
        for c in range(9):
            if user_grid[r][c] == 0:
                full = False
            elif not fixed[r][c] and user_grid[r][c] != solution[r][c]:
                errors[r][c] = True
                if life != 0 :
                    life_nb -=1
                    if life_nb == 0:
                        end_game()
    if full and not any(errors[r][c] for r in range(9) for c in range(9)):
        solved = True
 
def draw():
    global Chrono, time_open_menu

    screen.fill((245, 245, 250))
    font = pygame.font.Font(None, 30)
    title = font.render("Sudoku", True, (50, 50, 50))
    screen.blit(title, title.get_rect(center=(W // 2, 25)))
 
    if solved:
        end_game()
 
    nf = pygame.font.Font(None, 28)
    for r in range(9):
        for c in range(9):
            x = OX + c * CELL
            y = OY + r * CELL
            if r == sel_r and c == sel_c:
                pygame.draw.rect(screen, (200, 220, 255), (x, y, CELL, CELL))
            elif (r // 3 + c // 3) % 2 == 0:
                pygame.draw.rect(screen, (230, 230, 240), (x, y, CELL, CELL))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, CELL, CELL))
            pygame.draw.rect(screen, (180, 180, 180), (x, y, CELL, CELL), 1)
            val = user_grid[r][c]
            if val != 0:
                if errors[r][c]:
                    color = (220, 50, 50)
                elif fixed[r][c]:
                    color = (30, 30, 30)
                else:
                    color = (30, 80, 200)
                t = nf.render(str(val), True, color)
                screen.blit(t, t.get_rect(center=(x + CELL // 2, y + CELL // 2)))
 
    for i in range(4):
        lx = OX + i * 3 * CELL
        pygame.draw.line(screen, (40, 40, 40), (lx, OY), (lx, OY + 9 * CELL), 2)
    for i in range(4):
        ly = OY + i * 3 * CELL
        pygame.draw.line(screen, (40, 40, 40), (OX, ly), (OX + 9 * CELL, ly), 2)
 
    num_rects = []
    nbw = 38
    total = 9 * nbw + 8 * 3
    nx_start = (W - total) // 2
    for i in range(9):
        nx = nx_start + i * (nbw + 3)
        rect = pygame.Rect(nx, NUM_Y, nbw, BTN_H)
        pygame.draw.rect(screen, (70, 130, 180), rect, border_radius=6)
        nt = nf.render(str(i + 1), True, (255, 255, 255))
        screen.blit(nt, nt.get_rect(center=rect.center))
        num_rects.append(rect)
 
    bf = pygame.font.Font(None, 24)
    check_rect = pygame.Rect(W // 2 - 120, BTN_Y, 100, 38)
    pygame.draw.rect(screen, (80, 160, 80), check_rect, border_radius=6)
    ct = bf.render("vérifier", True, (255, 255, 255))
    screen.blit(ct, ct.get_rect(center=check_rect.center))
 
    clr_rect = pygame.Rect(W // 2 , BTN_Y,100, 38)
    pygame.draw.rect(screen, (150, 150, 160), clr_rect, border_radius=6)
    clt = bf.render("effacer", True, (255, 255, 255))
    screen.blit(clt, clt.get_rect(center=clr_rect.center))

    #boutton de parametre
    settings_btn = pygame.Rect(250,5,50,50)
    text_settings = pygame.image.load(pathlib.Path("settings.png"))
    text_settings = pygame.transform.scale(text_settings,(50,50))
    screen.blit(text_settings,(250,5))
    if timer == True and end == False:
        if settings == False and start_pause is not None :
            time = time_open_menu +( pygame.time.get_ticks() - start_pause )
        else :
            time =time_open_menu
        minutes = time // 60000
        secondes = (time % 60000)//1000
        Chrono = font.render(f"{minutes:02d}:{secondes:02d}", True, (50, 50, 50))
        screen.blit(Chrono, (310, 19))

    if settings == True :

        background = pygame.Rect(15,50, 370, 520)
        pygame.draw.rect(screen, (200, 200, 200), background, border_radius= 8)

        Valid_rect =  pygame.Rect(290, 530, 90, 34)
        pygame.draw.rect(screen, (0, 180, 0), Valid_rect, border_radius=6)
        valt = bf.render("Validé", True, (0, 0, 0))
        screen.blit(valt, valt.get_rect(center=Valid_rect.center))

        difficult_txt = font.render("Niveau",True,(0,0,0))
        screen.blit(difficult_txt, (150,80))
        if difficult == 1 : 
            diff_rect =  pygame.Rect(150, 120, 90, 34)
            pygame.draw.rect(screen, (0, 180, 0), diff_rect, border_radius=6)
            dift = bf.render("facile", True, (0, 0, 0))
            screen.blit(dift, dift.get_rect(center=diff_rect.center))
        elif difficult == 2:
            diff_rect = pygame.Rect(150, 120, 90, 34)
            pygame.draw.rect(screen, (0, 100, 0), diff_rect, border_radius=6)
            dift = bf.render("moyen", True, (0, 0, 0))
            screen.blit(dift, dift.get_rect(center=diff_rect.center))
        elif difficult == 3:
            diff_rect = pygame.Rect(150, 120, 90, 34)
            pygame.draw.rect(screen, (180, 0, 0), diff_rect, border_radius=6)
            dift = bf.render("difficile", True, (0, 0, 0))
            screen.blit(dift, dift.get_rect(center=diff_rect.center))
            
        elif difficult == 4:
            diff_rect = pygame.Rect(150, 120, 90, 34)
            pygame.draw.rect(screen, (130, 0, 0), diff_rect, border_radius=6)
            dift = bf.render("extreme", True, (0, 0, 0))
            screen.blit(dift, dift.get_rect(center=diff_rect.center))

        life_txt = font.render("activer les Vies ?",True,(0,0,0))
        screen.blit(life_txt, (115,180))
        if life == 0 :
            life_rect = pygame.Rect(150, 220, 90, 34)
            pygame.draw.rect(screen, (128, 128, 128), life_rect, border_radius=6)
            lft = bf.render("Désactiver", True, (0, 0, 0))
            screen.blit(lft, lft.get_rect(center=life_rect.center))
        elif life == 1:
            life_rect = pygame.Rect(150, 220, 90, 34)
            pygame.draw.rect(screen, (0, 200, 0), life_rect, border_radius=6)
            lft = bf.render("Facile", True, (0, 0, 0))
            screen.blit(lft, lft.get_rect(center=life_rect.center))
        elif life == 2:
            life_rect = pygame.Rect(150, 220, 90, 34)
            pygame.draw.rect(screen, (0, 150, 0), life_rect, border_radius=6)
            lft = bf.render("Normal", True, (0, 0, 0))
            screen.blit(lft, lft.get_rect(center=life_rect.center))
        elif life == 3:
            life_rect = pygame.Rect(150, 220, 90, 34)
            pygame.draw.rect(screen, (0, 120, 0), life_rect, border_radius=6)
            lft = bf.render("One Life", True, (0, 0, 0))
            screen.blit(lft, lft.get_rect(center=life_rect.center))
        



        timer_txt = font.render("activer le chronomètre ?",True,(0,0,0))
        screen.blit(timer_txt, (80,280))
        if timer == False :
            timer_rect = pygame.Rect(150, 320, 90, 34)
            pygame.draw.rect(screen, (128, 128, 128), timer_rect, border_radius=6)
            timt = bf.render("Désactiver", True, (0, 0, 0))
            screen.blit(timt, timt.get_rect(center=timer_rect.center))
        elif timer == True:
            timer_rect = pygame.Rect(150, 320, 90, 34)
            pygame.draw.rect(screen, (0, 200, 0), timer_rect, border_radius=6)
            timt = bf.render("Activer", True, (0, 0, 0))
            screen.blit(timt, timt.get_rect(center=timer_rect.center))

        new_txt = font.render("autre Sudoku ?",True,(0,0,0))
        screen.blit(new_txt, (120,400))

        new_rect = pygame.Rect(146,450, 100, 38)
        pygame.draw.rect(screen, (100, 100, 220), new_rect, border_radius=6)
        nt2 = bf.render("Nouveau", True, (0, 0, 0))
        screen.blit(nt2, nt2.get_rect(center=new_rect.center))
    if end == True :
        end_game()
    if life == 1 or life == 2 or life == 3:
        draw_life(life_nb)


 
    pygame.display.flip()
    return num_rects, check_rect, clr_rect, 

def draw_life(life):
    x = 0
    for coeur in range(life):
        x += 25
        circle = pygame.draw.circle(screen, (220,0,0), (x,25), 10)

def end_game():
    global end
    end = True
    background = pygame.Rect(15,50, 370, 520)
    pygame.draw.rect(screen, (200, 200, 200), background, border_radius= 8)
    if solved == True:
        sf2 = pygame.font.Font(None, 28)
        st2 = sf2.render("Terminer!", True, (0, 160, 0))
        st2 = pygame.transform.scale(st2,(200,60))
        screen.blit(st2, (100,120))
    else :

        sf2 = pygame.font.Font(None, 28)
        st2 = sf2.render("Perdu!", True, (160, 0, 0))
        st2 = pygame.transform.scale(st2,(200,60))
        screen.blit(st2, (100,120))

    if timer == True :
        time = pygame.font.Font(None, 28)
        times = time.render("ton temps :", True, (0, 0, 0))
        screen.blit(times, (150,200))

        end_Chrono = Chrono
        end_Chrono = pygame.transform.scale(end_Chrono,(100,30))
        screen.blit(end_Chrono,(150,250))


    re_retry = pygame.font.Font(None, 28)
    retry = re_retry.render("recommencer ?", True, (0, 0, 0))
    screen.blit(retry, (130,350))

    re_rect = pygame.Rect(125,390, 150, 57)
    pygame.draw.rect(screen, (0, 170, 0), re_rect, border_radius=6)
    re2 = bf.render("Oui", True, (0, 0, 0))
    screen.blit(re2, re2.get_rect(center=re_rect.center))

    re2_rect = pygame.Rect(150,450, 100, 38)
    pygame.draw.rect(screen, (165, 10, 10), re2_rect, border_radius=6)
    re3 = bf.render("Non", True, (0, 0, 0))
    screen.blit(re3, re3.get_rect(center=re2_rect.center))



new_game()
num_rects, check_rect, clr_rect = draw()
 
running = True
while running:
    if end == False:
        if settings == False :
            num_rects, check_rect, clr_rect = draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if settings_btn.collidepoint(mx, my):
                        settings = True
                        if timer == True and start_pause is not None :
                            time_open_menu += pygame.time.get_ticks() - start_pause
                            start_pause = None
                    if check_rect.collidepoint(mx, my):
                        check_errors()
                        num_rects, check_rect, clr_rect = draw()
                    if clr_rect.collidepoint(mx, my):
                        if 0 <= sel_r < 9 and 0 <= sel_c < 9 and not fixed[sel_r][sel_c]:
                            user_grid[sel_r][sel_c] = 0
                            errors[sel_r][sel_c] = False
                            num_rects, check_rect, clr_rect = draw()
                    if not solved:
                        for i, rect in enumerate(num_rects):
                            if rect.collidepoint(mx, my):
                                if 0 <= sel_r < 9 and 0 <= sel_c < 9 and not fixed[sel_r][sel_c]:
                                    user_grid[sel_r][sel_c] = i + 1
                                    errors[sel_r][sel_c] = False
                                    num_rects, check_rect, clr_rect = draw()
                                    break
                        else:
                            c = (mx - OX) // CELL
                            r = (my - OY) // CELL
                            if 0 <= r < 9 and 0 <= c < 9:
                                sel_r, sel_c = r, c
                            else:
                                sel_r, sel_c = -1, -1
                                num_rects, check_rect, clr_rect = draw()
        elif settings == True:
            diff_rect =  pygame.Rect(150, 120, 90, 34)
            pygame.draw.rect(screen, (0, 180, 0), diff_rect, border_radius=6)
            dift = bf.render("facile", True, (0, 0, 0))
            screen.blit(dift, dift.get_rect(center=diff_rect.center))

            life_rect = pygame.Rect(150, 220, 90, 34)
            timer_rect = pygame.Rect(150, 320, 90, 34)

            num_rects, check_rect, clr_rect = draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if settings_btn.collidepoint(mx, my):
                        settings = False
                        if timer == True and start_pause is None :
                            start_pause = pygame.time.get_ticks()
                    if life_rect.collidepoint(mx, my):
                        life += 1
                        life_activate = True
                        if life == 1:
                            life_nb = 5
                        elif life == 2:
                            life_nb = 3
                        elif life == 3 :
                            life_nb = 1
                        elif life == 4 :
                            life = 0
                    if timer_rect.collidepoint(mx, my):
                        if timer == False:
                            time_open_menu = 0
                            start_pause = None
                            timer = True
                        elif timer == True :
                            timer = False
                    if new_rect.collidepoint(mx, my):
                        new_game()
                        num_rects, check_rect, clr_rect = draw()
                        continue
                    if diff_rect.collidepoint(mx, my):
                        difficult += 1
                        if difficult == 5 :
                            difficult = 1
                        new_game()
                        draw()
                        continue
    elif end == True :
        re_rect = pygame.Rect(125,390, 150, 57)
        re2_rect  = pygame.Rect(150,450, 100, 38)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if re_rect.collidepoint(mx, my):
                    new_party()
                if re2_rect.collidepoint(mx, my):
                    running = False
            

    bf = pygame.font.Font(None, 24)

    settings_btn = pygame.Rect(250,5,50,50)
    new_rect = pygame.Rect(150,450, 100, 38)
    pygame.time.wait(30)
 
pygame.quit()
