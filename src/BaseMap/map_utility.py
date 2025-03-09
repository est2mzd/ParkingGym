import numpy as np
from matplotlib import pyplot as plt

#==============================================================#
def rot_mat_2d(angle_rad):
    """2D回転行列"""
    return np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                     [np.sin(angle_rad), np.cos(angle_rad)]])

#==============================================================#
def create_line(start, end, ds, delete_end_point=False):
    """
    2点 (start, end) を結ぶ直線の xy 点群を ds 間隔で生成

    Parameters:
        start : list [x, y] (開始点)
        end   : list [x, y] (終了点)
        ds    : float 点の間隔 [m]
        delete_end_point : True > 終点を削除.多角形を作ろときに便利

    Returns:
        line_x, line_y : numpy.ndarray (直線上の x, y 座標リスト)
    """
    # 2点間の距離を計算
    length = np.hypot(end[0] - start[0], end[1] - start[1])

    # 点の個数を計算（両端含む）
    num_points = int(length / ds) + 1

    # X, Y の点群を生成
    line_x = np.linspace(start[0], end[0], num_points)
    line_y = np.linspace(start[1], end[1], num_points)

    if delete_end_point:
        line_x = line_x[:-1]
        line_y = line_y[:-1]

    return line_x, line_y

#==============================================================#
def create_circle(x, y, radius, ds):
    """
    円周上の xy 点群を ds 間隔で生成

    Parameters:
        x : float (円の中心 x 座標)
        y : float (円の中心 y 座標)
        radius : float (円の半径)
        ds : float (点の間隔 [m])

    Returns:
        circle_x, circle_y : numpy.ndarray (円周上の x, y 座標リスト)
    """
    # 円周の長さを計算
    circumference = 2 * np.pi * radius

    # 必要な点の数を計算
    num_points = int(circumference / ds) + 1

    # 角度を均等に分割
    angles = np.linspace(0, 2 * np.pi, num_points)

    # 円周上の点を計算
    circle_x = x + radius * np.cos(angles)
    circle_y = y + radius * np.sin(angles)

    return circle_x, circle_y

#==============================================================#
if __name__ == '__main__':
    # テスト用
    start = [0, 0]
    end   = [5, 4]
    ds    = 0.5
    #
    x, y = 5, 4
    radius = 2
    
    # 点群の作成
    line_x, line_y = create_line(start, end, ds)
    line_x2, line_y2 = create_circle(x, y, radius, ds)
    
    # プロット
    plt.plot(line_x,  line_y,  "ro")
    plt.plot(line_x2, line_y2, "bo")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

