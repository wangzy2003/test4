import math
import pandas as pd


# 定义经纬度转换为米勒坐标的方法
def millerToXY(lon, lat):
    xy_coordinate = []
    L = 6381372 * math.pi * 2  # 地球周长
    W = L  # 平面展开，将周长视为 X 轴
    H = L / 2  # Y 轴约等于周长一半
    mill = 2.3  # 米勒投影中的一个常数，范围大约在正负 2.3 之间

    # 循环，因为要批量转换
    for x, y in zip(lon, lat):
        x = x * math.pi / 180  # 将经度从度数转换为弧度
        y = y * math.pi / 180  # 将纬度从度数转换为弧度
        y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y))  # 米勒投影转换
        x = (W / 2) + (W / (2 * math.pi)) * x  # 将弧度转为实际距离，单位为 km
        y = (H / 2) - (H / (2 * mill)) * y  # 将弧度转为实际距离，单位为 km
        xy_coordinate.append((int(round(x)), int(round(y))))

    return xy_coordinate


# 读取 Excel 数据文件，指定多级表头
df = pd.read_excel(r"D:\科研--海洋数据分析\图神经网络--珠三角\珠江河网逐时水文数据\坐标.xlsx", header=[0, 1])
#"D:\科研--海洋数据分析\图神经网络--珠三角\珠江河网逐时水文数据\坐标.xlsx"
# 获取起点和终点的经纬度数据
start_lon = df[('起点', 'X(°E)')]  # 起点经度
start_lat = df[('起点', 'Y(°N)')]  # 起点纬度
end_lon = df[('终点', 'X(°E)')]  # 终点经度
end_lat = df[('终点', 'Y(°N)')]  # 终点纬度

# 调用经纬度转化为 XY 坐标的方法
start_xy = millerToXY(start_lon, start_lat)  # 起点的 XY 坐标
end_xy = millerToXY(end_lon, end_lat)  # 终点的 XY 坐标

# 将转换结果添加到原 DataFrame 中
df[('起点', 'X_米勒')] = [xy[0] for xy in start_xy]
df[('起点', 'Y_米勒')] = [xy[1] for xy in start_xy]
df[('终点', 'X_米勒')] = [xy[0] for xy in end_xy]
df[('终点', 'Y_米勒')] = [xy[1] for xy in end_xy]

df.columns = [' '.join(col).strip() for col in df.columns.values]

# 将结果保存到新的 Excel 文件，保留多层表头
df.to_excel(r"D:\科研--海洋数据分析\图神经网络--珠三角\珠江河网逐时水文数据\坐标jm-zy.xlsx", index=False)
