import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

#================================================================#
def create_line(x, y, yaw_deg, length):
    """
    指定した端点 (x, y) から yaw_deg 方向に length の長さを持つ薄い壁（線）を作成

    Parameters:
        x : float  (壁の端点 x 座標)
        y : float  (壁の端点 y 座標)
        yaw_deg : float  (壁の向き [度])
        length : float  (壁の長さ [m])

    Returns:
        LineString : 壁（Shapely LineString）
    """
    # 角度をラジアンに変換
    yaw_rad = np.radians(yaw_deg)

    # もう一方の端点を計算
    end_x = x + length * np.cos(yaw_rad)
    end_y = y + length * np.sin(yaw_rad)

    # 壁を作成
    return LineString([(x, y), (end_x, end_y)])

#==============================================================#
def create_circle(x, y, radius):
    """
    指定した中心 (x, y) と半径 radius で円を作成

    Parameters:
        x : float  (円の中心 x 座標)
        y : float  (円の中心 y 座標)
        radius : float  (円の半径 [m])

    Returns:
        Polygon : 円（Shapely の buffer で作成した円）
    """
    return Point(x, y).buffer(radius)  # Shapely の buffer() を使用して円（Polygon）を作成



#================================================================#
def create_lidar_beam(x, y, yaw_deg, range_m):
    """
    指定した位置 (x, y) から yaw_deg 方向に LIDAR の光線を作成

    Parameters:
        x : float  (LIDARの起点 x 座標)
        y : float  (LIDARの起点 y 座標)
        yaw_deg : float  (LIDARの向き [度])
        range_m : float  (LIDAR の最大測定距離 [m])

    Returns:
        LineString : LIDAR の光線（Shapely LineString）
    """
    # LIDAR の光線を作成
    return create_line(x, y, yaw_deg, range_m)



#==============================================================#
def calc_distance(lidar_beam, obstacle, lidar_x, lidar_y, lidar_range_m):
    """
    LIDAR の光線が障害物と交差する場合、その最短距離を計算する

    Parameters:
        lidar_beam : LineString  (LIDAR の光線)
        obstacle : Shapely Geometry (障害物)
        lidar_x : float  (LIDAR の x 座標)
        lidar_y : float  (LIDAR の y 座標)
        lidar_range_m : float  (LIDAR の最大測定距離)

    Returns:
        float : 交差点までの最短距離（障害物がない場合は lidar_range_m）
    """
    min_dist = lidar_range_m  # 初期値は最大距離
    lidar_position = Point(lidar_x, lidar_y)  # LIDAR の位置を Point に変換

    # LIDAR 光線と障害物が交差するか判定
    if lidar_beam.intersects(obstacle):
        intersection = lidar_beam.intersection(obstacle)  # 交点を取得
        
        # 交差点が1つの場合
        if intersection.geom_type == "Point":
            min_dist = intersection.distance(lidar_position)
        
        # 交差点が複数（MultiPoint）の場合、最も近い点を取得
        elif intersection.geom_type == "MultiPoint":
            min_dist = min(pt.distance(lidar_position) for pt in intersection.geoms)
            
        # Point(x,y).buffer(radius)を使った場合
        elif intersection.geom_type == "LineString":
            coords = list(intersection.coords)
            min_dist = min(pt[0] for pt in coords)


    return min_dist


#==============================================================#
def calc_distance_multi(lidar_beam, obstacles, lidar_x, lidar_y, lidar_range_m):
    """
    LIDAR 光線が複数の障害物と交差する場合、最も近い障害物までの距離を求める

    Parameters:
        lidar_beam : LineString  (LIDAR の光線)
        obstacles : list  (Shapely Geometry のリスト)
        lidar_x : float  (LIDAR の x 座標)
        lidar_y : float  (LIDAR の y 座標)
        lidar_range_m : float  (LIDAR の最大測定距離)

    Returns:
        float : 最も近い障害物までの距離（障害物がない場合は lidar_range_m）
    """
    
    # LIDAR の最大測定距離を初期値として設定
    min_distance = lidar_range_m
    
    # 複数の障害物に対して距離を計算
    for obstacle in obstacles:
        # 各障害物に対して LIDAR ビームとの最短距離を計算
        tmp_distance = calc_distance(lidar_beam, obstacle, lidar_x, lidar_y, lidar_range_m)
        
        # もし現在の障害物までの距離が最短なら更新
        if tmp_distance < min_distance:
            min_distance = tmp_distance

    # 計算した最短距離を返す
    return min_distance


#==============================================================#
def plot_shapely_line(lidar_beam, color="red", linestyle="dashed", label="Lidar Beam"):
    """
    Shapely LineString 形式の LIDAR ビームをプロットする関数

    Parameters:
        lidar_beam : LineString (LIDAR の光線)
        color : str (線の色)
        linestyle : str (線のスタイル)
        label : str (凡例ラベル)
    """
    x, y = lidar_beam.xy  # LIDAR 光線の座標を取得
    plt.plot(x, y, color=color, linestyle=linestyle, alpha=0.7, label=label)

#==============================================================#
def plot_shapely_circle(circle, color="blue", label="Circle"):
    """
    Shapely の円 (Polygon) をプロットする関数

    Parameters:
        circle : Polygon (Shapely の buffer で作成した円)
        color : str (円の色, デフォルトは "blue")
        label : str (凡例用のラベル)
    """
    # 円の外周の x, y 座標を取得
    x, y = circle.exterior.xy  
    plt.fill(x, y, color=color, alpha=0.5, label=label)



#==============================================================#
if __name__ == '__main__':
    # テスト用
    # lidarのbeam
    lidar_x, lidar_y, lidar_yaw_deg = 0,0,0
    lidar_range_m   = 30
    lidar_beam_1    = create_lidar_beam(lidar_x, lidar_y, lidar_yaw_deg, lidar_range_m)
    
    # wall
    x, y, yaw_deg = 20,-10,90
    length        = 20    
    wall_1 = create_line(x, y, yaw_deg, length)
    wall_2 = create_line(16, y, yaw_deg, length)
    
    # circle
    x, y, radius = 15, 0, 2
    circle_1 = Point(x, y).buffer(radius)
    # Polygon([(30, 20), (50, 20), (50, 40), (30, 40)]),  # 長方形の壁
    
    obstacle_type = 3
    
    if obstacle_type == 1:
        obstacles = [wall_1, wall_2]
    elif  obstacle_type == 2:
        obstacles = [circle_1]
    else:
        obstacles = [wall_1, wall_2, circle_1]
    
    # calc distance
    #distance = calc_distance(lidar_beam_1, wall_1, lidar_x, lidar_y, lidar_range_m)
    distance = calc_distance_multi(lidar_beam_1, obstacles, lidar_x, lidar_y, lidar_range_m)
    
    # 📢 測定結果
    print(f"LIDAR 測定距離: {distance:.2f} m")
        
    # プロット
    plt.plot(lidar_x, lidar_y, "ro")
    plot_shapely_line(lidar_beam_1, color="red", linestyle="dashed", label="Lidar Beam")
    
    if obstacle_type == 1:
        plot_shapely_line(wall_1, color="black", linestyle="solid", label="Wall")
        plot_shapely_line(wall_2, color="black", linestyle="solid", label="Wall")
    elif obstacle_type == 2:
        plot_shapely_circle(circle_1, color="blue", label="Circle")
    else:
        plot_shapely_line(wall_1, color="black", linestyle="solid", label="Wall")
        plot_shapely_line(wall_2, color="black", linestyle="solid", label="Wall")
        plot_shapely_circle(circle_1, color="blue", label="Circle")
        
    plt.grid(True)
    plt.axis("equal")
    plt.show()
