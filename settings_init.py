from settings_manager import SettingsManager

def initialize_settings():
    #create instance of settings manager
    settings = SettingsManager("settings.json")

    #initialize settings

    #debug
    settings.add_setting("debug","Display extra debuging output on screen?", "False", ("True","False"))

    #orientation
    orientation_setting_description = "This flips the map and the tokens so they are facing players\n"
    orientation_setting_description += "that are sitting across from the dm.\n"
    orientation_setting_description += "It also displays messages on all 4 sides of the screen facing outward,\n"
    orientation_setting_description += "instead of just one at the bottom."
    settings.add_setting("table_top_orientation",orientation_setting_description,"False",("True","False"))

    #return the settings manager
    return settings
