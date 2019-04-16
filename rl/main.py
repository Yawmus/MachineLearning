from gym_unity.envs import UnityEnv
from tf_agents.environments.gym_wrapper import GymWrapper
from tf_agents.environments import tf_py_environment

from tf_agents.policies import random_tf_policy
from tf_agents.agents.ppo import ppo_agent
from tf_agents.networks import actor_distribution_network
from tf_agents.networks import value_network

from tf_agents.drivers import dynamic_episode_driver
from tf_agents.replay_buffers import tf_uniform_replay_buffer

#from tf_agents.trajectories import time_step as ts
from tf_agents.environments import time_step as ts

import tensorflow as tf

env = tf_py_environment.TFPyEnvironment(GymWrapper(UnityEnv(environment_filename=None, worker_id=0, use_visual=False, multiagent=False)))

def random_policy():
    random_policy = random_tf_policy.RandomTFPolicy(env.time_step_spec(),
                                                    env.action_spec())

    """
    #time_step = ts.restart(tf.ones(env.time_step_spec().observation.shape))
    time_step = env.reset()
    while True:
        time_step = env.step(random_policy.action(time_step).action)
    """


    driver = dynamic_episode_driver.DynamicEpisodeDriver(env, random_policy, [], num_episodes=20)
    initial_time_step = env.reset()
    final_time_step, _ = driver.run(initial_time_step)

def ppo():
    actor_net = actor_distribution_network.ActorDistributionNetwork(
          env.observation_spec(),
          env.action_spec(),
          fc_layer_params=(10,10,))
    value_net = value_network.ValueNetwork(
          env.observation_spec(), fc_layer_params=(10,10,))

    #optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-4)

    tf_agent = ppo_agent.PPOAgent(
        env.time_step_spec(),
        env.action_spec(),
        optimizer,
        actor_net=actor_net,
        value_net=value_net,
        num_epochs=10)
    tf_agent.initialize()

    eval_policy = tf_agent.policy
    collect_policy = tf_agent.collect_policy

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        tf_agent.collect_data_spec,
        batch_size=1,
        max_length=10_000)

    collect_driver = dynamic_episode_driver.DynamicEpisodeDriver(
        env,
        collect_policy,
        observers=[replay_buffer.add_batch],
        num_episodes=50)

    global_steps = 0
    while global_steps < 1_000_000:
        global_steps += 1

        collect_driver.run()

        trajectories = replay_buffer.gather_all()
        total_loss, _ = tf_agent.train(experience=trajectories)
        replay_buffer.clear()

ppo()