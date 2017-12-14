import grpc

import simulator_pb2 as s
import simulator_pb2_grpc as sg


class JointKind:
    RIGHT_SHOULDER = "right shoulder"
    RIGHT_ELBOW = "right elbow"
    RIGHT_HIP = "right hip"
    RIGHT_KNEE = "right knee"
    RIGHT_FOOT = "right foot"
    LEFT_SHOULDER = "left shoulder"
    LEFT_ELBOW = "left elbow"
    LEFT_HIP = "left hip"
    LEFT_KNEE = "left knee"
    LEFT_FOOT = "left foot"


class PartKind:
    HEAD = "head"


class Angle:
    def __init__(self, kind: JointKind, roll: float, pitch: float, yaw: float):
        self.kind = kind
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw


class Position:
    def __init__(self, kind: PartKind, x: float, y: float, z: float):
        self.kind = kind
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "position: %s, %s, %s, %s" % (self.kind, self.x, self.y, self.z)

class SimulatorClient:
    def __init__(self, address: str):
        channel = grpc.insecure_channel(address)
        self.stub = sg.SimulatorStub(channel)

    def start(self):
        self.stub.Start(s.VoidValue())

    def send(self, angle: Angle) -> Position:
        p = self.stub.Send(_create_grpc_angle(angle))
        position = _create_position(p)
        return position

    def end(self):
        self.stub.End(s.VoidValue())


def _create_grpc_angle(angle: Angle) -> s.Angle:
    a = s.Angle()
    a.kind = _create_grpc_joint_kind(angle.kind)
    a.roll = angle.roll
    a.pitch = angle.pitch
    a.yaw = angle.yaw
    return a


def _create_grpc_joint_kind(kind: JointKind) -> s.JointKind:
    if kind == JointKind.RIGHT_SHOULDER:
        return s.RIGHT_SHOULDER
    elif kind == JointKind.RIGHT_ELBOW:
        return s.RIGHT_ELBOW
    elif kind == JointKind.RIGHT_HIP:
        return s.RIGHT_HIP
    elif kind == JointKind.RIGHT_KNEE:
        return s.RIGHT_KNEE
    elif kind == JointKind.RIGHT_FOOT:
        return s.RIGHT_FOOT
    elif kind == JointKind.LEFT_SHOULDER:
        return s.LEFT_SHOULDER
    elif kind == JointKind.LEFT_ELBOW:
        return s.LEFT_ELBOW
    elif kind == JointKind.LEFT_HIP:
        return s.LEFT_HIP
    elif kind == JointKind.LEFT_KNEE:
        return s.LEFT_KNEE
    elif kind == JointKind.LEFT_FOOT:
        return s.LEFT_FOOT
    else:
        print("kind value is invalid(%s)" % kind)


def _create_grpc_part_kind(kind: PartKind) -> s.PartsKind:
    if kind == PartKind.HEAD:
        return s.HEAD
    else:
        return s.HEAD


def _create_position(p: s.Position) -> Position:
    return Position(_create_parts_kind(p.kind), p.x, p.y, p.z)


def _create_parts_kind(k: s.PartsKind) -> PartKind:
    if k == s.HEAD:
        return PartKind.HEAD
    else:
        return PartKind.HEAD
