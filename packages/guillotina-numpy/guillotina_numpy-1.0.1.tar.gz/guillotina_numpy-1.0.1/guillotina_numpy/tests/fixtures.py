from guillotina import testing


def base_settings_configurator(settings):
    if "applications" in settings:
        settings["applications"].append("guillotina_numpy")
    else:
        settings["applications"] = ["guillotina_numpy"]


testing.configure_with(base_settings_configurator)
