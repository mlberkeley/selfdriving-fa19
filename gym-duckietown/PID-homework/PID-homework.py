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

#Initialize environment and draw a lane curve as a trajectory to follow
env = DuckietownEnv(
    seed = 1,
    map_name = 'loop_empty',
    draw_curve = True,
    domain_rand = False,
)

#Preliminary rendering of environment
env.reset()
env.render()

'''
This is the PID class to fill out. Figure out what constants you want to save and what past information you would like to save
for the integral and derivative terms.
'''

class PID:
    def __init__(self, proportional = 0, integral = 0, derivative = 0):
        '''
        Initialize the constants and any other variables you need
        '''

    def update(self, error):
        delT = 0.03333333333
        delE = #Need to keep track of change in error
        '''
        We have given two values here to start with: the change in T as calculated by framerate (which is update rate) and the other,
        which has not yet been defined, which is the change in error from last time.
        '''
        return output


def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing. It is where you will have your control
    logic. Thus you should only have to edit the PID class and this update function.

    You do not need to worry about the dt input to this function. If you look below,
    pyglet is scheduled to call update once for each frame (at the same rate as the environment
    frame rate). In the PID function, this is why we define delT as such as the frame rate is 30 fps.

    e_p is the cross track error as measured by the environment. It will be positive on one side of the track
    (right) and negative on the other side (left). This is the error signal passed to the PID

    We have included all the logic needed to create the running environment except a steering command.
    You could put in a random steering command and start the environment if you want to see.

    However, this steer value should come from a PID controller you define outside of the update function
    (so it is not reinitialized and you lose prior useful values). We have given you a starting velocity of
    .1 which is very slow. Try to tweak the three parameters of your PID so that you can complete one loop
    of the environment at a speed greater than or equal to .3

    """
    lane_pose = env.get_lane_pos2(env.cur_pos, env.cur_angle)
    e_p = lane_pose.dist


    steer = '''???'''
    action = np.array([.1, steer])

    obs, reward, done, info = env.step(action)

    if done:
        print('done!')
        env.reset()
        car.reset()
        env.render()
    env.render()
    
print(env.unwrapped.frame_rate)
pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

# Enter main event loop
pyglet.app.run()
env.close()