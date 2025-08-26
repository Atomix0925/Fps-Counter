import time
import ctypes
import psutil
import dearpygui.dearpygui as dpg

# Hide console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

dpg.create_context()

selected_process = {"name": None}  

def get_process_names():
    names = []
    for proc in psutil.process_iter(['name']):
        try:
            names.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(set(names))

def on_process_selected(sender, app_data, user_data):
    selected_process["name"] = app_data
    dpg.configure_item("StartButton", show=True)

def on_start_fps(sender, app_data, user_data):
    dpg.configure_item("FPSLabel", show=True)
    dpg.configure_item("StartButton", show=False)
    dpg.configure_item("ProcessSelector", enabled=False)

with dpg.window(label="FPS Counter", tag="MainWindow", width=300, height=150):
    dpg.add_text("Select a process:")
    dpg.add_combo(get_process_names(), tag="ProcessSelector", callback=on_process_selected)
    dpg.add_button(label="Start FPS Counter", tag="StartButton", show=False, callback=on_start_fps)
    dpg.add_text("FPS: ", tag="FPSLabel", show=False)

dpg.create_viewport(title="FPS Counter", width=300, height=150)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    if selected_process["name"]:
        if dpg.is_item_shown("FPSLabel"):
            fps = dpg.get_frame_rate()
            dpg.set_value("FPSLabel", f"{fps:.2f} FPS")
    dpg.render_dearpygui_frame()
    time.sleep(0.01)

dpg.destroy_context()