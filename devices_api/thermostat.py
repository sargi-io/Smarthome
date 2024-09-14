from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_THERMOSTAT

class BaseThermostat(Accessory):
    category = CATEGORY_THERMOSTAT

    def __init__(self, bmr, room_index, room_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bmr = bmr
        self.room_id = room_index
        self.name = room_name

        # Add Thermostat service
        thermostat_service = self.add_preload_service('Thermostat')
        
        # Get current and target temperature characteristics
        self.current_temp_char = thermostat_service.get_characteristic('CurrentTemperature')
        self.target_temp_char = thermostat_service.get_characteristic('TargetTemperature')

        # Set initial temperature
        self.update_current_temperature()

        # Set the callback for the TargetTemperature
        self.target_temp_char.setter_callback = self.set_target_temperature

    def update_current_temperature(self):
        # Get the current temperature from BMR and update the characteristic
        circuit = self.bmr.getCircuit(self.room_id)
        current_temp = circuit['temperature']
        self.current_temp_char.set_value(current_temp)

    def set_target_temperature(self, value):
        # Set the new temperature using BMR system
        self.bmr.setManualTemp(self.room_id, value)
        self.bmr.setManualTemp(self.room_id+10, value)
        print(f"Setting new target temperature: {value}°C for room {self.name}")