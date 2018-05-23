import pigpio
from pwm_reader import PwmReader

class PwmRouter:
   """
   A class providing the ability to mirror the pulse width from a GPIO input 
   to a different GPIO output or to accept a manual setting of pulse width 
   for output to the GPIO output.
   """
   SRC_GPIO = 0
   SRC_CPU = 1

   def __init__(self, pi, gpio_in, gpio_out):
      """
      Instantiate with the pigpio pi, GPIO input and GPIO output for PWM 
      mirroring.
      """
      self._pi = pi
      self._gpio_in = gpio_in
      self._gpio_out = gpio_out
      self._source = PwmRouter.SRC_GPIO
      self._pulse_width_in_us = 1500
      self._pulse_width_out_us = 1500
      self._pwm_reader = PwmReader(pi, gpio_in, 0, self._cbf)

      pi.set_mode(gpio_out, pigpio.OUTPUT)
      pi.set_servo_pulsewidth(gpio_out, 0)

   def _cbf(self, pulse_width_us):
      """
      Callback function called with the GPIO input pulse width changes.
      """
      self._pulse_width_in_us = pulse_width_in_us

      if self._source == PwmRouter.GPIO:
         self._pulse_width_out_us = pulse_width_us
         self._pi.set_servo_pulsewidth(self._gpio_out, pulse_width_us)

   def set_pwm_source(self, source):
      """
      Set source for output PWM pulse width
      """
      if source == PwmRouter.SRC_GPIO or source == PwmRouter.SRC_CPU:
         self._source = source
         return source
      else:
         return -1

   def get_pwm_source(self):
      """
      Returns current pwm source
      """
      return self._source

   def set_pulse_width(self, pulse_width_us):
      """
      Sets output pulse width. Only effective when source is CPU.
      """
      pulse_width_us = round(pulse_width_us)
      if pulse_width_us >= 0 and pulse_width_us <= 2500:
         self._pulse_width_out_us = pulse_width_us

         if self._source == PwmRouter.SRC_CPU:
            self._pi.set_servo_pulsewidth(self._gpio_out, pulse_width_us)

         return pulse_width_us
      else:
         return -1

   def get_pulse_width_out(self):
      """
      Returns current output pulse width.
      """
      return self._pulse_width_out_us

   def get_pulse_width_in(self):
      """
      Returns current input pulse width.
      """
      return self._pulse_width_in_us

