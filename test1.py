from dronekit import VehicleMode, connect

vehicle = connect("/dev/ttyACM0", wait_ready=True)


print("Testing")
print("Armed: %s" %vehicle.armed)
print("Mode: %s" %vehicle.mode)
print("Is Armable: %s" %vehicle.is_armable)