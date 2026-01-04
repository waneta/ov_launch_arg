import sys
import os

# 导入 SimulationApp (参考 isaacsim.simulation_app 示例)
from isaacsim import SimulationApp

# 配置启动参数 - 无界面模式
CONFIG = {
    "headless": True,
    "sync_loads": True,
}

# 启动 Isaac Sim (无界面模式)
print("正在启动 Isaac Sim (无界面模式)...")
kit = SimulationApp(launch_config=CONFIG)

# 等待几帧以确保扩展系统初始化
for i in range(10):
    kit.update()

print("Isaac Sim 已启动 (无界面模式)")

# 导入必要的模块
import omni.kit.app
import omni.ext

def find_active_extension_id(prefix: str):
    ext_manager = omni.kit.app.get_app().get_extension_manager()
    ext_list = ext_manager.get_extensions()
    for ext in ext_list:
        '''
        print(f"ID: {ext['id']}")
        print(f"Version: {ext['version']}")
        print(f"Enabled: {ext['enabled']}")
        print(f"Dependencies: {ext.get('dependencies', [])}")

        ID: datamesh.factverse_ovadaptor_extension-1.0.1
        Version: (1, 0, 1, '', '')
        Enabled: True
        Dependencies: []
        '''
        if ext["id"].startswith(prefix) and ext["enabled"]:
            return ext["id"]
    print(f"No active extension found for prefix: {prefix}")
    return None

# 获取扩展管理器
ext_manager = omni.kit.app.get_app().get_extension_manager()
ext_id = "datamesh.factverse_ovadaptor_extension"

# 检查扩展是否已加载
if not ext_manager.is_extension_enabled(ext_id):
    print(f"扩展 {ext_id} 未启用，尝试启用...")
    ext_manager.set_extension_enabled_immediate(ext_id, True)
    # 等待扩展加载
    for i in range(20):
        kit.update()

# 获取扩展实例并调用登录方法
try:
    # 导入扩展模块
    from datamesh.factverse_ovadaptor_extension.extension import DatameshFactverse_extensionExtension
    import omni.ui as ui
    
    extension_path = ext_manager.get_extension_path(ext_id)
    print(f"扩展路径: {extension_path}")
    
    # 等待扩展完全初始化
    print("等待扩展初始化...")
    for i in range(50):
        kit.update()
    
    # 设置登录参数
    nucleus_ip = "localhost"
    server_url = "https://dcs.datamesh.com"
    account_id = "test@datamesh.com"
    password = "abc123456"
    scene_id = "f26713a578954506a8b1cee80862c965"
    record_id = ""
    
    print(f"\n登录参数:")
    print(f"  Nucleus IP: {nucleus_ip}")
    print(f"  Server URL: {server_url}")
    print(f"  Account ID: {account_id}")
    print(f"  Scene ID: {scene_id}")
    print(f"  Record ID: {record_id}\n")
    
    # 获取扩展实例
    # 扩展由系统管理，我们需要找到已启动的实例
    ext_instance = None
    
    # 方法1: 通过扩展管理器获取已启动的扩展实例
    try:
        # 扩展系统在启动扩展时会创建实例
        # 我们可以通过扩展的接口获取
        import datamesh.factverse_ovadaptor_extension.extension as ext_module
        
        # 尝试多种方式获取实例
        # 方式1: 检查模块级别的全局变量
        if hasattr(ext_module, '_instance'):
            ext_instance = ext_module._instance
            print("通过模块全局变量获取扩展实例")
        
        # 方式2: 检查是否有注册的实例
        if ext_instance is None and hasattr(ext_module, 'get_instance'):
            ext_instance = ext_module.get_instance()
            print("通过 get_instance 方法获取扩展实例")
        
        # 方式3: 通过扩展管理器获取扩展接口
        if ext_instance is None:
            try:
                # 获取扩展的接口（如果扩展实现了接口）
                ext_id_obj = ext_manager.get_extension_id_by_path(extension_path)
                if ext_id_obj:
                    # 尝试获取扩展的接口实例
                    # 注意：这取决于扩展的实现方式
                    pass
            except:
                pass
                
    except Exception as e:
        print(f"尝试获取扩展实例时出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 方法2: 如果无法获取已启动的实例，尝试创建新实例
    # 注意：这可能会与系统管理的实例冲突
    if ext_instance is None:
        print("无法获取已启动的扩展实例，尝试创建新实例...")
        try:
            ext_instance = DatameshFactverse_extensionExtension()
            # 调用 on_startup（需要 ext_id）
            ext_id_obj = ext_manager.get_extension_id_by_path(extension_path)
            if ext_id_obj:
                print(f"调用扩展的 on_startup，ext_id: {ext_id_obj}")
                ext_instance.on_startup(ext_id_obj)
                # 等待扩展初始化
                print("等待扩展初始化...")
                for i in range(30):
                    kit.update()
                print("扩展初始化完成")
        except Exception as e:
            print(f"创建扩展实例失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 如果成功获取实例，设置 UI 组件并调用方法
    if ext_instance:
        print("扩展实例已获取，准备调用登录方法...")
        print(f"扩展实例类型: {type(ext_instance)}")
        
        # 检查扩展的关键组件是否已初始化
        if not hasattr(ext_instance, 'ov_adaptor') or ext_instance.ov_adaptor is None:
            print("警告: ov_adaptor 未初始化，尝试初始化...")
            try:
                from datamesh.factverse_ovadaptor_extension.factverse_ovadaptor import FactVerseOVAdaptor
                ext_instance.ov_adaptor = FactVerseOVAdaptor()
                print("ov_adaptor 初始化成功")
            except Exception as e:
                print(f"初始化 ov_adaptor 失败: {e}")
        
        # 创建模拟的 UI 组件（因为 on_click_login 需要 UI 输入字段）
        class MockStringModel:
            def __init__(self, value):
                self._value = value
            def get_value_as_string(self):
                return self._value
            def set_value(self, value):
                self._value = value
        
        class MockStringField:
            def __init__(self, value=""):
                self.model = MockStringModel(value)
        
        class MockLabel:
            def __init__(self):
                self.text = ""
                self.style = {}
        
        class MockButton:
            def __init__(self):
                self.enabled = True
        
        class MockProgressModel:
            def set_value(self, value):
                pass
        
        class MockProgressBar:
            def __init__(self):
                self.visible = False
                self._model = MockProgressModel()
            @property
            def model(self):
                return self._model
        
        # 设置模拟的 UI 组件（如果不存在）
        if not hasattr(ext_instance, 'input_nucleus_ip') or ext_instance.input_nucleus_ip is None:
            ext_instance.input_nucleus_ip = MockStringField(nucleus_ip)
            ext_instance.input_server_url = MockStringField(server_url)
            ext_instance.input_account_id = MockStringField(account_id)
            ext_instance.input_pass = MockStringField(password)
            ext_instance.input_scene_id = MockStringField(scene_id)
            ext_instance.input_record_id = MockStringField(record_id)
        
        if not hasattr(ext_instance, 'label_status') or ext_instance.label_status is None:
            ext_instance.label_status = MockLabel()
        
        if not hasattr(ext_instance, '_buttons') or ext_instance._buttons is None:
            ext_instance._buttons = {}
        if "Connect" not in ext_instance._buttons:
            ext_instance._buttons["Connect"] = MockButton()
        if "Stop" not in ext_instance._buttons:
            ext_instance._buttons["Stop"] = MockButton()
        
        if not hasattr(ext_instance, 'progress_bar') or ext_instance.progress_bar is None:
            ext_instance.progress_bar = MockProgressBar()
        
        # 调用登录方法
        print("\n" + "="*50)
        print("准备调用登录方法...")
        print("="*50)
        
        # 首先调用测试方法 on_click_login2
        try:
            print("调用 on_click_login2 (测试方法)...")
            ext_instance.on_click_login2()
            print("✓ on_click_login2 调用成功")
        except Exception as e:
            print(f"✗ 调用 on_click_login2 时出错: {e}")
            import traceback
            traceback.print_exc()
        
        # 如果需要调用真正的登录方法，取消下面的注释
        # print("\n调用 on_click_login (真正的登录方法)...")
        # try:
        #     ext_instance.on_click_login()
        #     print("✓ on_click_login 方法调用成功")
        # except Exception as e:
        #     print(f"✗ 调用 on_click_login 时出错: {e}")
        #     import traceback
        #     traceback.print_exc()
    else:
        print("✗ 警告：无法获取或创建扩展实例")
        print("提示：扩展可能需要在有 UI 的环境中运行，或者需要修改扩展以支持程序化调用")
    
except Exception as e:
    print(f"获取或调用扩展时出错: {e}")
    import traceback
    traceback.print_exc()

# 运行主循环
print("运行主循环...")
try:
    for i in range(100):
        kit.update()
except KeyboardInterrupt:
    print("收到中断信号")

# 关闭 Isaac Sim
print("正在关闭 Isaac Sim...")
kit.close()
print("Isaac Sim 已关闭")
