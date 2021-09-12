from controller import Controller
from ox_signal import OxSignal

# https://en.wikipedia.org/wiki/Observer_pattern#Python

controller = Controller()
ox1_signal = OxSignal(controller, 1, 2)

controller.notify(ox1_freq=3, ox1_duty=0.1)
