from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_THERMOSTAT

class StudyMojmirThermostat(Accessory):
    category = CATEGORY_THERMOSTAT

    def __init__(self, bmr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bmr = bmr
        self.room_id = 7
        self.name = "Mojmirs study"
        self.circuit = self.bmr.getCircuit(self.room_id)
      
        # Add Thermostat service
        thermostat_service = self.add_preload_service('Thermostat')
        
        # Get current and target temperature characteristics and heating status
        self.current_temp_char = thermostat_service.get_characteristic('CurrentTemperature')
        self.target_temp_char = thermostat_service.get_characteristic('TargetTemperature')
        self.current_heating_cooling_char = thermostat_service.get_characteristic('CurrentHeatingCoolingState')
        self.target_heating_cooling_char = thermostat_service.get_characteristic('TargetHeatingCoolingState')

        # Set initial temperature
        self.update_current_temperature()
        self.current_temp_char.getter_callback = self.update_current_temperature()

        self.target_temp_char.override_properties(properties={
            'minValue': 10.0,
            'maxValue': 30.0,
            'minStep': 0.5
        })

        self.target_temp_char.set_value(self.circuit["target_temperature"])

        # Set the callback for the TargetTemperature
        self.target_temp_char.setter_callback = self.set_target_temperature
        


    def update_current_temperature(self):
        # Get the current temperature from BMR and update the characteristic
        current_temp = self.circuit['temperature']
        self.current_temp_char.set_value(current_temp)
        self.current_heating_cooling_char.set_value(int(self.circuit["heating"]))
        self.target_heating_cooling_char.set_value(int(self.circuit["heating"]))


    def set_target_temperature(self, value):
        # Set the new temperature using BMR system
        self.bmr.setManualTemp(self.room_id, value)
        self.bmr.setManualTemp(self.room_id+10, value)
        print(f"Setting new target temperature: {value}°C for room {self.name}")