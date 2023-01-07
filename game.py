import pygame as pg
from appearance import *
from main import *


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.playboard = Playboard(screen)
        self.turn = 'black square.jpg'
        self.valid_moves = {}

    def __reset(self):
        self._init()

    def select(self, row=4, line=4):
        if self.selected:
            result = self._move(row, line)
            if not result:
                self.selected = None
                self.select(row, line)
        checker = self.playboard.__draw_items(row, line)
        if checker!=0 and checker.colour == self.turn:
            self.selected = checker
            self.valid_moves = self.playboard.get_valid_moves(checker)
            return True

        return False

    def _move(self, row, line):
        checker = self.playboard.get_checker(row, line)
        if self.selected and checker == 0 and (row, line) in self.valid_moves:

