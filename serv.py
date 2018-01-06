import operator
from random import choices, randint
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer
import namesgenerator
from player import Player
from world import World
from common import *

class GameServer(rpyc.Service):
    """

    Attributes:
        _world      A two dimension grid of int where : - 0 represents nothing (absence of all)
                                                        - 1 represents a player
                                                        - 2 represents a sweet
                    Example of a 4*4 world : [[0, 2, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 1, 0],
                                              [0, 0, 0, 0]]

        _players   A one dimension array of dictionaries

                Example of the array at one moment :
                [ ... ]

    """

    """
    _world = [[choices([0, 2], [0.7, 0.3])[0] for _ in range(10)] for _ in range(10)]
    _players = []
    _names_pick = []
    """

    """
    def __init__(self, conn):
        super().__init__(conn)
        dim = 10
        world = World(dimensions=(dim, dim))
        self.names_pick = []
        self.players = []
        self.world = world
    """


    dim = 10
    world = World(dimensions=(dim, dim))
    names_pick = []
    players = []
    world = world

    def on_connect(self):
        print('someone connected')
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                x,y = player.get_pos()
                self.world.set_pos(x, y, 1)
                for i, player in enumerate(self.players):
                    player.world.set_world(self.world)

    def on_disconnect(self):
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                player_name = player.get_name()
                x, y = player.get_pos()
                print('player left:', player_name, x, y)
                self.world.get_world()[x][y] = 0
                print(self.players)
                del self.players[i]
                print(self.players)
                for playerToNotify in self.players:
                    print('here')
                    playerToNotify.get_conn().root.notify_player_left(player_name)

    def exposed_get_best_player(self):
        score_tab = {}
        for player in self.players:
            score_tab[player.get_name()] = player.get_score()
        for (player, score) in score_tab.items():
            if score == max(score_tab.values()):
                return player

    #def exposed_init_world(self):
     #   self.world = World(dimensions=(self.dim, self.dim))
        #for i, player in enumerate(self.players):
        #    del self.players[i]

    def exposed_start_game(self, name):
        x, y = self.world.get_available_spawnable_pos()
        # self.world.set_pos(x, y, 1)  # TODO : A voir si on en a besoin
        if name in self.names_pick:
            name += ' :)'
        player = Player(x, y, name, self._conn, self.world)
        self.players.append(player)
        print('new player joined the game: ' + name)
        for player in self.players:
            player.get_conn().root.notify_new_player(name)
        return x, y, name, self.world.get_world()

    def exposed_is_end(self):
        for i, row in enumerate(self.world.get_world()):
            for j, box in enumerate(row):
                if box == 2: return False
        self.world.generate_new_world()
        for player in self.players:
            player.set_score(0)
        return True

    def exposed_get_score_tab(self):
        score_text = ""
        score_tab = {}
        for player in self.players:
            score_tab[player.get_name()] = player.get_score()
        score_tab = sorted(score_tab.items(), key=operator.itemgetter(1))
        score_tab.reverse()
        for case in score_tab:
            player, score = case
            score_text += "| " + player + " : " + str(score) + " \n"
        return score_text

    def exposed_get_players(self):
        return self.players

    def exposed_get_world(self):
        return self.world.get_world()

    def exposed_get_world_dim(self):
        return self.dim

    def exposed_start(self):
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                self.world.set_pos(player.case_x, player.case_y, 1)

    def exposed_get_score(self):
        print("test")
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                print("score" + str(player.get_score()))
                return player.get_score()

    def exposed_get_pos(self):
        x, y = self.world.get_available_spawnable_pos()
        # self.world.set_pos(x, y, 1)  # TODO : A voir si on en a besoin
        return x, y


    def exposed_move(self, direction):
        is_allowed = False
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                dim_x, dim_y = self.world.get_dimensions()
                player_name = player.get_name()
                print(player_name, 'wants to move to the', direction)
                # TODO : gerer bombons et score ici
                # TODO 2 : quand quelqun bouge il faut reset le world du server
                if direction == 'right' and player.case_x < (dim_x - 1) and self.world.get_world()[player.case_x + 1][player.case_y] != 1:
                    if self.world.get_world()[player.case_x + 1][player.case_y] == 2:
                        print(player.get_name() + " +1 " + str(player.get_score()))
                        player.set_score(player.get_score() + 1)
                    self.world.set_pos(player.case_x + 1, player.case_y, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_x += 1
                    is_allowed = True
                if direction == 'left' and player.case_x > 0 and self.world.get_world()[player.case_x - 1][player.case_y] != 1:
                    if self.world.get_world()[player.case_x - 1][player.case_y] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                    self.world.set_pos(player.case_x - 1, player.case_y, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_x -= 1
                    is_allowed = True
                if direction == 'top' and player.case_y > 0 and self.world.get_world()[player.case_x][player.case_y - 1] != 1:
                    if self.world.get_world()[player.case_x][player.case_y - 1] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                    self.world.set_pos(player.case_x, player.case_y - 1, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_y -= 1
                    is_allowed = True
                if direction == 'bot' and player.case_y < (dim_y - 1) and self.world.get_world()[player.case_x][player.case_y + 1] != 1:
                    if self.world.get_world()[player.case_x][player.case_y + 1] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                    self.world.set_pos(player.case_x, player.case_y + 1, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_y += 1
                    is_allowed = True
                return is_allowed

    '''
    def find_correct_place_to_spawn(self):
        dim_x, dim_y = len(self._world[0]), len(self._world)
        rand_x, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        while self._world[rand_x][rand_y] != 0:
            rand_x, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        return rand_x, rand_y
        '''


if __name__ == '__main__':
    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    server = ThreadedServer(GameServer, port=12345)
    server.start()
