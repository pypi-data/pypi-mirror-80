from playment.base.sensors.frame import Frame
from playment.base.sensors.sensor import Sensor
from typing import List


class SensorFusionData:
    def __init__(self, frames: List[Frame] = None, sensor: List[Sensor] = None):
        self.frames = frames
        self.sensor_meta = sensor

    def add_sensor(self, sensor: Sensor):
        if self.sensor_meta is None:
            self.sensor_meta = []
        self.sensor_meta.append(sensor)

    def add_frame(self, frame: Frame):
        if self.frames is None:
            self.frames = []
        self.frames.append(frame)
