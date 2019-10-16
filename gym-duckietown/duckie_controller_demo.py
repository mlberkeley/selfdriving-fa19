#!/usr/bin/env python
# manual

"""
This script allows you to manually control the simulator or Duckiebot
using the keyboard arrows.
"""

import sys
import argparse
import pyglet
from pyglet.window import key
import numpy as np
import gym
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
from gym_duckietown.wrappers import UndistortWrapper
import threading

sys.path.append('../Car Interface Weeks 2-3')
import controller

class Car():

    def __init__(self):
        self.interface = controller.Car_Interface()

        self.pedal_type = None
        self.amount = 0.0
        self.TIME_UNIT = self.interface.dt


    def start(self):

        threading.Timer(self.TIME_UNIT, self.update_pos).start()

    def update_pos(self):

        if (self.interface.gear is not None):
            self.interface.apply_control(self.pedal_type, self.amount)

        threading.Timer(self.TIME_UNIT, self.update_pos).start()

    def gear(self, g):
        if g == "forward":
            car.interface.set_gear(car.interface.FORWARD)
        elif g == "reverse":
            car.interface.set_gear(car.interface.REVERSE)

    def pedal(self, p):
        if (p == "accelerate"):
            car.pedal_type = car.interface.ACCELERATOR
            car.amount = 1.0
        elif (p == "brake"):
            car.pedal_type = car.interface.BRAKE
            car.amount = 1.0
        elif (p == "release"):
            car.pedal_type = None
            car.amount = 0.0

    def turn(self, t):
        if (t == "left"):
            car.interface.steer_to(1.0)
        elif (t == "right"):
            car.interface.steer_to(-1.0)
        elif (t == "release"):
            car.interface.steer_to(0.0)

    def reset(self):
        self.__init__()

    def duckietown_control(self):

        return [self.interface.velocity, self.interface.steering_angle]

car = Car()
car.start()

# from experiments.utils import save_img

parser = argparse.ArgumentParser()
parser.add_argument('--map-name', default='udem1')
parser.add_argument('--distortion', default=False, action='store_true')
parser.add_argument('--draw-curve', action='store_true', help='draw the lane following curve')
parser.add_argument('--draw-bbox', action='store_true', help='draw collision detection bounding boxes')
parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
parser.add_argument('--frame-skip', default=1, type=int, help='number of frames to skip')
parser.add_argument('--seed', default=1, type=int, help='seed')
args = parser.parse_args()

env = DuckietownEnv(
    seed = args.seed,
    map_name = args.map_name,
    draw_curve = args.draw_curve,
    draw_bbox = args.draw_bbox,
    domain_rand = args.domain_rand,
    frame_skip = args.frame_skip,
    distortion = args.distortion,
)

env.reset()
env.render()

@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """

    if symbol == key.BACKSPACE or symbol == key.SLASH:
        print('RESET')
        env.reset()
        env.render()
    elif symbol == key.PAGEUP:
        env.unwrapped.cam_angle[0] = 0
    elif symbol == key.ESCAPE:
        env.close()
        sys.exit(0)

    # Take a screenshot
    # UNCOMMENT IF NEEDED - Skimage dependency
    # elif symbol == key.RETURN:
    #     print('saving screenshot')
    #     img = env.render('rgb_array')
    #     save_img('screenshot.png', img)

# Register a keyboard handler
key_handler = key.KeyStateHandler()
env.unwrapped.window.push_handlers(key_handler)

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """

    if key_handler[key.F]:
        car.gear("forward")
    elif key_handler[key.R]:
        car.gear("reverse")

    if key_handler[key.UP]:
        car.pedal("accelerate")
    elif key_handler[key.DOWN]:
        car.pedal("brake")
    else:
        car.pedal("release")

    if key_handler[key.LEFT]:
        car.turn("left")
    elif key_handler[key.RIGHT]:
        car.turn("right")
    else:
        car.turn("release")

    action = np.array(car.duckietown_control())

    # Speed boost
    if key_handler[key.LSHIFT]:
        action *= 1.5

    obs, reward, done, info = env.step(action)
    #print('step_count = %s, reward=%.3f' % (env.unwrapped.step_count, reward))

    
    if key_handler[key.RETURN]:
        from PIL import Image
        im = Image.fromarray(obs)

        im.save('screen.png')

    if done:
        print('done!')
        env.reset()
        car.reset()
        env.render()


    env.render()


    

pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

# Enter main event loop
pyglet.app.run()

env.close()
