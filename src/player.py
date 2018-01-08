import pygame
from common.common import *


class Player:
    """

    """
    def __init__(self, x, y, name, conn, world_ref):
        self.name = name
        self.score = 0
        self.conn = conn
        self.pict = pict_player
        self.case_x = x
        self.case_y = y
        self.world = world_ref

    '''
    Renvoie la position du joueur sur la grille
    '''
    def get_pos(self):
        return self.case_x, self.case_y

    '''
    Renvoie le score du joueur
    '''
    def get_score(self):
        return self.score

    '''
    Modifie le score du joueur
    '''
    def set_score(self, score):
        self.score = score

    '''
    Renvoie le nom du joueur
    '''
    def get_name(self):
        return self.name

    '''
    Renvoie la connection avec le joueur
    '''
    def get_conn(self):
        return self.conn

    '''
    Permet de print un joueur
    '''
    def __repr__(self):
        return "Player : " + self.name + ", Coords : (" + str(self.case_x) + "," + str(self.case_y) + "), Score : " \
               + str(self.score)