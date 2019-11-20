#!/usr/bin/env python
"""
"""
import sys
import argparse
import pyglet
import numpy as np
import gym
sys.path.append('../')
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
from gym_duckietown.wrappers import UndistortWrapper
sys.path.append('../../Car Interface Weeks 2-3')
import controller

env = DuckietownEnv(
    seed = 1,
    map_name = 'loop_empty',
    draw_curve = True,
    domain_rand = False,
)

env.reset()
env.render()

class PID:
    def __init__(self, proportional = 0, integral = 0, derivative = 0):
        self.pWeight = proportional
        self.iWeight = integral
        self.dWeight = derivative
        self.clear()
        self.prev_error = 0.0

    def clear(self):
        self.pTerm = 0.0
        self.iTerm = 0.0
        self.dTerm = 0.0
        self.last_error = 0.0
        self.output = 0.0

    def update(self, error):
        delT = 0.03333333333
        delE = error - self.prev_error
        self.pTerm = error
        self.iTerm += error * delT
        self.dTerm = delE / delT
        self.prev_error = error
        output = self.pWeight * self.pTerm + self.iWeight * self.iTerm + self.dWeight * self.dTerm
        return output

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    lane_pose = env.get_lane_pos2(env.cur_pos, env.cur_angle)

    e_p = lane_pose.dist

    steer = steering_controller.update(e_p)
    action = np.array([.3, steer])
    print(e_p)

    obs, reward, done, info = env.step(action)

    if done:
        print('done!')
        env.reset()
        car.reset()
        env.render()
    env.render()

steering_controller = PID(5, 3, 20)
    
print(env.unwrapped.frame_rate)
pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

# Enter main event loop
pyglet.app.run()
env.close()