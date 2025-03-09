import math
#
def create_map(ox, oy):
    print("Call : create_map")
    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(40):
        ox.append(20.0)
        oy.append(i)
    for i in range(40):
        ox.append(40.0)
        oy.append(60.0 - i)

    if False:
        # add circle
        # 円の中心座標
        x_center = 30.0
        y_center = 30.0
        radius = 3.0
        num_points = 40  # 点の数

        # 角度を等間隔にして円周上の点を計算
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points  # 角度（ラジアン）
            ox.append(x_center + radius * math.cos(angle))
            oy.append(y_center + radius * math.sin(angle))
    
    if False:
        # add circle
        # 円の中心座標
        x_center = 30.0
        y_center = 40.0
        radius = 3.0
        num_points = 40  # 点の数

        # 角度を等間隔にして円周上の点を計算
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points  # 角度（ラジアン）
            ox.append(x_center + radius * math.cos(angle))
            oy.append(y_center + radius * math.sin(angle))    

    if False:    
        # add circle
        # 円の中心座標
        x_center = 30.0
        y_center = 25.0
        radius = 3.0
        num_points = 40  # 点の数

        # 角度を等間隔にして円周上の点を計算
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points  # 角度（ラジアン）
            ox.append(x_center + radius * math.cos(angle))
            oy.append(y_center + radius * math.sin(angle))      
    
    return ox, oy