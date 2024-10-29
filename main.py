from ETS2LA.Plugin import *
from ETS2LA.UI import *
import time
import math

class Plugin(ETS2LAPlugin):
    author = Author(
        name="Zia",
        url="https://github.com/Zia-ullah-khan",
        icon="https://avatars.githubusercontent.com/u/88408107?s=400&v=4"
    )
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

    def imports(self):
        global torch, np
        import numpy as np
        import torch
    
    def warning(self):
        if not self.warningShown:
            warning = '''
            <img src="https://raw.githubusercontent.com/Zia-ullah-khan/ETS2LA-OpenShock/main/assets/safety-front.png" style="width: 50px;"> 
            <img src="https://raw.githubusercontent.com/Zia-ullah-khan/ETS2LA-OpenShock/main/assets/safety-back.png" style="width: 50px;"><br> 
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
        api_values = self.modules.TruckSimAPI.run()
        self.warning()
        distaneFromCenter = self.globals.tags.lateral_offset
        print(distaneFromCenter)
        if distaneFromCenter is None or distaneFromCenter == "None":
            self.notify("Please Enable The Map Plugin To Use This Plugin", type="error")
            return
        if distaneFromCenter > 1.5 or distaneFromCenter < -1.5 and blinkerLeftActive == false or blinkerRightActive == false:
             #shock the user
