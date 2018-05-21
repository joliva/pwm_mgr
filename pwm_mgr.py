import time
import pigpio

class PwmMgr:
   """
   A class providing access to Raspberry Pi GPIO servo PWM routers via REST API 
   """
   ROUTER_THROTTLE = 0
   ROUTER_STEERING = 1

   def __init__(self):
      self._pwm_reader = PwmReader(pi, gpio_in, 0, _cbf)

      pi.set_mode(gpio_out, pigpio.OUTPUT)
      pi.set_servo_pulsewidth(gpio_out, 0)

   def set_pwm_source(self, source):
      """
      Set source for output PWM pulse width
      """
      if source == PwmRouter.GPIO or source == PwmRouter.CPU:
         self._source = source
         return source
      else:
         return -1

   def set_pulse_width(self, pulse_width_us):
      """
      Sets output pulse width. Only effective when source is CPU.
      """
      pulse_width_us = round(pulse_width_us)
      if pulse_width_us >= 0 and pulse_width_us <= 2500
         self._pulse_width_out_us = pulse_width_us

         if self._source = PwmRouter.CPU:
            self._pi.set_servo_pulsewidth(self._gpio_out, pulse_width_us)

         return pulse_width_us
      else:
         return -1

   def set_pulse_width(self, pulse_width_us):
      """
      Sets output pulse width. Only effective when source is CPU.
      """
      pulse_width_us = round(pulse_width_us)
      if pulse_width_us >= 0 and pulse_width_us <= 2500
         self._pulse_width_out_us = pulse_width_us

         if self._source = PwmRouter.CPU:
            self._pi.set_servo_pulsewidth(self._gpio_out, pulse_width_us)

         return pulse_width_us
      else:
         return -1

if __name__ == "__main__":

   import time
   import pigpio
   import read_PWM

   PWM_GPIO = 4
   RUN_TIME = 600000.0
   SAMPLE_TIME = 1 

   SERVO_GPIO = 22

   pi = pigpio.pi()

   p = read_PWM.reader(pi, PWM_GPIO)

   pi.set_PWM_range(PWM_GPIO, 1023)
   #pi.set_PWM_range(PWMC_GPIO, 1023)

   start = time.time()

   while (time.time() - start) < RUN_TIME:

      #time.sleep(SAMPLE_TIME)

      f = p.frequency()
      pw = p.pulse_width()
      dc = p.duty_cycle()
     
      #print("f={:.1f} pw={} dc={:.2f}".format(f, int(pw+0.5), dc))

      #pi.set_PWM_dutycycle(PWMC_GPIO, dc*1023/100)
      pi.set_servo_pulsewidth(SERVO_GPIO, pw)

   p.cancel()

   pi.stop()

