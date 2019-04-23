from gym_unity.envs import UnityEnv
from tf_agents.environments.gym_wrapper import GymWrapper
from tf_agents.environments import tf_py_environment

from tf_agents.policies import random_tf_policy
from tf_agents.agents.ppo import ppo_agent
from tf_agents.networks import actor_distribution_network
from tf_agents.networks import value_network

from tf_agents.drivers import dynamic_episode_driver
from tf_agents.drivers import dynamic_step_driver
from tf_agents.replay_buffers import tf_uniform_replay_buffer

#from tf_agents.trajectories import time_step as ts
from tf_agents.trajectories import time_step as ts

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
          fc_layer_params=(128,128,))
    value_net = value_network.ValueNetwork(
          env.observation_spec(), fc_layer_params=(128,128,)) # Unity's num_layers and hidden_units

    #optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=3.0e-4)

    tf_agent = ppo_agent.PPOAgent(
        env.time_step_spec(),
        env.action_spec(),
        optimizer,
        actor_net=actor_net,
        value_net=value_net,
        importance_ratio_clipping = 0.2, # Unity's epsilon
        use_gae = True,
        lambda_value=0.99,
        discount_factor=0.995, # AKA gamma
        entropy_regularization = 0.001, # Unity's beta
        normalize_observations = True,
        num_epochs=3)
    tf_agent.initialize()

    eval_policy = tf_agent.policy
    collect_policy = tf_agent.collect_policy

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        tf_agent.collect_data_spec,
        batch_size=1,
        max_length=1_000) # batch_size*max_length = Unity's buffer_size

    """
    collect_driver = dynamic_episode_driver.DynamicEpisodeDriver(
        env,
        collect_policy,
        observers=[replay_buffer.add_batch],
        num_episodes=50)
    """
    collect_steps = 1_000 # must correspond to replay_buffer size
    collect_driver = dynamic_step_driver.DynamicStepDriver(
        env,
        collect_policy,
        observers=[replay_buffer.add_batch],
        num_steps=collect_steps)

    global_steps = 0
    while global_steps < 1_000_000:
        global_steps += collect_steps

        collect_driver.run()

        trajectories = replay_buffer.gather_all()
        total_loss, _ = tf_agent.train(experience=trajectories)
        replay_buffer.clear()
        print('Total loss at {} is {}'.format(str(global_steps), str(total_loss)))

ppo()