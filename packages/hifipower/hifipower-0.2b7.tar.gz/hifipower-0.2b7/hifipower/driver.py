# -*- coding: utf-8 -*-
"""hardware control backend for hifipower.
Can be used with Orange Pi (the original device is based on OPi Plus,
as it has gigabit Ethernet port and SATA controller),
or a regular Raspberry Pi"""
import atexit
import os
import time
from contextlib import suppress

try:
    # use SUNXI as it gives the most predictable results
    import OPi.GPIO as GPIO
    GPIO.setmode(GPIO.SUNXI)
    GPIO_DEFINITIONS = dict(onoff_button='PA7', mode_led='PC4',
                            relay_out='PC7', auto_mode_in='PA8',
                            shutdown_button='PA9', reboot_button='PA10',
                            relay_state='PA11', ready_led='PA12')
    print('Using OPi.GPIO on an Orange Pi with the SUNXI numbering.')

except ImportError:
    # maybe we're using Raspberry Pi?
    # use BCM as it is the most conventional scheme here
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO_DEFINITIONS = dict(onoff_button=5, mode_led=23,
                            relay_out=24, auto_mode_in=6,
                            shutdown_button=13, reboot_button=19,
                            relay_state=3, ready_led=2)
    print('Using RPi.GPIO on a Raspberry Pi with the BCM numbering.')

ON, OFF = GPIO.HIGH, GPIO.LOW
STATE = dict(relay=OFF, auto_mode=OFF)


class AutoControlDisabled(Exception):
    """Exception raised when trying to turn the device on or off
    if the equipment is switched OFF or ON manually.
    """


def gpio_setup(config):
    """Reads the gpio definitions dictionary,
    sets the outputs and inputs accordingly."""
    def shutdown(*_):
        """Shut the system down"""
        led('mode_led', OFF, blink=2)
        command = config.get('shutdown_command', 'sudo shutdown -h now')
        os.system(command)

    def reboot(*_):
        """Restart the system"""
        led('mode_led', OFF, blink=2)
        command = config.get('reboot_command', 'sudo reboot')
        os.system(command)

    def toggle_relay_state(*_):
        """Turn the power on or off after pressing the on/off button,
        depending on the previous state"""
        led('mode_led', blink=2)
        relay(not STATE['relay'])

    def update_relay_state(*_):
        """Read the relay control input whenever its state changes
        and update the state dict. This enables the function to work
        even in a forced manual control mode."""
        STATE['relay'] = check_state('relay_state')

    def check_auto_mode(*_):
        """When the automatic control mode is on, turn on the red LED,
        when it's off, turn the LED off. Update the state dictionary."""
        auto_mode = check_state('auto_mode_in')
        STATE['auto_mode'] = auto_mode
        led('mode_led', auto_mode)

    def finish(*_):
        """Blink a LED and then clean the GPIO"""
        led('ready_led', OFF, blink=5)
        GPIO.cleanup()

    def get_gpio_id(gpio_name):
        """Gets the GPIO id (e.g. "PA7") from the configuration,
        updating the id in GPIO_DEFINITIONS if overriden in config.
        If the GPIO name is not found in config, it's looked up
        in GPIO_DEFINITIONS.
        """
        gpio_id = config.get(gpio_name)
        if gpio_id is None:
            gpio_id = GPIO_DEFINITIONS[gpio_name]
        else:
            # update definitions with the value found in config
            GPIO_DEFINITIONS[gpio_name] = gpio_id

    inputs = [('onoff_button', toggle_relay_state, GPIO.RISING),
              ('auto_mode_in', check_auto_mode, GPIO.BOTH),
              ('relay_state', update_relay_state, GPIO.BOTH),
              ('shutdown_button', shutdown, GPIO.RISING),
              ('reboot_button', reboot, GPIO.RISING)]

    outputs = [('mode_led', check_state('auto_mode_in')),
               ('relay_out', OFF), ('ready_led', ON)]

    for (gpio_name, callback, edge) in inputs:
        gpio_id = get_gpio_id(gpio_name)
        # set the input with pulldown resistor, if supported by GPIO library
        GPIO.setup(gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # add a threaded callback on this GPIO
        GPIO.add_event_detect(gpio_id, edge, callback=callback, bouncetime=200)

    for (gpio_name, initial_state) in outputs:
        gpio_id = get_gpio_id(gpio_name)
        GPIO.setup(gpio_id, GPIO.OUT, initial=initial_state)

    atexit.register(finish)


def check_state(gpio_name):
    """Checks the output state"""
    channel = GPIO_DEFINITIONS[gpio_name]
    return GPIO.input(channel)


def relay(state):
    """Controls the state of the power relay"""
    if not STATE('auto_mode'):
        raise AutoControlDisabled
    channel = GPIO_DEFINITIONS['relay_out']
    GPIO.output(channel, state)


def led(gpio_name, state=None, blink=0, duration=0.5):
    """LED control:
        state - 0/1, True/False - sets the new state;
                None preserves the previous one
        blink - number of LED blinks before the state is set
        duration - total time of blinking in seconds"""
    channel = GPIO_DEFINITIONS[gpio_name]
    # preserve the previous state in case it is None
    if state is None:
        state = check_state(gpio_name)
    # each blink cycle has 2 timesteps,
    # how long they are depends on the number of cycles and blinking duration
    timestep = 0.5 * duration / (blink or 1)
    # blinking a number of times
    for _ in range(blink):
        GPIO.output(channel, ON)
        time.sleep(timestep)
        GPIO.output(channel, OFF)
        time.sleep(timestep)
    # final state
    GPIO.output(channel, state)
