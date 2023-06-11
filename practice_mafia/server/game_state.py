from enum import Enum
from random import shuffle, random, seed
from multiprocessing import Condition
import logging
from time import time
logging.basicConfig(level=logging.INFO)


class Role(Enum):
    Mafia = 0
    Civilian = 1
    Cop = 2


class Game:
    def __init__(self, id, game_size):
        self.game_id = id
        self.game_size = game_size
        self.players = []
        self.roles = {}
        self.alive = []
        self.day = 0
        self.killed_login = "_"
        self.vote = [None] * game_size
        self.cond_vote = Condition()

        self.finished = 0
        self.cond_finished = Condition()

        self.waited = 0
        self.cond_waited = Condition()

    def IsStarded(self):
        return len(self.players) == self.game_size

    def GetPlayers(self):
        return self.players

    def AddPlayer(self, login):
        logging.info(
            f"Game {self.game_id}, day {self.day}, added player {login}")
        self.players.append(login)
        return self.IsStarded()

    def InitRoles(self):
        cnt_mafias = 1
        cnt_cops = 1
        cnt_civilians = self.game_size - cnt_mafias
        seed(time())
        shuffled_players = self.players.copy()
        shuffle(shuffled_players)
        mafias = shuffled_players[:cnt_mafias]
        shuffled_players = shuffled_players[cnt_mafias:]
        cops = shuffled_players[:cnt_cops]
        shuffled_players = shuffled_players[cnt_cops:]
        civilians = shuffled_players[:cnt_civilians]
        for mafia in mafias:
            self.roles[mafia] = Role.Mafia
        for cop in cops:
            self.roles[cop] = Role.Cop
        for civilian in civilians:
            self.roles[civilian] = Role.Civilian
        assert (len(self.roles) == self.game_size)
        logging.info(f"Game {self.game_id}, init roles {self.roles}")
        self.alive = [True] * len(self.players)

    def GetRole(self, login):
        assert (login in self.players)
        if len(self.roles) == 0:
            self.InitRoles()
        assert (login in self.roles)
        return self.roles[login]

    def IsVoteFinished(self):
        with self.cond_vote:
            for i in range(self.game_size):
                if self.alive[i] and self.vote[i] is None:
                    return False
        return True

    def Vote(self, login_from, login_to):
        logging.info(
            f"Game {self.game_id}, day {self.day}, vote {login_from} -> {login_to}")
        assert (login_from in self.GetAlivePlayers())
        assert (login_to in self.GetAlivePlayers())

        with self.cond_vote:
            self.vote[self.players.index(login_from)] = login_to
            if self.IsVoteFinished():
                cnt = {}
                for login in self.vote:
                    if not login in self.players:
                        continue
                    if not login in cnt:
                        cnt[login] = 0
                    cnt[login] += 1
                max_login = "_"
                for login in cnt:
                    if max_login == "_" or cnt[max_login] < cnt[login]:
                        max_login = login
                self.killed_login = max_login
                if max_login in self.players:
                    self.alive[self.players.index(max_login)] = False
                self.cond_vote.notify_all()

            while self.killed_login == None:
                logging.info(
                    f"Game {self.game_id}, {login_from} is wating for finishing voting stage")
                self.cond_vote.wait()

    def FinishDay(self, login):
        logging.info(
            f"Game {self.game_id}, day {self.day}, finish day {login}")

        with self.cond_finished:
            self.finished += 1
            if self.finished % self.game_size == 0:
                self.night_killed = "_"
                self.cond_finished.notify_all()

            while self.finished % self.game_size != 0:
                logging.info(
                    f"Game {self.game_id}, {login} is wating for finishing finish day stage")
                self.cond_finished.wait()
            return self.killed_login

    def WaitNextDay(self, login):
        logging.info(
            f"Game {self.game_id}, day {self.day}, wait next day {login}")

        with self.cond_waited:

            self.waited += 1
            if self.waited % self.game_size == 0:
                self.killed_login = None
                self.vote = [None] * self.game_size
                self.cond_waited.notify_all()
                self.day += 1

            while self.waited % self.game_size != 0:
                logging.info(
                    f"Game {self.game_id}, {login} is wating for wait next_day finish day stage")
                self.cond_waited.wait()

    def GetCurDay(self):
        return self.day

    def GetAlivePlayers(self):
        alive_players = []
        for (id, player) in enumerate(self.players):
            if self.alive[id]:
                alive_players.append(player)
        return alive_players

    def MafiaVote(self, login_from, login_to):
        logging.info(
            f"Game {self.game_id}, day {self.day}, mafia kill {login_from} -> {login_to}")
        assert (login_from in self.GetAlivePlayers())
        assert (login_to in self.GetAlivePlayers())
        self.night_killed = login_to
        self.alive[self.players.index(login_to)] = False

    def GetNightKilled(self):
        return self.night_killed

    def GetWinner(self):
        cnt_alive = len(self.GetAlivePlayers())
        cnt_alive_mafia = 0
        for player in self.GetAlivePlayers():
            if self.roles[player] == Role.Mafia:
                cnt_alive_mafia += 1
        if cnt_alive_mafia == 0:
            return 2
        if cnt_alive <= cnt_alive_mafia * 2:
            return 1
        return 0
