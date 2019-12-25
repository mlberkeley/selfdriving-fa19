#!/usr/bin/env python


"""
This script transforms duckietown images into costmaps.

A costmap is a greyscale image that specifies which areas of the map are driveable.
The white sections are able to driven on by the duckiebot, and the black sections are not.
Practically, the costmap will be used in A* to weight certain edges.
Edges that correspond to non driveable areas will have a large weight.
Edges that are on the road will have low weight.

test your implementation with the following command:
python duckie_astar_hw7/render_costmap.py --outfile "costmap.png"

Your costmap will be part of your checkoff, so be sure to save it.
"""


import argparse
import cv2
import numpy as np
import gym
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default=None)
    parser.add_argument('--map-name', default='udem1')
    parser.add_argument('--distortion', default=False, action='store_true')
    parser.add_argument('--draw-curve', action='store_true', help='draw the lane following curve')
    parser.add_argument('--draw-bbox', action='store_true', help='draw collision detection bounding boxes')
    parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
    parser.add_argument('--frame-skip', default=1, type=int, help='number of frames to skip')
    parser.add_argument('--seed', default=1, type=int, help='seed')
    parser.add_argument('--outfile', default="costmap.png", type=str)
    parser.add_argument('--radius', default=75, type=int)
    args = parser.parse_args()

    env = DuckietownEnv(
        seed=args.seed,
        map_name=args.map_name,
        draw_curve=args.draw_curve,
        draw_bbox=args.draw_bbox,
        domain_rand=args.domain_rand,
        frame_skip=args.frame_skip,
        distortion=args.distortion,
        do_color_relabeling=True)

    """YOUR CODE HERE"""

    # reset the environment

    # render a top_down_rgb_array image from the environment

    # convert the image to an opencv UMat

    # convert the color space from BGR to HSV

    # apply a color filter to detect everything within the HSV spectrum of [0, 0, 0] to [20, 20, 20]

    # assign the resulting thresholded image to "x"

    """END YOUR CODE HERE"""

    contours, hierarchy = cv2.findContours(x, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    """YOUR CODE HERE"""

    # using OpenCV erode the costmap x by a kernel size of args.radius

    # apply a gaussian blur to smooth the costmap using cv2.BORDER_DEFAULT

    """END YOUR CODE HERE"""

    cv2.imwrite(args.outfile, x)

    lower_left = (999999, 999999)
    upper_right = (0, 0)

    for j in range(env.grid_height):
        for i in range(env.grid_width):
            tile = env._get_tile(i, j)

            kind = tile['kind']

            if (kind == "3way_left" or kind == "3way_right" or kind == "straight"
                    or kind == "curve_right" or kind == "curve_left"):
                lower_left = (min(lower_left[0], i), min(lower_left[1], j))
                upper_right = (max(upper_right[0], i), max(upper_right[1], j))

    lower_left = (env.road_tile_size * lower_left[0], env.road_tile_size * lower_left[1])
    upper_right = (env.road_tile_size * (upper_right[0] + 1), env.road_tile_size * (upper_right[1] + 1))

    lower_left_image = (999999, 999999)
    upper_right_image = (0, 0)

    for x in contours:
        pos_min = x.min(axis=0)[0]
        pos_max = x.max(axis=0)[0]
        lower_left_image = (min(lower_left_image[0], pos_min[0]), min(lower_left_image[1], pos_min[1]))
        upper_right_image = (max(upper_right_image[0], pos_max[0]), max(upper_right_image[1], pos_max[1]))

    # calculate the world to image coordinates scale factor and xy offset

    scale_factor = (lower_left[0] - upper_right[0]) / (
            lower_left_image[0] - upper_right_image[0])

    offset = (lower_left_image[0] - lower_left[0] / scale_factor,
              lower_left_image[1] - lower_left[1] / scale_factor)

    np.save("transform.npy", np.array([scale_factor, offset[0], offset[1]]))
