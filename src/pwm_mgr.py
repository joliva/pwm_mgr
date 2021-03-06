import json
import os.path
import pigpio
from pwm_router import PwmRouter

CFG_FILE = '/root/config/pwmmgr.conf'

conf = {}
if not os.path.isfile(CFG_FILE):
    # Create dummy configuration file
    conf['throttle'] = {'gpio_in':17, 'gpio_out':22}
    conf['steering'] = {'gpio_in':18, 'gpio_out':23}
    confs = json.dumps(conf)

    with open(CFG_FILE, 'w') as f: f.write(confs)

with open(CFG_FILE) as f:
    conf = json.loads(f.read())

# IP address where pigpiod is exposed
IP_PIGPIOD = '172.17.0.1'  # docker host

class PwmMgr:
   """
   A class providing access to Raspberry Pi GPIO servo PWM routers via REST API 
   """

   ROUTER_THROTTLE = 'throttle'
   ROUTER_STEERING = 'steering'
   
   SOURCE_GPIO = 'gpio'
   SOURCE_CPU = 'cpu'
   
   def __init__(self):
      self._pi = pigpio.pi(IP_PIGPIOD)

      self.routers = [
          {
              'id': PwmMgr.ROUTER_THROTTLE,
          },
          {
              'id': PwmMgr.ROUTER_STEERING,
          }
      ]
      
      self.throttle = PwmRouter(self._pi, conf['throttle']['gpio_in'], conf['throttle']['gpio_out'])
      self.set_pwm_source(self.throttle, PwmMgr.SOURCE_GPIO)
      self.set_pulse_width(self.throttle, 1500)

      self.steering = PwmRouter(self._pi, conf['steering']['gpio_in'], conf['steering']['gpio_out'])
      self.set_pwm_source(self.steering, PwmMgr.SOURCE_GPIO)
      self.set_pulse_width(self.steering, 1500)

   def set_pwm_source(self, router, source):
      """
      Set source for output PWM pulse width
      """
      if router == self.throttle:
         mgr_router = self.routers[0]
      elif router == self.steering:
         mgr_router = self.routers[1]

      if source == PwmMgr.SOURCE_GPIO:
         router.set_pwm_source(PwmRouter.SRC_GPIO)
         mgr_router['source'] = source
      elif source == PwmMgr.SOURCE_CPU:
         router.set_pwm_source(PwmRouter.SRC_CPU)
         mgr_router['source'] = source
      else:
         return -1

   def get_pwm_source(self, router):
      """
      Returns current pwm source
      """
      source = router.get_pwm_source()

      if source == PwmRouter.GPIO:
         return PwmMgr.SOURCE_GPIO
      elif source == PwmRouter.CPU:
         return PwmMgr.SOURCE_CPU
      else:
         return -1

   def set_pulse_width(self, router, pulse_width_us):
      """
      Sets output pulse width. 
      """
      router.set_pulse_width(pulse_width_us)
      
      if router == self.throttle:
          self.routers[0]['pulse_width_usec'] = pulse_width_us
      elif router == self.steering:
          self.routers[1]['pulse_width_usec'] = pulse_width_us

      return pulse_width_us

   def get_pulse_width_out(self, router):
      """
      Returns current output pulse width.
      """
      return router.get_pulse_width_out()

   def get_pulse_width_in(self, router):
      """
      Returns current input pulse width.
      """
      return router.get_pulse_width_in()

