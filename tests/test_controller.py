from auroraarm.controller import PID
def test_voltage_saturation():
 c=PID()
 for _ in range(5): assert abs(c.step(100,0))<=48
def test_reset():
 c=PID(); c.step(1,0); c.reset(); assert c.integral==0 and c.prev_error==0
