"""PID discreto com saturação de tensão e anti-windup condicional."""
from dataclasses import dataclass
from .model import P
@dataclass
class PID:
    kp:float=120.0; ki:float=8.0; kd:float=2.0; ts:float=P.Ts
    v_limit:float=P.Vmax; integral_limit:float=5.0
    integral:float=0.0; prev_error:float=0.0
    def reset(self):
        self.integral=0.0; self.prev_error=0.0
    def step(self,reference,position):
        e=float(reference-position); de=(e-self.prev_error)/self.ts
        ip=max(-self.integral_limit,min(self.integral_limit,self.integral+e*self.ts))
        raw=self.kp*e+self.ki*ip+self.kd*de
        u=max(-self.v_limit,min(self.v_limit,raw))
        if raw==u or (raw>self.v_limit and e<0) or (raw< -self.v_limit and e>0):
            self.integral=ip
        self.prev_error=e
        return u
