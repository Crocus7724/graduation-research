import gym
import gym.spaces
import numpy as np
from SimulatorClient import *


class RoboEnv(gym.core.Env):
    def __init__(self, client: SimulatorClient):
        self.client = client

        self.action_space = gym.spaces.Discrete(40)

        high = np.array([6, 1.2, 6])
        low = np.array([-6, 0.4, -6])
        self.observation_space = gym.spaces.Box(low=low, high=high)

    def _step(self, action):
        angle = create_angle_from_action(action)
        position = self.client.send(angle)
        failed_out_of_bounds = position.x < -5 or position.y > 5 or position.y < -5
        failed_fell = position.z < 0.4
        success = position.x > 5

        dt = position.x * 0.1
        if failed_out_of_bounds:
            reward = -1.0 + dt
        elif failed_fell:
            reward = -5.0 + dt
        elif success:
            reward = 5.0
        else:
            reward = dt

        done = failed_out_of_bounds or failed_fell or success

        return np.array([position.x, position.y, position.z]), reward, done, {}

    def _reset(self):
        self.client.end()
        self.client.start()
        return np.array([0, 1.0, 0])


def create_angle_from_action(action: int) -> Angle:
    kind = create_kind_from_action(action)
    roll, pitch, yaw = create_angle_value_from_action(action)
    return Angle(kind, roll, pitch, yaw)


def create_kind_from_action(action: int) -> JointKind:
    if action < 6:
        return JointKind.RIGHT_SHOULDER
    elif action < 8:
        return JointKind.RIGHT_ELBOW
    elif action < 14:
        return JointKind.RIGHT_HIP
    elif action < 16:
        return JointKind.RIGHT_KNEE
    elif action < 20:
        return JointKind.RIGHT_FOOT
    elif action < 26:
        return JointKind.LEFT_SHOULDER
    elif action < 28:
        return JointKind.LEFT_ELBOW
    elif action < 34:
        return JointKind.LEFT_HIP
    elif action < 36:
        return JointKind.LEFT_KNEE
    elif action < 40:
        return JointKind.LEFT_FOOT


def create_angle_value_from_action(action: int) -> (float, float, float):
    roll, pitch, yaw, = -1, -1, -1

    if action in {0, 8, 16, 20, 28, 36}:
        roll = 5
    elif action in {1, 9, 17, 21, 29, 37}:
        roll = -5
    elif action in {2, 6, 10, 14, 18, 22, 26, 30, 34, 38}:
        pitch = -5
    elif action in {3, 7, 11, 15, 19, 23, 27, 31, 35, 39}:
        pitch = 5
    elif action in {4, 12, 24, 32}:
        yaw = -5
    elif action in {5, 13, 25, 33}:
        yaw = 5

    return roll, pitch, yaw


def get_value_from_action(action: int) -> float:
    return 5 if action % 2 == 0 else -5
