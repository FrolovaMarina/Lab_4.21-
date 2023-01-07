from items import *
from extra import *
from board_data import *
import pygame as pg

pg.init()
font = pg.font.SysFont('calibry', 18, italic=True)


class Playboard:
    def __init__(self, parent_surface: pg.Surface):
        self.__screen = parent_surface
        self.__table = board
        self.__count = CELL_COUNT
        self.__size = CELL_SIZE
        self.__item_types = types
        self.__next_turn = 'white'
        self.__cells_sprite = pg.sprite.Group()
        self.__items_sprite = pg.sprite.Group()
        self.__items_white = []
        self.__items_black = []
        self.__queens_white = []
        self.__queens_black = []
        self.__items_coords = []
        self.__pressed_cell = None
        self.__picked_checker = None
        self.__CHECK = False
        self.__wqCHECK = False
        self.__bqCHECK = False
        self.__background()
        self.__draw_playboard()
        self.__draw_items()
        self.N = 0

        pg.display.update()

    #фон     
    def __background(self):
        background_image = pg.image.load('images/' + 'Ametist.jpg')
        background_image = pg.transform.scale(background_image, WINDOW_SIZE)
        self.__screen.blit(background_image, (0, 0))

    def __draw_playboard(self):
        total_size = self.__count * self.__size
        # номера полей
        numbers_fields = self.__numbers_fields()
        self.__cells_sprite = self.__create_cells()
        # сами игровые поля
        width = numbers_fields[0].get_width()
        board_view = pg.Surface((2 * width + total_size, 2 * width + total_size), pg.SRCALPHA)

        contour_image = pg.image.load('images/' + 'Sea_contour.jpg')
        contour_image = pg.transform.scale(contour_image, (board_view.get_width(), board_view.get_height()))
        board_view.blit(contour_image, contour_image.get_rect())

        board_view.blit(numbers_fields[0], (0, width))
        board_view.blit(numbers_fields[0], (width + total_size, width))
        board_view.blit(numbers_fields[1], (width, 0))
        board_view.blit(numbers_fields[1], (width, width + total_size))

        board_rect = board_view.get_rect()
        board_rect.x += (self.__screen.get_width() - board_rect.width) // 2
        board_rect.y += (self.__screen.get_height() - board_rect.height) // 2
        # прикрепление поверхности к screen
        self.__screen.blit(board_view, board_rect)
        cells_direction = (board_rect.x + width, board_rect.y + width)
        self.__draw_cells(cells_direction)

    def __numbers_fields(self):
        n_lines = pg.Surface((self.__count * self.__size, self.__size // 2), pg.SRCALPHA)
        n_rows = pg.Surface((self.__size // 2, self.__count * self.__size), pg.SRCALPHA)
        # корректировка клеток
        for i in range(0, self.__count):
            letters = font.render(names[i], 1, WHITE)
            number = font.render(str(self.__count - i), 1, WHITE)
            n_lines.blit(letters, (i * self.__size + (self.__size - letters.get_rect().width) // 2,
                                   (n_lines.get_height() - letters.get_rect().height) // 2)) 
            n_rows.blit(number, ((n_rows.get_width() - letters.get_rect().width) // 2,
                                 i * self.__size + (self.__size - number.get_rect().height) // 2)) 
        return n_rows, n_lines

    def __create_cells(self):
        group = pg.sprite.Group()
        even_count = (self.__count % 2 == 0)
        cell_colour_index = 1 if even_count else 0
        # отрисовка ячеек
        for y in range(self.__count):
            for x in range(self.__count):
                cells = Cells(cell_colour_index, self.__size, (x, y), names[x] + str(self.__count - y))
                group.add(cells)
                cell_colour_index ^= True
            cell_colour_index = cell_colour_index ^ True if even_count else cell_colour_index
        return group

    # смещение и прорисовка ячеек со спрайтами
    def __draw_cells(self, direction):
        for cells in self.__cells_sprite:
            cells.rect.x += direction[0]
            cells.rect.y += direction[1]
        self.__cells_sprite.draw(self.__screen)

    # отрисовка фигурок на соответствующие поля
    def __draw_items(self):
        self.__run_board()
        self.__black_or_white()
        self.__items_sprite.draw(self.__screen)

    def __run_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    item = self.__create_item(field_value, (j, i))
                    self.__items_sprite.add(item)
        for item in self.__items_sprite:
            for cells in self.__cells_sprite:
                if item.field_name == cells.field_name:
                    item.colour = cells.colour
                    item.rect = cells.rect

    # table_coord = координаты в матрице
    def __create_item(self, item_symbol: str, table_coord: tuple):
        field_name = self.__to_field_name(table_coord)
        item_tuple = self.__item_types[item_symbol]
        classname = globals()[item_tuple[0]]
        return classname(self.__size, item_tuple[0], field_name)

    def __to_field_name(self, table_coord: tuple):
        return names[table_coord[1]] + str(self.__count - table_coord[0])

    def __get_cell(self, position: tuple):
        for cells in self.__cells_sprite:
            if cells.rect.collidepoint(position):
                return cells
        return None

    def button_down(self, button_type: int, position: tuple):
        self.__pressed_cell = self.__get_cell(position)

    def button_up(self, button_type: int, position: tuple):
        released_cell = self.__get_cell(position)
        # проверка на то, кликнул ли пользователь на поле
        if (released_cell is not None) and (released_cell == self.__pressed_cell):
            if button_type == 1:
                self.__pick_cell(released_cell)
        self.__update()

    def __black_or_white(self):
        for item in self.__items_sprite:
            if item.icolour == Checker1.icolour:
                self.__items_white.append(item.field_name)
            elif item.icolour == Checker2.icolour:
                self.__items_black.append(item.field_name)
        return self.__items_white, self.__items_black

    def __update(self):
        print(" ")
        self.__cells_sprite.draw(self.__screen)
        self.__items_sprite.draw(self.__screen)
        pg.display.update()

    def __pick_cell(self, cells):
        print("Очередь хода у", self.__next_turn)
        if self.__picked_checker is None:
            for item in self.__items_sprite:
                if item.field_name == cells.field_name:
                    self.__picked_checker = item
                    self.__field_checker = item.field_name
                    self.__checker_colour = item.icolour
                    break
        else:
            if cells.colour == 0:
                self.__field_cell = cells.field_name
                self.__jump_forward = []
                self.__jump_backward = []
                #если ход белых 
                if self.__next_turn == 'white' and self.__checker_colour == Checker1.icolour:
                    self.__CHECK_HITTING = self.__check_hitting()
                    # для дамки 
                    if self.__field_checker in self.__queens_white:
                        variants = self.__move_queens(self.__field_checker)
                        self.__qCHECK_HITTING = self.__qcheck_hitting()
                        if self.__wqCHECK is True:
                            if cells.field_name in self.__hiting_move_wqueens(self.__qCHECK_HITTING) and \
                                    self.__picked_checker.field_name == self.__field_checker and \
                                    cells.field_name not in self.__items_white:
                                self.__wchecker_step(cells)
                            else:
                                self.__picked_checker = None
                        elif self.__field_cell in variants and self.__wCHECK is False:
                            self.__wchecker_step(cells)
                        elif self.__wCHECK is False:
                            self.__qcheck_hitting()
                        else:
                            self.__picked_checker = None
                    if self.__wCHECK is True and self.__wqCHECK is False:
                        if len(self.__active_Wcheckers) >= 2:
                            self.__CHECK_HITTING = self.__field_checker
                        if cells.field_name in self.__hiting_move_wcheckers(self.__CHECK_HITTING) and\
                                self.__picked_checker.field_name == self.__field_checker and\
                                cells.field_name not in self.__items_white:
                            self.__wchecker_step(cells)
                        else:
                            self.__picked_checker = None
                    elif cells.field_name in self.__move_wcheckers(self.__field_checker) and \
                            cells.field_name not in self.__items_white and self.N == 0:
                        print("Делaem обычный ход")
                        self.__wchecker_step(cells)
                    else:
                        self.__picked_checker = None
                #если ход чёрных 
                elif self.__next_turn == 'black' and self.__checker_colour == Checker2.icolour:
                    self.__CHECK_HITTING = self.__check_hitting()
                    if self.__field_checker in self.__queens_white:
                        variants = self.__move_queens(self.__field_checker)
                        self.__qCHECK_HITTING = self.__qcheck_hitting()
                        if self.__bqCHECK is True:
                            if cells.field_name in self.__hiting_move_bqueens(self.__qCHECK_HITTING) and \
                                    self.__picked_checker.field_name == self.__field_checker and \
                                    cells.field_name not in self.__items_black:
                                self.__bchecker_step(cells)
                            else:
                                self.__picked_checker = None
                        elif self.__field_cell in variants and self.__bCHECK is False:
                            self.__bchecker_step(cells)
                        elif self.__bCHECK is False:
                            self.__qcheck_hitting()
                        else:
                            self.__picked_checker = None
                    if self.__bCHECK is True:
                        if len(self.__active_Bcheckers) >= 2:
                            self.__CHECK_HITTING = self.__field_checker
                        if cells.field_name in self.__hiting_move_bcheckers(self.__CHECK_HITTING) and \
                                self.__picked_checker.field_name == self.__field_checker and \
                                cells.field_name not in self.__items_black:
                            self.__bchecker_step(cells)
                        else:
                            self.__picked_checker = None
                    elif cells.field_name in self.__move_bcheckers(self.__field_checker) and\
                            cells.field_name not in self.__items_black and self.N == 0:
                        print("Делaem обычный ход")
                        self.__bchecker_step(cells)
                    else:
                        self.__picked_checker = None
                else:
                    self.__picked_checker = None

    #победа чёрных                
    def __black_win(self):
        win = pg.display.set_mode((200, 70))
        win.fill((167, 200, 250))
        text_surface = font.render('Чёрные выиграли!', True, (75, 0, 130))
        win.blit(text_surface, (45, 30))
        self.__screen.blit(win, (200, 200))
        
    #победа белых
    def __white_win(self):
        win = pg.display.set_mode((200, 70))
        win.fill((237, 186, 245))
        text_surface = font.render('Белые выиграли!', True, (75, 0, 130))
        win.blit(text_surface, (45, 30))
        self.__screen.blit(win, (200, 200))

    #ход белых    
    def __wchecker_step(self, cells):
        print("Ход на поле", cells.field_name)
        self.__picked_checker.rect = cells.rect
        self.__items_white.remove(self.__picked_checker.field_name)
        self.__picked_checker.field_name = cells.field_name
        self.__items_white.append(cells.field_name)
        if self.__picked_checker.field_name in WHITE_QUEEN_FIELD and\
                self.__field_checker not in self.__queens_white:
            self.__transform_to_queen(self.__picked_checker.field_name)
        elif self.__field_checker in self.__queens_white:
            self.__queens_white.remove(self.__field_checker)
            self.__queens_white.append(cells.field_name)
        if not self.__items_black:
            self.__black_win()
        if self.__wCHECK is True:
            if cells.colour == 0 and self.__checker_colour == Checker1.icolour:
                self.__check_hitting()
                if self.__wCHECK is True:
                    self.__picked_checker = None
                    self.N = 1
                else:
                    self.N = 0
                    self.__picked_checker = None
                    self.__next_turn = 'black'
        else:
            self.N = 0
            self.__picked_checker = None
            self.__next_turn = 'black'
        print("Ход сделан!")

    #ход чёрных    
    def __bchecker_step(self, cells):
        print("Ход на поле", cells.field_name)
        self.__picked_checker.rect = cells.rect
        self.__items_black.remove(self.__picked_checker.field_name)
        self.__picked_checker.field_name = cells.field_name
        self.__items_black.append(cells.field_name)
        if self.__picked_checker.field_name in BLACK_QUEEN_FIELD and\
                self.__field_checker not in self.__queens_black:
            self.__transform_to_queen(self.__picked_checker.field_name)
        if not self.__items_white:
            self.__white_win()
        if self.__bCHECK is True:
            if cells.colour == 0 and self.__checker_colour == Checker2.icolour:
                self.__check_hitting()
                if self.__bCHECK is True:
                    self.__picked_checker = None
                    self.N = 1
                else:
                    self.N = 0
                    self.__picked_checker = None
                    self.__next_turn = 'white'
        else:
            self.N = 0
            self.__picked_checker = None
            self.__next_turn = 'white'
        print("Ход сделан!")

    #если обычный ход белой шашки     
    def __move_wcheckers(self, field_name):
        directions = DIRECTIONS[field_name[0]]
        moves = list(map(lambda el: el + str(int(field_name[1]) + 1), directions))
        return moves

    #если обычный ход дамки   
    def __move_queens(self, field_name):
        self.__diagonal_1 = []
        self.__diagonal_2 = []
        self.__diagonal_3 = []
        self.__diagonal_4 = []
        variants = []
        self.__all = []
        q = QUEEN_DIRECTIONS[field_name[0]]
        n = 0
        while n < len(q):
            for i in range(1, len(q) + 1):
                try:
                    self.__q_moves1 = list(map(lambda el: el + str(int(field_name[1]) + i), q[n]))
                    self.__q_moves2 = list(map(lambda el: el + str(int(field_name[1]) - i), q[n]))
                    if self.__q_moves1[0] in FIELD:
                        self.__all.append(self.__q_moves1[0])
                        self.__diagonal_1.append(self.__q_moves1[0])
                        if self.__q_moves1[0] not in self.__items_white and\
                                self.__q_moves1[0] not in self.__items_black:
                            variants.append(self.__q_moves1[0])
                    if self.__q_moves2[0] in FIELD:
                        self.__all.append(self.__q_moves2[0])
                        self.__diagonal_2.append(self.__q_moves2[0])
                        if self.__q_moves2[0] not in self.__items_white and\
                                self.__q_moves2[0] not in self.__items_black:
                            variants.append(self.__q_moves2[0])
                    if self.__q_moves1[1] in FIELD:
                        self.__all.append(self.__q_moves1[1])
                        self.__diagonal_3.append(self.__q_moves1[1])
                        if self.__q_moves1[1] not in self.__items_white and\
                                self.__q_moves1[1] not in self.__items_black:
                            variants.append(self.__q_moves1[1])
                    if self.__q_moves2[1] in FIELD:
                        self.__all.append(self.__q_moves2[1])
                        self.__diagonal_4.append(self.__q_moves2[1])
                        if self.__q_moves2[1] not in self.__items_white and\
                                self.__q_moves2[1] not in self.__items_black:
                            variants.append(self.__q_moves2[1])
                except Exception:
                    pass
                n += 1
        return variants

    #если ход белых = взятие  
    def __hiting_move_wcheckers(self, field_name):
        if self.__field_checker not in self.__active_Wcheckers:
            return field_name
        step_backward = list(map(lambda el: el + str(int(field_name[1]) - 1), DIRECTIONS[field_name[0]]))
        step_forward = self.__move_wcheckers(field_name)
        result = step_forward + step_backward
        for i in result:
            if i in self.__items_black:
                try:
                    if i[0] in HIT_DIRECTIONS[field_name[0]].keys():
                        self.__jump_forward = HIT_DIRECTIONS[field_name[0]][i[0]] + str(int(field_name[1]) + 2)
                        self.__jump_backward = HIT_DIRECTIONS[field_name[0]][i[0]] + str(int(field_name[1]) - 2)
                    if i in step_forward and self._Wforward_jump == 1 and self.__jump_forward not in self.__items_black:
                        result.clear()
                        result.append(self.__jump_forward)
                        if self.__jump_forward == self.__field_cell:
                            for item in self.__items_sprite:
                                if item.field_name == i:
                                    self.__items_sprite.remove(item)
                                    self.__items_black.remove(item.field_name)
                                    return result
                        else:
                            return result
                    elif i in step_backward and self._Wback_jump == 1 and self.__jump_backward not in self.__items_black:
                        step_backward.append(self.__jump_backward)
                        if self.__jump_backward == self.__field_cell:
                            for item in self.__items_sprite:
                                if item.field_name == i:
                                    self.__items_sprite.remove(item)
                                    self.__items_black.remove(item.field_name)
                                    return step_backward
                        else:
                            return step_backward
                    else:
                        continue
                except Exception:
                    break

    #если ход белой дамки = взятие               
    def __hiting_move_wqueens(self, field_name):
        if self.__field_checker not in self.__active_Wqueens:
            return field_name
        step = self.__move_queens(field_name)
        not_hit = []
        for i in self.__diagonal:
            if i != self.Q:
                not_hit.append(i)
            else:
                hit = list(set(self.__diagonal) - set(not_hit))
                step.clear()
                step.append(hit)
                if self.__field_cell in hit and self.__field_cell != self.Q and\
                        self.__field_cell not in self.__items_white:
                    for item in self.__items_sprite:
                        if item.field_name == i:
                            self.__items_sprite.remove(item)
                            self.__items_black.remove(item.field_name)
                            return hit
                else:
                    return step

    #если ход чёрной дамки = взятие            
    def __hiting_move_bqueens(self, field_name):
        if self.__field_checker not in self.__active_Bqueens:
            return field_name
        step = self.__move_queens(field_name)
        not_hit = []
        for i in self.__diagonal:
            if i != self.Q:
                not_hit.append(i)
            else:
                hit = list(set(self.__diagonal) - set(not_hit))
                step.clear()
                step.append(hit)
                if self.__field_cell in step and self.__field_cell != self.Q and\
                        self.__field_cell not in self.__items_black:
                    for item in self.__items_sprite:
                        if item.field_name == i:
                            self.__items_sprite.remove(item)
                            self.__items_white.remove(item.field_name)
                            return step
                else:
                    return step

    #если обычный ход чёрной шашки             
    def __move_bcheckers(self, field_name):
        directions = DIRECTIONS[field_name[0]]
        moves = list(map(lambda el: el + str(int(field_name[1]) - 1), directions))
        return moves

    #если ход чёрных = взятие
    def __hiting_move_bcheckers(self, field_name):
        if self.__field_checker not in self.__active_Bcheckers:
            return field_name
        step_backward = list(map(lambda el: el + str(int(field_name[1]) + 1), DIRECTIONS[field_name[0]]))
        step_forward = self.__move_bcheckers(field_name)
        result = step_forward + step_backward
        for i in result:
            if i in self.__items_white:
                try:
                    if i[0] in HIT_DIRECTIONS[field_name[0]].keys():
                        self.__jump_forward = HIT_DIRECTIONS[field_name[0]][i[0]] + str(int(field_name[1]) - 2)
                        self.__jump_backward = HIT_DIRECTIONS[field_name[0]][i[0]] + str(int(field_name[1]) + 2)
                    if i in step_forward and self.__jump_forward not in self.__items_white and self._Bforward_jump = 1:
                        result.clear()
                        result.append(self.__jump_forward)
                        if self.__jump_forward == self.__field_cell:
                            for item in self.__items_sprite:
                                if item.field_name == i:
                                    self.__items_sprite.remove(item)
                                    self.__items_white.remove(item.field_name)
                                    return result
                        else:
                            return result
                    if i in step_backward and self.__jump_backward not in self.__items_white and self._Bback_jump = 1:
                        step_backward.clear()
                        step_backward.append(self.__jump_backward)
                        if self.__jump_backward == self.__field_cell:
                            for item in self.__items_sprite:
                                if item.field_name == i:
                                    self.__items_sprite.remove(item)
                                    self.__items_white.remove(item.field_name)
                                    return step_backward
                        else:
                            return step_backward
                    else:
                        continue
                except Exception:
                    break

    def __create_a_queen(self, item_symbol: str):
        field_name = self.__picked_checker.field_name
        item_tuple = self.__item_types[item_symbol]
        classname = globals()[item_tuple[0]]
        return classname(self.__size, item_tuple[0], field_name)

    #превращение в дамку 
    def __transform_to_queen(self, field_name):
        for item in self.__items_sprite:
            if item.field_name == field_name:
                self.__items_sprite.remove(item)
                for k in types.keys():
                    if k == 'Q' and item.field_name in self.__items_white:
                        queen = self.__create_a_queen(k)
                        self.__items_sprite.add(queen)
                        queen.rect = item.rect
                        self.__queens_white.append(queen.field_name)
                        self.__items_white.append(queen.field_name)
                        self.__items_white.remove(item.field_name)
                    elif k == 'q' and item.field_name in self.__items_black:
                        queen = self.__create_a_queen(k)
                        self.__items_sprite.add(queen)
                        queen.rect = item.rect
                        self.__queens_black.append(queen.field_name)
                        self.__items_black.append(queen.field_name)
                        self.__items_black.remove(item.field_name)

    #проверка на возможное взятие                     
    def __check_hitting(self):
        if self.__next_turn == 'white':
            self.__active_Wcheckers = []
            self._Wforward_jump = 0
            self._Wback_jump = 0
            for field in self.__items_white:
                forward = self.__move_wcheckers(field)
                back = list(map(lambda el: el + str(int(field[1]) - 1), DIRECTIONS[field[0]]))
                near = forward + back
                for any_checker in near:
                    try:
                        if any_checker[0] in HIT_DIRECTIONS[field[0]].keys():
                            self.__jump_forward = HIT_DIRECTIONS[field[0]][any_checker[0]] + str(int(field[1]) + 2)
                            self.__jump_backward = HIT_DIRECTIONS[field[0]][any_checker[0]] + str(int(field[1]) - 2)
                            if any_checker in self.__items_black:
                                if any_checker in forward and self.__jump_forward not in self.__items_black and\
                                        self.__jump_forward not in self.__items_white and\
                                        self.__jump_forward in FIELD:
                                    self.__active_Wcheckers.append(field)
                                    self.__field = field
                                    self._Wforward_jump = 1
                                if any_checker in back and self.__jump_backward not in self.__items_black and\
                                        self.__jump_backward not in self.__items_white and\
                                        self.__jump_backward in FIELD:
                                    self.__active_Wcheckers.append(field)
                                    self.__field = field
                                    self._Wback_jump = 1
                    except Exception:
                        break
            if len(self.__active_Wcheckers) == 1:
                self.__wCHECK = True
                return self.__field
            elif len(self.__active_Wcheckers) >= 2:
                self.__wCHECK = True
                return self.__active_Wcheckers
            else:
                self.__wCHECK = False
        elif self.__next_turn == 'black':
            self.__active_Bcheckers = []
            for field in self.__items_black:
                forward = self.__move_bcheckers(field)
                back = list(map(lambda el: el + str(int(field[1]) + 1), DIRECTIONS[field[0]]))
                near = forward + back
                for any_checker in near:
                    try:
                        if any_checker[0] in HIT_DIRECTIONS[field[0]].keys():
                            self.__jump_forward = HIT_DIRECTIONS[field[0]][any_checker[0]] + str(int(field[1]) - 2)
                            self.__jump_backward = HIT_DIRECTIONS[field[0]][any_checker[0]] + str(int(field[1]) + 2)
                            if any_checker in self.__items_white:
                                if any_checker in forward and self.__jump_forward not in self.__items_black and \
                                        self.__jump_forward not in self.__items_white and \
                                        self.__jump_forward in FIELD:
                                    self.__active_Bcheckers.append(field)
                                    self.__field = field
                                    self._Bforward_jump = 1
                                if any_checker in back and self.__jump_backward not in self.__items_black and \
                                        self.__jump_backward not in self.__items_white and \
                                        self.__jump_backward in FIELD:
                                    self.__active_Bcheckers.append(field)
                                    self.__field = field
                                    self._Bback_jump = 1
                    except Exception:
                        break
            if len(self.__active_Bcheckers) == 1:
                self.__bCHECK = True
                return self.__field
            elif len(self.__active_Bcheckers) >= 2:
                self.__bCHECK = True
                return self.__active_Bcheckers
            else:
                self.__bCHECK = False

    #проверка на возможное взятие у дамки             
    def __qcheck_hitting(self):
        if self.__next_turn == 'white':
            self.__active_Wqueens = []
            self.__diagonal = []
            for field in self.__queens_white:
                for any_item in self.__all:
                    if any_item in self.__items_black:
                        try:
                            forward = self.__move_bcheckers(any_item)
                            back = list(map(lambda el: el + str(int(any_item[1]) + 1), DIRECTIONS[any_item[0]]))
                            if any_item in self.__diagonal_1:
                                if back[0] not in self.__items_black:
                                    self.__diagonal = self.__diagonal_1
                                    self.Q = any_item
                                    self.__active_Wqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_2:
                                if back[1] not in self.__items_black:
                                    self.__diagonal = self.__diagonal_2
                                    self.Q = any_item
                                    self.__active_Wqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_3:
                                if forward[0] not in self.__items_black:
                                    self.__diagonal = self.__diagonal_3
                                    self.Q = any_item
                                    self.__active_Wqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_4:
                                if forward[1] not in self.__items_black:
                                    self.__diagonal = self.__diagonal_4
                                    self.Q = any_item
                                    self.__active_Wqueens.append(field)
                                    self.__field = field
                        except Exception:
                            print(" ")
            if len(self.__active_Wqueens) >= 1:
                for j in self.__diagonal:
                    for k in self.__items_white:
                        if j == k:
                            self.__wqCHECK = False
                        else:
                            self.__wqCHECK = True
                            return self.__field
            else:
                self.__wqCHECK = False
        elif self.__next_turn == 'black':
            self.__active_Bqueens = []
            self.__diagonal = []
            for field in self.__queens_black:
                for any_item in self.__all:
                    if any_item in self.__items_white:
                        try:
                            forward = self.__move_wcheckers(any_item)
                            back = list(map(lambda el: el + str(int(any_item[1]) - 1), DIRECTIONS[any_item[0]]))
                            if any_item in self.__diagonal_1:
                                if back[0] not in self.__items_white:
                                    self.__diagonal = self.__diagonal_1
                                    self.Q = any_item
                                    self.__active_Bqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_2:
                                if back[1] not in self.__items_white:
                                    self.__diagonal = self.__diagonal_2
                                    self.Q = any_item
                                    self.__active_Bqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_3:
                                if forward[0] not in self.__items_white:
                                    self.__diagonal = self.__diagonal_3
                                    self.Q = any_item
                                    self.__active_Bqueens.append(field)
                                    self.__field = field
                            elif any_item in self.__diagonal_4:
                                if forward[1] not in self.__items_white:
                                    self.__diagonal = self.__diagonal_4
                                    self.Q = any_item
                                    self.__active_Bqueens.append(field)
                                    self.__field = field
                        except Exception:
                            print(" ")
            if len(self.__active_Bqueens) >= 1:
                for j in self.__diagonal:
                    for k in self.__items_black:
                        if j == k:
                            self.__bqCHECK = False
                        else:
                            self.__bqCHECK = True
                            return self.__field
            else:
                self.__bqCHECK = False


class Cells(pg.sprite.Sprite):
    def __init__(self, colour_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.colour = colour_index
        self.field_name = name
        self.image = pg.image.load(COLOURS[colour_index])
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = pg.Rect(x * size, y * size, size, size)
