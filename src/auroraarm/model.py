"""Modelo da planta no eixo do motor: estados [corrente, velocidade, posição]."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Params:
    R: float=0.8; L: float=1.2e-3; Kt: float=0.085; Ke: float=0.085
    J: float=4.2e-4; b: float=1.5e-4; N: float=100.0
    Vmax: float=48.0; Imax: float=8.0; Ts: float=0.002; tau_load: float=0.25
P=Params()

def state_space(p=P):
    A=np.array([[-p.R/p.L,-p.Ke/p.L,0.0],[p.Kt/p.J,-p.b/p.J,0.0],[0.0,1.0,0.0]])
    B=np.array([[1/p.L],[0.0],[0.0]])
    C=np.array([[0.0,0.0,1.0]])
    E=np.array([[0.0],[-1/p.J],[0.0]])
    return A,B,C,E

def operating_point(omega=450.0,p=P):
    i=(p.tau_load+p.b*omega)/p.Kt
    v=p.R*i+p.Ke*omega
    return {"current_A":i,"voltage_V":v,"voltage_margin_V":p.Vmax-v,
            "current_margin_A":p.Imax-i,"feasible_voltage":abs(v)<=p.Vmax,
            "feasible_current":abs(i)<=p.Imax}

def time_constants(p=P):
    A,*_=state_space(p)
    return {"tau_e_s":p.L/p.R,"tau_m_approx_s":p.J/p.b,
            "eigenvalues_per_s":np.linalg.eigvals(A)}

def controllability_observability(p=P):
    A,B,C,_=state_space(p)
    ctrb=np.hstack([np.linalg.matrix_power(A,k)@B for k in range(3)])
    obsv=np.vstack([C@np.linalg.matrix_power(A,k) for k in range(3)])
    return {"controllability_rank":int(np.linalg.matrix_rank(ctrb)),
            "observability_rank":int(np.linalg.matrix_rank(obsv))}

def derivative(x,u,tau=0.0,p=P):
    A,B,_,E=state_space(p); u=float(np.clip(u,-p.Vmax,p.Vmax))
    return A@np.asarray(x,float)+B[:,0]*u+E[:,0]*tau
