import numpy as np

# --- 1. 输入矩阵 ---
# Kalibr 文件中的 T_cam_imu 通常表示 T_imu_from_cam
# 即从相机坐标系到 IMU 坐标系的变换

# T_imu_from_cam0: 从 cam0 坐标系到 IMU 坐标系的变换
T_imu_from_cam0 = np.array([
   [0.0008247496568674628, 0.9999961104998093, -0.002664352314491823, 0.043041669055924436],
   [-0.9999929524133787, 0.0008149826348758382, -0.003664822898610003, 0.003376471075594937],
   [-0.0036626372434111396, 0.0026673560986662063, 0.9999897350972485, -0.021104195227740437],
   [0.0, 0.0, 0.0, 1.0]
])

# T_imu_from_cam1: 从 cam1 坐标系到 IMU 坐标系的变换
T_imu_from_cam1 = np.array([
    [-0.001835964017484093, 0.999979457302906, -0.00614118948676923, -0.07410578385444819],
   [-0.9999970575613598, -0.001845664547293735, -0.001574290634432294, 0.003383609126826685],
   [-0.001585592869970595, 0.0061382810757381065, 0.9999799034984085, -0.021194379548050524],
   [0.0, 0.0, 0.0, 1.0]
])


# --- 2. 使用修正后的公式计算 ---
# 正确公式: T_c1_c0 = inv(T_imu_from_c1) * T_imu_from_c0

# 首先，计算 T_imu_from_cam1 的逆矩阵
# 这相当于得到了从 IMU 坐标系到 cam1 坐标系的变换 T_cam1_from_imu
try:
    T_cam0toimu = np.linalg.inv(T_imu_from_cam0)
except np.linalg.LinAlgError:
    print("错误：T_imu_from_cam1 矩阵是奇异矩阵，无法计算逆矩阵。")
    exit()

# 然后，执行矩阵乘法
# (T_c1 <- imu) * (T_imu <- c0) = (T_c1 <- c0)
T_cam1_cam0 = T_cam0toimu @ T_imu_from_cam1


# --- 3. 输出结果 ---
# 设置打印选项，使输出更易读
np.set_printoptions(precision=17, suppress=True)

print("✅ 计算完成！(已使用修正逻辑)")
print("cam1 的 T_cn_cnm1 (即 T_cam1_cam0) 矩阵为:")
print(T_cam1_cam0)

print("\n📋 YAML 格式:")
for row in T_cam1_cam0:
    formatted_row = f"    - [{', '.join(f'{val:.17f}' for val in row)}]"
    print(formatted_row)
