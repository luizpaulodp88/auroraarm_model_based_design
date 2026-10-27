from auroraarm.model import state_space,operating_point,time_constants,controllability_observability
def test_shapes():
 A,B,C,E=state_space(); assert A.shape==(3,3) and B.shape==(3,1) and C.shape==(1,3) and E.shape==(3,1)
def test_operating_point():
 r=operating_point(); assert abs(r["current_A"]-3.735294118)<1e-6
 assert abs(r["voltage_V"]-41.23823529)<1e-5
def test_ranks():
 r=controllability_observability(); assert r["controllability_rank"]==3 and r["observability_rank"]==3
def test_electrical_tau(): assert abs(time_constants()["tau_e_s"]-.0015)<1e-12
