from ETS2LA.Plugin import *
from ETS2LA.UI import *
import time
import math

class SettingsMenu(ETS2LASettingsMenu):
    dynamic = True
    plugin_name = "OpenShockConnect"

    def render(self):
        # dynamic settings menus have access to self.plugin to access the running plugin object


        Title("Shock me uwu")
        Description("Get shocked uwu")
        
        with EnabledLock(): # Will show the elements as blurred until the plugin is enabled.
            if self.plugin is not None:
                Label("Connection Status: " + str(self.plugin.connectstate))

        Separator()
        Selector("OpenShock Api Sever", "apiserver", "api.openshock", ["api.openshock", "Custom"], description="The OpenShock API Server to connect to", requires_restart=True)
        Input("OpenShock Api Token", "api_token", "number", "", description="The OpenShock API Token to use", requires_restart=True)

        with EnabledLock(): # Will show the elements as blurred until the plugin is enabled.
            if self.plugin is not None:
                #Display a selector with shocker list to choose a device to use
                Selector("Device", "deviceid", "" , self.plugin.shocker_ids, description="The device to use", requires_restart=True)
        Separator()
        Input("Vibration Lane Offset", "vibration_offset", "number", 1, description="The vibration offset to use")
        Input("Vibration Duration", "vibration_duration", "number", 300, description="The duration of the vibration to use")
        Input("Shock Lane Offset", "shock_offset", "number", 1.25, description="The shock offset to use")
        Input("Shock Duration", "shock_duration", "number", 0.5, description="The duration of the shock to use")
        Input("Shock Intensity", "shock_intensity", "number", 0.5, description="The intensity of the shock to use")
        Separator()
        
        with EnabledLock(): # Will show the elements as blurred until the plugin is enabled.
            if self.plugin is not None:
                Label("Lane Offset: " + str(self.plugin.LaneOffset))
                
                

        return RenderUI()
        
class Plugin(ETS2LAPlugin):
    settings_menu = SettingsMenu()
    connectstate = ""
    shocker_ids = []
    LaneOffset = 0

    author = [
        Author(
            name="Cloud",
            url="https://github.com/Cloud-121",
            icon="https://avatars.githubusercontent.com/u/83072683?v=4"
        ), 
        Author(
            name="Zia",
            url="https://wiki.ets2la.com",
            icon="https://wiki.ets2la.com/assets/favicon.ico"
        )
    ]

    description = PluginDescription(
        name="ETS2LA-OpenShock",
        version="1.0.0",
        description="ETS2LA and ETS2's Implementation with Open Shock",
        compatible_os=["Windows", "Linux"],
        compatible_game=["ETS2"],
        modules = ["TruckSimAPI"],
        update_log={
            "1.0.0": "Initial release"
        }
    )
    
    warningShown = False
    makeconnection = False

    def imports(self):
        global torch, np, OpenShockAPI
        import numpy as np
        import torch
        from plugins.OpenShockConnect.openshocksdk import OpenShockAPI
    
    def warning(self):
        if not self.warningShown:
            warning = '''
            <img src="https://raw.githubusercontent.com/Zia-ullah-khan/ETS2LA-OpenShock/main/assets/safety-front.png" style="width: 20px;"> 
            <img src="https://raw.githubusercontent.com/Zia-ullah-khan/ETS2LA-OpenShock/main/assets/safety-back.png" style="width: 20px;"><br> 
            <h1>Safety Warning!</h1><br> 
            <h2>Please use the images above as a guide of where to add the shock pads.</h2><br> 
            <h2>The Developers of this plugin are not responsible for any damage or harm caused by this plugin.</h2><br>
            <h2>Do you agree to use this plugin under your own supervision?</h2>
            '''
            answer = self.ask(warning, options=["Yes", "No"], description="WARNING!")
            if answer == "Yes":
                self.notify("Plugin Enabled", type="success")
                self.warningShown = True
            else:
                self.notify("Plugin Disabled", type="error")
    
    def run(self):
        self.warning()
        if self.makeconnection == False:
            try:
                apiserver = ""
                apiserver = self.settings.apiserver
                if apiserver == "api.openshock":
                    self.settings.actualapiserver = "https://api.openshock.app"
                    server = "https://api.openshock.app"
                elif apiserver == "Custom":
                    print("UNSUPPORTED")
                
                api_token = ""
                api_token = self.settings.api_token

                openshock = OpenShockAPI(token=api_token, base_url=server)
                self.makeconnection = True
                shockers = openshock.list_shockers()

                for shocker in shockers:
                    self.shocker_ids.append(shocker['device_id'])



                
                

                

                

                self.connectstate = "Connected"
            except Exception as e:
                print(e)
                self.connectstate = "Not Connected"

            
        




        api_values = self.modules.TruckSimAPI.run()

        distaneFromCenter = self.globals.tags.lateral_offset

        self.LaneOffset = distaneFromCenter
        if distaneFromCenter == "None":
            distaneFromCenter = 0


        
        #Shocking :3

        #Setting some values
        blinkeractive = False

        #Get values

        shocker_id = self.settings.deviceid
        viblaneoffset = self.settings.vibration_offset
        vibduration = self.settings.vibration_duration
        shocklaneoffset = self.settings.shock_offset
        shockduration = self.settings.shock_duration
        shockintensity = self.settings.shock_intensity
        if api_values["truckBool"]["blinkerLeftActive"] == True or api_values["truckBool"]["blinkerRightActive"] == True:
            blinkeractive = True

        #Check for vibration
        try:

            if distaneFromCenter != "None":
                distaneFromCenter = abs(distaneFromCenter['Map'])

                if self.connectstate == "Connected":
                    
                    if (distaneFromCenter > shocklaneoffset) and blinkeractive == False:
                            openshock = OpenShockAPI(token=self.settings.api_token, base_url=self.settings.actualapiserver)
                            shocks = [{
                                "id": shocker_id,
                                "type": "Shock",
                                "intensity": shockintensity,
                                "duration": shockduration,
                                "exclusive": True
                            }]
                            response = openshock.control_device(shocks=shocks, custom_name="Exit Lane Shock")

                            print("Shocked")



                    elif (distaneFromCenter > viblaneoffset ) and blinkeractive == False:
                            openshock = OpenShockAPI(token=self.settings.api_token, base_url=self.settings.actualapiserver)
                            shocks = [{
                                "id": shocker_id,
                                "type": "Vibrate",
                                "intensity": 100,
                                "duration": vibduration,
                                "exclusive": True
                            }]
                            response = openshock.control_device(shocks=shocks, custom_name="Exit Lane Vibration")

                            print("Vibrated")


                
        except Exception as e:
            print(e)
            