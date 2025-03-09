import sys
import os
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt
from ReedsSheppPath import reeds_shepp_path_planning as rs

from HybridAStar.car import move, check_car_collision, MAX_STEER, WB, plot_car, BUBBLE_R
from Maps import sample_map
import yaml

# 設定ファイルの読み込み
config_file_path = "./configs/base_settings.yaml"
#
with open(config_file_path, "r", encoding="utf-8") as file:
    config = (yaml.safe_load(file))["hybrid_a_star"]

XY_GRID_RESOLUTION  = float(config["xy_grid_resolution_m"])  # [m]
YAW_GRID_RESOLUTION = np.deg2rad(float(config["yaw_grid_resolution_deg"]))  

# フルパス
#current_file_path = os.path.abspath(__file__)
#current_dir_path  = os.path.dirname(current_file_path)
#parent_dir_path   = os.path.dirname(current_dir_path)

# ../PythonRobotics をパスに追加
# sys.path.append(os.path.abspath(parent_dir_path))

# 確認
pprint(sys.path)

from HybridAStar import hybrid_a_star_ver2 as m

show_animation = True
# m.show_animation = False
#m.main()

print("Start Hybrid A* planning")

ox, oy = [], []
ox, oy = sample_map.create_map(ox, oy)

# Set Initial parameters
start = [10.0, 10.0, np.deg2rad(90.0)]
goal  = [45.0, 55.0, np.deg2rad(-90.0)]

print("start : ", start)
print("goal : ", goal)


path = m.hybrid_a_star_planning(start, goal, ox, oy, XY_GRID_RESOLUTION, YAW_GRID_RESOLUTION)

x   = path.x_list
y   = path.y_list
yaw = path.yaw_list

plt.plot(ox, oy, ".k")
rs.plot_arrow(start[0], start[1], start[2], fc='g')
plt.plot(start[0], start[1], 'bo')

rs.plot_arrow(goal[0], goal[1], goal[2])
plt.plot(goal[0], goal[1], 'go')

plt.plot(x, y, "-r", label="Hybrid A* path")
plt.grid(True)
plt.axis("equal")
plt.savefig("test1.png")

if show_animation:
    for i_x, i_y, i_yaw in zip(x, y, yaw):
        plt.cla()
        plt.plot(ox, oy, ".k")
        plt.plot(x, y, "-r", label="Hybrid A* path")
        plt.grid(True)
        plt.axis("equal")
        plot_car(i_x, i_y, i_yaw)
        plt.pause(0.0001)

print(__file__ + " done!!")