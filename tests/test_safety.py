from auroraarm.safety import exhaustive_deadline,Supervisor,graph_coverage
def test_deadline():
 r=exhaustive_deadline(); assert r["combinations"]==189 and r["all_pass"] and r["worst_case_ms"]==24
def test_rearm():
 s=Supervisor(); assert s.event("human_detected")=="PROTECTIVE_STOP"; s.event("torque_zero_confirmed")
 assert s.state=="WAIT_RESET" and not s.may_resume(False,True) and s.may_resume(True,True)
def test_coverage():
 r=graph_coverage(); assert r["state_coverage"]==1 and r["transition_coverage"]==1
