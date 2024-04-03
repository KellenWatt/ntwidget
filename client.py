import ntcore
import time

if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable("SmartDashboard")
    topic = table.getDoubleTopic("throttle")
    xSub = topic.subscribe(0)
    print(topic.getName())

    def throttle_listener(evt):
        print(f"throttle changed! ({evt.data.value.getDouble()})")

    valueListenerHandle = inst.addListener(
        xSub, ntcore.EventFlags.kValueAll, throttle_listener
    )


    inst.startClient4("example client")
    inst.setServer("10.21.65.2")
    #  inst.setServerTeam(2165) # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
    #  inst.startDSClient() # recommended if running on DS computer; this gets the robot IP from the DS

    while True:
        time.sleep(1000)

        #  x = xSub.get()
        #  print(f"throttle: {x}")

