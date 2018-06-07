"""
Encapsulates command and coordination for the water-regulation module
"""

class Controller(object):
    """
    Encapsulates command and coordination for the water-regulation module
    """

    def __init__(self, sensor, pump, decider):
        """
        Create a new controller

        :param sensor: Typically an instance of sensor.Sensor
        :param pump: Typically an instance of pump.Pump
        :param decider: Typically an instance of decider.Decider
        """

        self.sensor = sensor
        self.pump = pump
        self.decider = decider

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def tick(self):
        """
        On each call to tick, the controller shall:

          1. query the sensor for the current height of liquid in the tank
          2. query the pump for its current state (pumping in, pumping out, or at rest)
          3. query the decider for the next appropriate state of the pump, given the above
          4. set the pump to that new state

        :return: True if the pump has acknowledged its new state, else False
        """

        # TODO: Implement the above-defined behaviors
        # 1. query the sensor for the current height of liquid in the tank
        current_height = self.sensor.measure()

        # 2. query the pump for its current state (pumping in, pumping out, or at rest)
        current_action = self.pump.get_state()

        # 3. query the decider for the next appropriate state of the pump, given the above
        new_pump_state = self.decider.decide(current_height, current_action, self.actions)

        # 4. set the pump to that new state
        self.pump.set_state(new_pump_state)

        return new_pump_state == self.pump.get_state()
