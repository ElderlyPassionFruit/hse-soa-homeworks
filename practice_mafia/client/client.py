import grpc
import pkg.mafia_proto.mafia_pb2 as pb2
import pkg.mafia_proto.mafia_pb2_grpc as pb2_grpc
from server.game_state import Role
from enum import Enum
from random import randint
from os import getenv
from time import sleep


class DayCommandType(Enum):
    Vote = 0
    Finish = 1


class NightCommandType(Enum):
    DoAction = 0


class Client:
    def __init__(self, is_bot=False):
        self.is_bot = is_bot
        if is_bot:
            self.channel = grpc.insecure_channel('server:50051')
        else:
            self.channel = grpc.insecure_channel('0.0.0.0:50051')
        self.stub = pb2_grpc.MafiaServerStub(self.channel)

    def ReadLogin(self):
        if self.is_bot:
            self.login = "bot" + str(randint(10**9, 2 * 10**9))
            print(self.login)
        else:
            print("Введите login, он должен состоять только из латинских букв.")
            while True:
                login = input()
                if len(login) == 0:
                    print("login должен быть не пустой, введите заново.")
                    continue

                def IsLatinString(s: str) -> bool:
                    return s.isalpha() and all(ord(c) < 128 for c in s)
                if not IsLatinString(login):
                    print(
                        "login должен состоять только из латинских букв, введите заново.")
                    continue
                self.login = login
                return

    def StartGame(self):
        action = pb2.SubscribeRequest(login=self.login)
        response_stream = self.stub.Subscribe(action)

        for response in response_stream:
            if response.HasField('ack'):
                self.game_id = response.ack.game_id
                print(f"game_id = {self.game_id}")
            elif response.HasField('new_player'):
                new_player_login = response.new_player.login
                print(f"new_player_login = {new_player_login}")
            elif response.HasField('start'):
                self.role = eval(response.start.role)
                self.alive_players = response.start.players
                print(f"Ваша роль в этой игре: {self.role}")
            else:
                raise ValueError("Unknown type")

    def ReadDayCommand(self):
        if self.is_bot:
            while True:
                if randint(1, 2) == 1:
                    if self.can_vote:
                        id = randint(0, len(self.alive_players) - 1)
                        print(f"vote {id}")
                        return [DayCommandType.Vote, self.alive_players[id]]
                else:
                    if not self.can_vote:
                        print("finish")
                        return [DayCommandType.Finish]
        else:
            while True:
                data = input().split()
                if len(data) == 1:
                    if data[0] != "finish":
                        print("Некорректный воод, попробуйте ещё раз")
                        continue
                    return [DayCommandType.Finish]
                elif len(data) == 2:
                    if not self.can_vote:
                        print("Некорректный воод, попробуйте ещё раз")
                        continue
                    if data[0] != "vote" or not data[1].isnumeric() or int(data[1]) < 0 or int(data[1]) >= len(self.alive_players):
                        print("Некорректный воод, попробуйте ещё раз")
                        continue
                    return [DayCommandType.Vote, self.alive_players[int(data[1])]]
                else:
                    print("Некорректный воод, попробуйте ещё раз")
                    continue

    def ProcessKilledLogin(self, login, winner):

        if login != '_':
            print(
                f"Убили {login}")
            self.alive_players.remove(login)
            print("Обновлённый список живых:")
            for (id, player) in enumerate(self.alive_players):
                print(f"login: {player}, current id: {id}")

            if login == self.login:
                print(
                    "Так как убили вас, на этом для вас игра заканчивается, вы можете наблюдать за происходящим в режиме духа.")
                self.alive = False
            if winner != 0:
                if winner == 1:
                    print("Победила Мафия")
                else:
                    print("Победили Мирные")
                exit(0)
        else:
            print("Никого не убили")

    def ProcessDayCommand(self):
        if not self.alive:
            print("finish day")
            finish_day = pb2.FinishDay(
                game_id=self.game_id, login=self.login)
            response = self.stub.DoFinishDay(finish_day)
            self.ProcessKilledLogin(response.killed_login, response.winner)
            return False
        else:
            print("Вам нужно совершить какое-то действие. Доступный набор команд:")
            if self.can_vote:
                print("vote {#id}, чтобы проголосовать за убийство, где в качестве {#id} требуется указать текущий id игрока, которого вы хотите убить на этом ходу.")
            else:
                print("finish, чтобы закончить этот ход")
            # print("chat, чтобы пообщаться в чате с другими игроками (пока не работает)")
            command = self.ReadDayCommand()
            if command[0] == DayCommandType.Vote:
                self.can_vote = False
                vote = pb2.Vote(game_id=self.game_id,
                                login_from=self.login, login_to=command[1])
                response = self.stub.DoVote(vote)
                return True
            elif command[0] == DayCommandType.Finish:
                finish_day = pb2.FinishDay(
                    game_id=self.game_id, login=self.login)
                response = self.stub.DoFinishDay(finish_day)
                self.ProcessKilledLogin(response.killed_login, response.winner)
                return False

    def ReadNightCommand(self):
        if self.is_bot:
            id = randint(0, len(self.alive_players) - 1)
            print(f"action {id}")
            return [NightCommandType.DoAction, self.alive_players[id]]
        else:
            while True:
                data = input().split()
                if len(data) == 2:
                    if not self.can_do_action:
                        print("Некорректный воод, попробуйте ещё раз")
                        continue
                    if data[0] != "action" or not data[1].isnumeric() or int(data[1]) < 0 or int(data[1]) >= len(self.alive_players):
                        print("Некорректный воод, попробуйте ещё раз")
                        continue
                    return [NightCommandType.DoAction, self.alive_players[int(data[1])]]
                else:
                    print("Некорректный воод, попробуйте ещё раз")
                    continue

    def ProcessMafiaNightCommand(self):
        if not self.alive:
            return
        else:
            print("Введите команду:")
            print(
                "action {#id}, чтобы убить игрока, где в качестве {#id} требуется указать текущий id игрока, которого вы хотите убить на этом ходу.")
            command = self.ReadNightCommand()
            self.can_do_action = False
            vote = pb2.Vote(game_id=self.game_id,
                            login_from=self.login, login_to=command[1])
            response = self.stub.DoMafiaVote(vote)
            return False

    def ProcessCopNightCommand(self):
        if not self.alive:
            return
        else:
            print("Введите команду:")
            print(
                "action {#id}, чтобы узнать роль игрока, где в качестве {#id} требуется указать текущий id игрока, роль которого вы хотите узнать на этом ходу.")
            command = self.ReadNightCommand()
            self.can_do_action = False
            check = pb2.Check(game_id=self.game_id, login=command[1])
            response = self.stub.DoCopCheck(check)
            print(f"Роль игрока с login: {command[1]} - {response.role}")
            return False

    def Play(self):
        day = 0
        self.alive = True
        self.is_finished = False

        while not self.is_finished:
            print(f"Наступил день №{day}")

            # Вывести всех живых игроков
            print("Сейчас живы:")
            for (id, player) in enumerate(self.alive_players):
                print(f"login: {player}, current id: {id}")

            if self.alive:
                if day == 0:
                    self.can_vote = False
                    print(
                        "Это день знакомства, сегодня днём игроки вы не голосуете за убийство одного из игроков.")
                else:
                    self.can_vote = True
                    print("Сегодня вам нужно выбрать игрока, которого вы хотите убить.")

            while self.ProcessDayCommand():
                pass

            match self.role:
                case Role.Civilian:
                    # Ничего не нужно делать, вы мирный житель
                    pass
                case Role.Mafia:
                    self.can_do_action = True
                    while self.ProcessMafiaNightCommand():
                        pass
                case Role.Cop:
                    self.can_do_action = True
                    while self.ProcessCopNightCommand():
                        pass
                case _:
                    raise ValueError("Incorrect role")

            print("Ждём следующий день")
            wait_next_day = pb2.WaitNextDay(
                game_id=self.game_id, login=self.login)
            response = self.stub.DoWaitNextDay(wait_next_day)
            self.ProcessKilledLogin(response.killed_login, response.winner)
            day += 1
            assert (day == response.day)
            self.alive_players = response.alive_players
            print("---------------------------------------\n")


def main():
    is_bot = getenv("IS_BOT")
    if not is_bot is None and int(is_bot) == 1:
        sleep(5)
        client = Client(is_bot=True)
        client.ReadLogin()
        client.StartGame()
        client.Play()
    else:
        client = Client(is_bot=False)
        client.ReadLogin()
        client.StartGame()
        client.Play()
