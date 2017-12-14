# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import simulator_pb2 as simulator__pb2


class SimulatorStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Start = channel.unary_unary(
        '/simulator.Simulator/Start',
        request_serializer=simulator__pb2.VoidValue.SerializeToString,
        response_deserializer=simulator__pb2.VoidValue.FromString,
        )
    self.Send = channel.unary_unary(
        '/simulator.Simulator/Send',
        request_serializer=simulator__pb2.Angle.SerializeToString,
        response_deserializer=simulator__pb2.Position.FromString,
        )
    self.End = channel.unary_unary(
        '/simulator.Simulator/End',
        request_serializer=simulator__pb2.VoidValue.SerializeToString,
        response_deserializer=simulator__pb2.VoidValue.FromString,
        )


class SimulatorServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Start(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Send(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def End(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SimulatorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Start': grpc.unary_unary_rpc_method_handler(
          servicer.Start,
          request_deserializer=simulator__pb2.VoidValue.FromString,
          response_serializer=simulator__pb2.VoidValue.SerializeToString,
      ),
      'Send': grpc.unary_unary_rpc_method_handler(
          servicer.Send,
          request_deserializer=simulator__pb2.Angle.FromString,
          response_serializer=simulator__pb2.Position.SerializeToString,
      ),
      'End': grpc.unary_unary_rpc_method_handler(
          servicer.End,
          request_deserializer=simulator__pb2.VoidValue.FromString,
          response_serializer=simulator__pb2.VoidValue.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'simulator.Simulator', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
