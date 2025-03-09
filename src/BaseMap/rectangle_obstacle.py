import numpy as np
import matplotlib.pyplot as plt
from map_utility import create_line, rot_mat_2d

#==============================================================#
def create_rectangle_with_rear_end(x, y, yaw, width, length, ds):
    """
    長方形の4辺の座標を計算(後端中心を基準)

    Parameters:
        x, y , yaw  : 後端中心の座標
        width  : 幅
        length : 長
        yaw    : 長方形の向き(ラジアン)
        ds     : 点群の間隔 [m]

    Returns:
        rectangle_x, rectangle_y : 回転後の4隅の座標リスト
    """
    # 車両の4隅(後端中心基準)
    rear_left   = [- width / 2, 0]
    rear_right  = [  width / 2, 0]
    front_left  = [- width / 2, length]
    front_right = [  width / 2, length]
    
    # 4辺のxy座標
    delete_end_point = True
    front_line_x, front_line_y = create_line(front_left, front_right, ds, delete_end_point)
    right_line_x, right_line_y = create_line(front_right, rear_right, ds, delete_end_point)
    rear_line_x,  rear_line_y  = create_line(rear_right,   rear_left, ds, delete_end_point)
    left_line_x,  left_line_y  = create_line(rear_left,   front_left, ds, delete_end_point)
    
    # 全てのxy座標 --> all_xy の size = (2,N)
    all_x  = np.concatenate([front_line_x, right_line_x, rear_line_x, left_line_x])
    all_y  = np.concatenate([front_line_y, right_line_y, rear_line_y, left_line_y])
    all_xy = np.vstack((all_x, all_y))

    # 回転行列を適用
    rot    = rot_mat_2d(yaw)
    all_xy = rot @ all_xy

    # 平行移動 (x, y を基準に)
    x_list = all_xy[0, :] + x
    y_list = all_xy[1, :] + y

    # デバッグ・プロット
    if False:
        plt.plot(front_line_x, front_line_y, "r.")
        plt.plot(right_line_x, right_line_y, "g.")
        plt.plot(rear_line_x,  rear_line_y,  "b.")
        plt.plot(left_line_x,  left_line_y,  "c.")
        plt.grid(True)
        plt.axis("equal")
        plt.show()


    return x_list, y_list

#==============================================================#
def create_rectangle_with_center(x, y, yaw, width, length, ds):
    """
    長方形の4辺の座標を計算(中心を基準)

    Parameters:
        x, y , yaw  : 後端中心の座標
        width  : 幅
        length : 長
        yaw    : 長方形の向き(ラジアン)
        ds     : 点群の間隔 [m]

    Returns:
        rectangle_x, rectangle_y : 回転後の4隅の座標リスト
    """
    # 車両の4隅(後端中心基準)
    rear_left   = [- width / 2, - length / 2]
    rear_right  = [  width / 2, - length / 2]
    front_left  = [- width / 2,   length / 2]
    front_right = [  width / 2,   length / 2]
    
    # 4辺のxy座標
    delete_end_point = True
    front_line_x, front_line_y = create_line(front_left, front_right, ds, delete_end_point)
    right_line_x, right_line_y = create_line(front_right, rear_right, ds, delete_end_point)
    rear_line_x,  rear_line_y  = create_line(rear_right,   rear_left, ds, delete_end_point)
    left_line_x,  left_line_y  = create_line(rear_left,   front_left, ds, delete_end_point)
    
    # 全てのxy座標 --> all_xy の size = (2,N)
    all_x  = np.concatenate([front_line_x, right_line_x, rear_line_x, left_line_x])
    all_y  = np.concatenate([front_line_y, right_line_y, rear_line_y, left_line_y])
    all_xy = np.vstack((all_x, all_y))

    # 回転行列を適用
    rot    = rot_mat_2d(yaw)
    all_xy = rot @ all_xy

    # 平行移動 (x, y を基準に)
    x_list = all_xy[0, :] + x
    y_list = all_xy[1, :] + y

    # デバッグ・プロット
    if False:
        plt.plot(front_line_x, front_line_y, "r.")
        plt.plot(right_line_x, right_line_y, "g.")
        plt.plot(rear_line_x,  rear_line_y,  "b.")
        plt.plot(left_line_x,  left_line_y,  "c.")
        plt.grid(True)
        plt.axis("equal")
        plt.show()


    return x_list, y_list



#==============================================================#
if __name__ == '__main__':
    # テスト用
    x   = 0
    y   = 0
    yaw = np.deg2rad(-60)
    width = 2.5
    length = 10
    ds    = 0.5
    
    # 点群の作成
    x_list, y_list   = create_rectangle_with_rear_end(x, y, yaw, width, length, ds)
    x_list2, y_list2 = create_rectangle_with_center(x, y, yaw, width, length, ds)
    
    # プロット
    if True:
        plt.plot(x_list, y_list, "ro")
        plt.plot(x_list2, y_list2, "bo")
        plt.grid(True)
        plt.axis("equal")
        plt.show()