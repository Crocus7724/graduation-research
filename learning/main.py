import argparse
import os.path
import pickle
import time

import keras.backend.tensorflow_backend as KTF
import tensorflow as tf

from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

from SimulatorClient import SimulatorClient
from RoboEnv import RoboEnv

model_save_path = 'data/model/model.json'
weight_save_path = 'data/weight/weight.hdf5'

parser = argparse.ArgumentParser()
parser.add_argument("--address", type=str, required=True)
args = parser.parse_args()

client = SimulatorClient(args.address)


def run():
    env = RoboEnv(client)
    nb_actions = env.action_space.n

    for i in range(50):
        print('simulation start: %d' % i)
        old_session = KTF.get_session()

        with tf.Graph().as_default():
            session = tf.Session('')
            KTF.set_session(session)
            KTF.set_learning_phase(1)

            if not os.path.isfile(model_save_path):
                model = Sequential()
                model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
                model.add(Dense(16))
                model.add(Activation('relu'))
                model.add(Dense(16))
                model.add(Activation('relu'))
                model.add(Dense(16))
                model.add(Activation('relu'))
                model.add(Dense(nb_actions))
                model.add(Activation('linear'))
            else:
                with open(model_save_path, 'r') as f:
                    model = model_from_json(f.read())

            if os.path.isfile(weight_save_path):
                model.load_weights(weight_save_path)
            print(model.summary())

            # experience replay用のmemory
            memory = SequentialMemory(limit=50000, window_length=1)
            # 行動方策はオーソドックスなepsilon-greedy。ほかに、各行動のQ値によって確率を決定するBoltzmannQPolicyが利用可能
            policy = EpsGreedyQPolicy(eps=0.1)
            dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
                           target_model_update=1e-2, policy=policy)
            dqn.compile(Adam(lr=1e-3), metrics=['mae'])

            tb = TensorBoard(log_dir='data/tensorboard', histogram_freq=0, write_graph=True)

            history = dqn.fit(env, nb_steps=50000, visualize=False, callbacks=[tb], verbose=2, nb_max_episode_steps=5000)

        json_string = model.to_json()
        with open(model_save_path, 'w') as f:
            f.write(json_string)
        model.save_weights(weight_save_path)

        with open('data/history/history%s.pickle' % time.strftime('%Y%m%d-%H%M%S'), 'wb') as f:
            pickle.dump(history.history, f)

        KTF.set_session(old_session)


if __name__ == '__main__':
    run()
