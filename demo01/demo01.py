import sys
import os

# Isaac Sim 路径
ISAAC_SIM_PATH = r"E:\OmniverseSpace\isaac-sim-standalone-5.0.0-windows-x86_64"

# 将 Isaac Sim 的 Python 路径添加到 sys.path
# 这样 Python 才能找到 omni.isaac.kit 模块
isaac_sim_python_path = os.path.join(ISAAC_SIM_PATH, "python-packages")
if isaac_sim_python_path not in sys.path:
    sys.path.insert(0, isaac_sim_python_path)

# 导入 SimulationApp (必须在添加路径后导入)
from omni.isaac.kit import SimulationApp  # noqa: E402

# 配置启动参数
config = {"headless": True}

# 启动 Isaac Sim (无界面模式)
print("正在启动 Isaac Sim (无界面模式)...")
simulation_app = SimulationApp(config)

print("Isaac Sim 已启动 (无界面模式)")

# 在这里可以添加你的仿真代码
# ...

# 关闭 Isaac Sim
# simulation_app.close()
