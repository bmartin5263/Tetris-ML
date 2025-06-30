from typing import Any, SupportsFloat, Union

import gymnasium as gym
import numpy as np
from gymnasium.core import Env

Observation = np.ndarray
Action = Union[int, np.ndarray]

def main():
    # Create our training environment
    env: Env[Observation, Action]
    with gym.make("CartPole-v1", 10, render_mode="human") as env:

        # Reset environment to start a new episode
        observation: Observation
        info: dict[str, Any]
        observation, info = env.reset()

        # observation: what the agent can "see" - cart position, velocity, pole angle, etc.
        #   Example output: [ 0.01234567 -0.00987654  0.02345678  0.01456789]
        #                   [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
        # info: extra debugging information (usually not needed for basic learning)
        print(f"Starting observation: {observation}")
        print(f"With info: {info}")

        episode_over = False
        total_reward = 0
        while not episode_over:
            # Choose an action, sample() will simply return a random action
            action: Action = env.action_space.sample()

            # Take the action and see what happens
            observation: Observation
            info: dict[str, Any]
            reward: SupportsFloat # +1 for each step the pole stays upright
            terminated: bool # True if pole falls too far (agent failed)
            truncated: bool  # True if we hit the time limit (500 steps)
            observation, reward, terminated, truncated, info = env.step(action)

            total_reward += reward
            episode_over = terminated or truncated
            if terminated:
                print("Terminated episode")
            if truncated:
                print("Truncated episode")

        print(f"Episode finished! Total reward: {total_reward}")

if __name__ == "__main__":
    main()