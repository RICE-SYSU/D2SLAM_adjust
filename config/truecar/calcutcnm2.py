import numpy as np

# --- 1. 输入矩阵 ---
# Kalibr 文件中的 T_cam_imu 

T_cam0_imu = np.array([
[-0.9995407230847781, 0.029100449860456495, -0.008456164206050667, 0.04812531099830761],
  [0.007419008250330716, -0.035565792521783365, -0.9993397984263814, -0.046268993994975235],
   [-0.02938198787934812, -0.9989435610785118, 0.03533356149670343, -0.06808128621572819],
   [0.0, 0.0, 0.0, 1.0]
])


T_cam1_imu = np.array([
  [-0.9995333551739931, 0.029563758443646823, -0.007684795462836215, -0.05277683771177886],
   [0.008020445760736369, 0.01125165640719669, -0.9999045317818563, -0.04396772695601477],
  [-0.029474469366199164, -0.9994995669907917, -0.011483520401031096, -0.0711950391086574],
  [0.0, 0.0, 0.0, 1.0]
])


# --- 2. 使用修正后的公式计算 ---
# 正确公式: T_c1_c0 = inv(T_imu_from_c1) * T_imu_from_c0

# 首先，计算 T_imu_from_cam1 的逆矩阵
# 这相当于得到了从 IMU 坐标系到 cam1 坐标系的变换 T_cam1_from_imu
try:
    T_imu_cam0 = np.linalg.inv(T_cam0_imu)
except np.linalg.LinAlgError:
    print("错误：T_imu_from_cam1 矩阵是奇异矩阵，无法计算逆矩阵。")
    exit()
# print T_imu_cam1:
print("T_imu_cam1 矩阵为:")
print(T_imu_cam0)


# 然后，执行矩阵乘法
# (T_c1 <- imu) * (T_imu <- c0) = (T_c1 <- c0)
T_cam1_cam0 = T_cam1_imu @ T_imu_cam0


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
