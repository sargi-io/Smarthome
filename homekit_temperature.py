from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_THERMOSTAT
from bmr import Bmr
from dotenv import load_dotenv

from rooms import BedroomThermostat, EntranceThermostat, GymThermostat, KitchenAndDinnerThermostat, LivingRoomThermostat, MainBathroomThermostat, SmallBahtroomThermostat, StudyAdeleThermostat, StudyMojmirThermostat, TopBathroomThermostat
                
import logging
import os


# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Load environment variables from the .env file
    load_dotenv() 
    bmr_username = os.getenv("BMR_USERNAME")
    bmr_password = os.getenv("BMR_PASSWORD")

     # Specify a directory where accessory.state can be stored
    persist_dir = os.path.join(os.getcwd(), 'persist')
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)

    # Specify the path for the accessory.state file
    persist_file = os.path.join(persist_dir, 'accessory.state')
    
    # Connect to the BMR heating controller using pybmr
    bmr = Bmr("http://192.168.68.109/", bmr_username, bmr_password)

    # Get the number of rooms (circuits) from the BMR system
    num_rooms = bmr.getNumCircuits()

    # Set up the HomeKit accessory driver
    driver = AccessoryDriver(port=51826, persist_file=persist_file)
    def get_bridge(driver):
        bridge = Bridge(driver, "Bridge")
        # Add each accessory individually
        bridge.add_accessory(BedroomThermostat(bmr, driver, f"Bedroom"))
        bridge.add_accessory(EntranceThermostat(bmr, driver, f"Entrance"))
        bridge.add_accessory(GymThermostat(bmr, driver, f"Gym"))
        bridge.add_accessory(KitchenAndDinnerThermostat(bmr, driver, f"Kitchen and dinner"))
        bridge.add_accessory(LivingRoomThermostat(bmr, driver, f"Living room"))
        bridge.add_accessory(MainBathroomThermostat(bmr, driver, f"Main bathroom"))
        bridge.add_accessory(SmallBahtroomThermostat(bmr, driver, f"Small bathroom"))
        bridge.add_accessory(StudyAdeleThermostat(bmr, driver, f"Adeles study"))
        bridge.add_accessory(StudyMojmirThermostat(bmr, driver, f"Mojmir study"))
        bridge.add_accessory(TopBathroomThermostat(bmr, driver, f"Top bathroom"))
                             
        return bridge



    # Start the HomeKit driver to make the sensors available to Home app
    driver.add_accessory(accessory=get_bridge(driver))
    driver.start()

if __name__ == '__main__':
    main()
