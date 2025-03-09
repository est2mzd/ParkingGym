import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

# 🚗 自車の位置（原点）
car_x, car_y = 0, 0

# 📏 LIDAR の最大測定距離
lidar_max_range = 20  # 20m 先まで測定

# 🎯 LIDAR 光線（x 軸方向にのみ飛ばす）
lidar_beam = LineString([(car_x, car_y), (car_x + lidar_max_range, car_y)])

# 🛑 壁（x=10 の位置に配置）
wall = LineString([(15, -10), (15, 10)])

# 📡 LIDAR の測定距離を求める
min_dist = lidar_max_range  # 初期値は最大距離
if lidar_beam.intersects(wall):  # 交差判定
    intersection = lidar_beam.intersection(wall)  # 交点を取得
    if intersection.geom_type == "Point":  # 交差点が1つの場合
        min_dist = intersection.distance(Point(car_x, car_y))  # ✅ Point に変換
    elif intersection.geom_type == "MultiPoint":  # 交差点が複数の場合
        min_dist = min(pt.distance(Point(car_x, car_y)) for pt in intersection.geoms)

# 📢 測定結果
print(f"LIDAR 測定距離: {min_dist:.2f} m")

# 📊 可視化
plt.figure(figsize=(6, 6))
plt.axis("equal")

# 🚗 自車の描画
plt.scatter(car_x, car_y, color='blue', s=100, label="Car")

# 🛑 壁の描画
x, y = wall.xy
plt.plot(x, y, color='black', linewidth=3, label="Wall")

# 📡 LIDAR 光線の描画
lidar_end_x = car_x + min_dist  # 壁との交差点まで
lidar_end_y = car_y
plt.plot([car_x, lidar_end_x], [car_y, lidar_end_y], linestyle="dashed", color="red", alpha=0.7, label="Lidar Beam")

plt.grid(True)
plt.legend()
plt.title("LIDAR Simulation with a Single Wall")
plt.show()
