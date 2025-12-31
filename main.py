import dearpygui.dearpygui as dpg

def setup_dpg():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

def desetup_dpg():
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def button_callback(sender, data):
    print("Button Clicked")

setup_dpg()

with dpg.window(label="OptimusEditor", tag="main_window"):
    dpg.add_text("This is a text")
    dpg.add_button(label="Click this Button!", callback=button_callback)

dpg.set_primary_window("main_window", True)  # Делаем primary

desetup_dpg()