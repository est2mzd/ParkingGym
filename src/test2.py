import sys
import os
import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt
from ReedsSheppPath import reeds_shepp_path_planning as rs

from HybridAStar.car import move, check_car_collision, MAX_STEER, WB, plot_car, BUBBLE_R
from Maps import sample_map
import yaml
import pandas as pd

# 設定ファイルの読み込み
config_file_path = "./Configs/base_settings.yaml"
#
with open(config_file_path, "r", encoding="utf-8") as file:
    config = (yaml.safe_load(file))["hybrid_a_star"]

XY_GRID_RESOLUTION  = float(config["xy_grid_resolution_m"])  # [m]
YAW_GRID_RESOLUTION = np.deg2rad(float(config["yaw_grid_resolution_deg"]))  

from HybridAStar import hybrid_a_star_ver2 as m

ox, oy = [], []
ox, oy = sample_map.create_map(ox, oy)

# Set Initial parameters
start = [10.0, 10.0, np.deg2rad(90.0)]
goal  = [45.0, 55.0, np.deg2rad(-90.0)]

print("start : ", start)
print("goal : ", goal)


path = m.hybrid_a_star_planning(start, goal, ox, oy, XY_GRID_RESOLUTION, YAW_GRID_RESOLUTION)

path.name    = "test1"
path.path_id = 1

# PathオブジェクトをDataFrameに変換
df1 = pd.DataFrame([{
    "name": path.name,
    "id": path.path_id,
    "x_list": path.x_list,
    "y_list": path.y_list,
    "yaw_list": path.yaw_list,
    "direction_list": path.direction_list,
    "cost": path.cost
}])

df2 = df1.copy()
df2.id = 2

df = pd.concat([df1, df2])

file_path_parquet = (str(__file__)).replace(".py", ".parquet")

df.to_parquet(file_path_parquet, engine="pyarrow", index=False, compression="snappy")


print(__file__ + " done!!")