import pigpio

class PwmReader:
   """
   A class to read PWM pulses and calculate their frequency
   and duty cycle.  The frequency is how often the pulse
   happens per second.  The duty cycle is the percentage of
   pulse high time per cycle.
   """

   # class variables
   gpio_to_obj = {} 	# GPIO to PwmReader object map

   def __init__(self, pi, gpio, weighting=0.0, callback_obj=None):
      """
      Instantiate with the Pi and gpio of the PWM signal
      to monitor.

      A callback is made if the callback has been set and 
      the pulse width changes.

      Optionally a weighting may be specified.  This is a number
      between 0 and 1 and indicates how much the old reading
      affects the new reading.  It defaults to 0 which means
      the old reading has no effect.  This may be used to
      smooth the data.
      """
      self.pi = pi
      self.gpio = gpio
      self.callback_obj = callback_obj
      if weighting < 0.0:
         weighting = 0.0
      elif weighting > 0.99:
         weighting = 0.99

      self._new = 1.0 - weighting # Weighting for new reading.
      self._old = weighting       # Weighting for old reading.

      self._high_tick = None
      self._period = None
      self._high = None
      self._high_prev = None
      self._refresh_cnt = 0

      pi.set_mode(gpio, pigpio.INPUT)

      # add object to gpio_to_obj map if new gpio 
      if gpio not in PwmReader.gpio_to_obj:
          PwmReader.gpio_to_obj[gpio] = self

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, PwmReader._cb_redirect)

   @classmethod
   def _cb_redirect(cls, gpio, level, tick):
      if gpio in PwmReader.gpio_to_obj:
          PwmReader.gpio_to_obj[gpio]._cbf(gpio, level, tick)

   def _cbf(self, gpio, level, tick):

      if level == 1:

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)

            if self._period is not None:
               self._period = (self._old * self._period) + (self._new * t)
            else:
               self._period = t

         self._high_tick = tick

      elif level == 0:

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)

            if self._high is not None:
               self._high = (self._old * self._high) + (self._new * t)
            else:
               self._high = t

            if self._high != self._high_prev:
                self._high_prev = self._high
                if self.callback_obj:
                    self.callback_obj.cbf(self._high)

   def frequency(self):
      """
      Returns the PWM frequency.
      """
      if self._period is not None:
         return 1000000.0 / self._period
      else:
         return 0.0

   def pulse_width(self):
      """
      Returns the PWM pulse width in microseconds.
      """
      if self._high is not None:
         return self._high
      else:
         return 0.0

   def duty_cycle(self):
      """
      Returns the PWM duty cycle percentage.
      """
      if self._high is not None:
         return 100.0 * self._high / self._period
      else:
         return 0.0

   def cancel(self):
      """
      Cancels the reader and releases resources.
      """
      self._cb.cancel()

