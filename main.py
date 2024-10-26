from ETS2LA.Plugin import *
from ETS2LA.UI import *
import time
import math

class Plugin(ETS2LAPlugin):
    author = Author(
        name="Zia",
        url="https://wiki.ets2la.com",
        icon="https://wiki.ets2la.com/assets/favicon.ico"
    )
    description = PluginDescription(
        name="ETS2LA-OpenShock",
        version="1.0.0",
        description="ETS2LA and ETS2's Implmentation with Open Shock",
        compatible_os=["Windows", "Linux"],
        compatible_game=["ETS2"],
        update_log={
            "1.0.0": "Initial release"
        }
    )
    def imports(self):
        global torch, np
        import numpy as np
        import torch
    def run(self):
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
            return
        else:
            self.notify("Plugin Disabled", type="error")
            return
        distaneFromCenter = self.globals.tags.lateral_offset
        print(distaneFromCenter)
        if distaneFromCenter == "None":
            self.notify("Please Enable The Map Plugin To Use This Plugin", type="error")
            return