import operator
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer
from src.player import Player
from src.world import World


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

    dim = 10
    world = World(dimensions=(dim, dim))
    names_pick = []
    players = []
    score_tab = {}


    def on_connect(self):
        print('someone connected')
        print(self.score_tab)

    '''
     Supprime le joueur de la grille
     Supprime le joueur de self.players
     Supprime le joueur du tableau des scores
     Notifie les joueurs que quelqu'un s'est déconnecté
    '''
    def on_disconnect(self):
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                player_name = player.get_name()
                x, y = player.get_pos()
                print('player left:', player_name, x, y)
                self.world.get_world()[x][y] = 0
                print(self.players)
                del self.players[i]
                if player.get_name() in self.score_tab.keys():
                    del self.score_tab[player.get_name()]
                print(self.players)
                for playerToNotify in self.players:
                    playerToNotify.get_conn().root.notify_player_left(player_name)

    '''
    Renvoie le nom du meilleur joueur
    '''
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

    '''
    Valide le nom du joueur
    Donne sa position
    Ajoute le joueur à self.players
    Notifie les joueurs que quelqu'un s'est connecté
    '''
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
    '''
    Renvoie vrai si la partie est terminé
    '''
    def is_end(self):
        for i, row in enumerate(self.world.get_world()):
            for j, box in enumerate(row):
                if box == 2: return False
        return True

    '''
    Génère un nouveau monde
    '''
    def generate_new_world(self):
        self.world.generate_new_world()

    '''
    Reset le tableau des scores 
    Met à 0 le score de tous les joueurs
    '''
    def reset_score(self):
        self.score_tab = {}
        print("reset" + str(self.score_tab))
        for player in self.players:
            player.set_score(0)

    '''
    Tri le tableau des scores et le renvoie en string
    '''
    def exposed_get_score_tab(self):
        score = {}
        for player in self.players:
            score[player.get_name()] = player.get_score()
        score_text = ""
        score_tab = sorted(score.items(), key=operator.itemgetter(1))
        score_tab.reverse()
        for case in score_tab:
            player, score = case
            score_text += "| " + player + " : " + str(score) + " \n"
        return score_text

    def exposed_get_players(self):
        return self.players

    '''
    Renvoie la grille
    '''
    def exposed_get_world(self):
        return self.world.get_world()

    '''
    Renvoie la dimension de la grille
    '''
    def exposed_get_world_dim(self):
        return self.dim

    '''
    Dans la boucle
    Rentre la position du joueur sur la grille
    Ajoute le joueur au tableau des scores
    '''
    def exposed_start(self):
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                self.world.set_pos(player.case_x, player.case_y, 1)
                self.score_tab[player.get_name()] = player.get_score()

    '''
    Si il ne va pas sortir de la grille et qu'il n'y a pas de joueur ou il va :
        On augmente son score s'il trouve un bonbon
        On met à jour le tableau des scores
        On modifie sa position dans la grille 
    Renvoie si le joueur peut bouger
    '''
    def exposed_move(self, direction):
        game_started = True
        is_allowed = False
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                dim_x, dim_y = self.world.get_dimensions()
                player_name = player.get_name()
                print(player_name, 'wants to move to the', direction)
                if direction == 'right' and player.case_x < (dim_x - 1) and self.world.get_world()[player.case_x + 1][player.case_y] != 1:
                    if self.world.get_world()[player.case_x + 1][player.case_y] == 2:
                        print(player.get_name() + " +1 " + str(player.get_score()))
                        player.set_score(player.get_score() + 1)
                        self.score_tab[player.get_name()] = player.get_score()
                    self.world.set_pos(player.case_x + 1, player.case_y, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_x += 1
                    is_allowed = True
                if direction == 'left' and player.case_x > 0 and self.world.get_world()[player.case_x - 1][player.case_y] != 1:
                    if self.world.get_world()[player.case_x - 1][player.case_y] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                        self.score_tab[player.get_name()] = player.get_score()
                    self.world.set_pos(player.case_x - 1, player.case_y, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_x -= 1
                    is_allowed = True
                if direction == 'top' and player.case_y > 0 and self.world.get_world()[player.case_x][player.case_y - 1] != 1:
                    if self.world.get_world()[player.case_x][player.case_y - 1] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                        self.score_tab[player.get_name()] = player.get_score()
                    self.world.set_pos(player.case_x, player.case_y - 1, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_y -= 1
                    is_allowed = True
                if direction == 'bot' and player.case_y < (dim_y - 1) and self.world.get_world()[player.case_x][player.case_y + 1] != 1:
                    if self.world.get_world()[player.case_x][player.case_y + 1] == 2:
                        print(player.get_name() + "+1")
                        player.set_score(player.get_score() + 1)
                        self.score_tab[player.get_name()] = player.get_score()
                    self.world.set_pos(player.case_x, player.case_y + 1, 1)
                    self.world.set_pos(player.case_x, player.case_y, 0)
                    player.case_y += 1
                    is_allowed = True
                print(self.score_tab)
                if self.is_end():
                    game_started = True
                    self.generate_new_world()
                    self.reset_score()
                return game_started, is_allowed


if __name__ == '__main__':
    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    server = ThreadedServer(GameServer, port=12345)
    server.start()
