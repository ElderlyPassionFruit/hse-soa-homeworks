import grpc
from concurrent import futures
from os import getenv
import pkg.mafia_proto.mafia_pb2 as pb2
import pkg.mafia_proto.mafia_pb2_grpc as pb2_grpc
from multiprocessing import Condition
from server.game_state import Game
import logging


class MafiaServerServicer(pb2_grpc.MafiaServerServicer):

    def __init__(self, game_size):
        self.game_size = game_size
        self.games = [Game(0, self.game_size)]
        self.cond = Condition()

    def Subscribe(self, request, context):
        with self.cond:
            logging.info(
                f"Subscribe: {request}, game_id: {len(self.games) - 1}")
            login = request.login
            game_id = len(self.games) - 1
            response = pb2.SubscribeResponse()
            response.ack.game_id = game_id
            yield response

            players = self.games[game_id].GetPlayers()
            for player in players:
                response = pb2.SubscribeResponse()
                response.new_player.login = player
                yield response

            if self.games[game_id].AddPlayer(login):
                self.games.append(Game(game_id + 1, self.game_size))
            players = self.games[game_id].GetPlayers()
            returned_players = len(players)

            self.cond.notify_all()

            while returned_players < len(players) or not self.games[game_id].IsStarded():
                while returned_players < len(players):
                    player = players[returned_players]
                    response = pb2.SubscribeResponse()
                    response.new_player.login = player
                    returned_players += 1
                    yield response
                if not self.games[game_id].IsStarded():
                    self.cond.wait()
                players = self.games[game_id].GetPlayers()

            assert (self.games[game_id].IsStarded())

            role = self.games[game_id].GetRole(login)
            response = pb2.SubscribeResponse()
            response.start.role = str(role)
            response.start.players.extend(players)
            yield response

    def DoVote(self, request, context):
        self.games[request.game_id].Vote(
            request.login_from, request.login_to)
        response = pb2.Nothing()
        return response

    def DoFinishDay(self, request, context):
        vote_result = self.games[request.game_id].FinishDay(request.login)
        winner = self.games[request.game_id].GetWinner()
        response = pb2.FinishDayResponse(
            killed_login=vote_result, winner=winner)
        return response

    def DoWaitNextDay(self, request, context):
        self.games[request.game_id].WaitNextDay(request.login)
        day = self.games[request.game_id].GetCurDay()
        alive_players = self.games[request.game_id].GetAlivePlayers()
        killed_login = self.games[request.game_id].GetNightKilled()
        winner = self.games[request.game_id].GetWinner()
        response = pb2.WaitNextDayResponse(
            day=day, alive_players=alive_players, killed_login=killed_login, winner=winner)
        return response

    def DoMafiaVote(self, request, context):
        self.games[request.game_id].MafiaVote(
            request.login_from, request.login_to)
        return pb2.Nothing()

    def DoCopCheck(self, request, context):
        role = self.games[request.game_id].GetRole(request.login)
        response = pb2.CheckResponse()
        response.role = str(role)
        return response


def main():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=64))
    pb2_grpc.add_MafiaServerServicer_to_server(
        MafiaServerServicer(int(getenv("GAME_SIZE"))), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print('Server started on port 50051')
    server.wait_for_termination()
