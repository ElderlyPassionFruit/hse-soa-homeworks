# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import pkg.mafia_proto.mafia_pb2 as mafia__pb2


class MafiaServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Subscribe = channel.unary_stream(
            '/MafiaServer/Subscribe',
            request_serializer=mafia__pb2.SubscribeRequest.SerializeToString,
            response_deserializer=mafia__pb2.SubscribeResponse.FromString,
        )
        self.DoVote = channel.unary_unary(
            '/MafiaServer/DoVote',
            request_serializer=mafia__pb2.Vote.SerializeToString,
            response_deserializer=mafia__pb2.Nothing.FromString,
        )
        self.DoFinishDay = channel.unary_unary(
            '/MafiaServer/DoFinishDay',
            request_serializer=mafia__pb2.FinishDay.SerializeToString,
            response_deserializer=mafia__pb2.FinishDayResponse.FromString,
        )
        self.DoWaitNextDay = channel.unary_unary(
            '/MafiaServer/DoWaitNextDay',
            request_serializer=mafia__pb2.WaitNextDay.SerializeToString,
            response_deserializer=mafia__pb2.WaitNextDayResponse.FromString,
        )
        self.DoMafiaVote = channel.unary_unary(
            '/MafiaServer/DoMafiaVote',
            request_serializer=mafia__pb2.Vote.SerializeToString,
            response_deserializer=mafia__pb2.Nothing.FromString,
        )
        self.DoCopCheck = channel.unary_unary(
            '/MafiaServer/DoCopCheck',
            request_serializer=mafia__pb2.Check.SerializeToString,
            response_deserializer=mafia__pb2.CheckResponse.FromString,
        )


class MafiaServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Subscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoFinishDay(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoWaitNextDay(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoMafiaVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoCopCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MafiaServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Subscribe': grpc.unary_stream_rpc_method_handler(
            servicer.Subscribe,
            request_deserializer=mafia__pb2.SubscribeRequest.FromString,
            response_serializer=mafia__pb2.SubscribeResponse.SerializeToString,
        ),
        'DoVote': grpc.unary_unary_rpc_method_handler(
            servicer.DoVote,
            request_deserializer=mafia__pb2.Vote.FromString,
            response_serializer=mafia__pb2.Nothing.SerializeToString,
        ),
        'DoFinishDay': grpc.unary_unary_rpc_method_handler(
            servicer.DoFinishDay,
            request_deserializer=mafia__pb2.FinishDay.FromString,
            response_serializer=mafia__pb2.FinishDayResponse.SerializeToString,
        ),
        'DoWaitNextDay': grpc.unary_unary_rpc_method_handler(
            servicer.DoWaitNextDay,
            request_deserializer=mafia__pb2.WaitNextDay.FromString,
            response_serializer=mafia__pb2.WaitNextDayResponse.SerializeToString,
        ),
        'DoMafiaVote': grpc.unary_unary_rpc_method_handler(
            servicer.DoMafiaVote,
            request_deserializer=mafia__pb2.Vote.FromString,
            response_serializer=mafia__pb2.Nothing.SerializeToString,
        ),
        'DoCopCheck': grpc.unary_unary_rpc_method_handler(
            servicer.DoCopCheck,
            request_deserializer=mafia__pb2.Check.FromString,
            response_serializer=mafia__pb2.CheckResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'MafiaServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class MafiaServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Subscribe(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_stream(request, target, '/MafiaServer/Subscribe',
                                              mafia__pb2.SubscribeRequest.SerializeToString,
                                              mafia__pb2.SubscribeResponse.FromString,
                                              options, channel_credentials,
                                              insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoVote(request,
               target,
               options=(),
               channel_credentials=None,
               call_credentials=None,
               insecure=False,
               compression=None,
               wait_for_ready=None,
               timeout=None,
               metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MafiaServer/DoVote',
                                             mafia__pb2.Vote.SerializeToString,
                                             mafia__pb2.Nothing.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoFinishDay(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MafiaServer/DoFinishDay',
                                             mafia__pb2.FinishDay.SerializeToString,
                                             mafia__pb2.FinishDayResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoWaitNextDay(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MafiaServer/DoWaitNextDay',
                                             mafia__pb2.WaitNextDay.SerializeToString,
                                             mafia__pb2.WaitNextDayResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoMafiaVote(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MafiaServer/DoMafiaVote',
                                             mafia__pb2.Vote.SerializeToString,
                                             mafia__pb2.Nothing.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoCopCheck(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MafiaServer/DoCopCheck',
                                             mafia__pb2.Check.SerializeToString,
                                             mafia__pb2.CheckResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
