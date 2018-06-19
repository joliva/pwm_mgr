# PWM Manager

Provides access to Raspberry Pi GPIO servo PWM routers via REST API.

Runs as a Docker container on a Donkey Car and allows a custom version of the Donkey Car software to select whether the servo PWM signals driving the throttle and steering come from the neural network (autonomous mode) or from the R/C control receiver (regenerated through the RPI).
