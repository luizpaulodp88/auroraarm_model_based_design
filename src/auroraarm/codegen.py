"""Gera C a partir dos ganhos do controlador Python."""
from pathlib import Path
from .controller import PID
def generate(path=None):
    p=PID()
    path=Path(path) if path else Path(__file__).resolve().parents[2]/"generated"/"auroraarm_controller.c"
    # Valores interpolados a partir da configuração PID acima.
    source=("""/* AUTO-GERADO por src/auroraarm/codegen.py; não editar.
 * Rastreabilidade: REQ-CTRL-AA-001..004; teste SIL em src/auroraarm/sil.py.
 * Protótipo acadêmico, não certificado para hardware real.
 */
#include <math.h>
#define TS %.9gf
#define VMAX %.9gf
#define KP %.9gf
#define KI %.9gf
#define KD %.9gf
#define ILIM %.9gf
typedef struct { float integral; float prev_error; } aa_pid_state;
void aa_pid_reset(aa_pid_state *s) { if(s){s->integral=0.0f;s->prev_error=0.0f;} }
float aa_pid_step(aa_pid_state *s,float reference,float position) {
 if(!s) return 0.0f;
 float e=reference-position, de=(e-s->prev_error)/TS;
 float ip=s->integral+e*TS;
 if(ip>ILIM) ip=ILIM; if(ip< -ILIM) ip= -ILIM;
 float raw=KP*e+KI*ip+KD*de, u=raw;
 if(u>VMAX)u=VMAX; if(u< -VMAX)u= -VMAX;
 if(raw==u || (raw>VMAX && e<0.0f) || (raw< -VMAX && e>0.0f)) s->integral=ip;
 s->prev_error=e; return u;
}
""" % (p.ts,p.v_limit,p.kp,p.ki,p.kd,p.integral_limit))
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(source,encoding="utf-8")
    return path
if __name__=="__main__": print(generate())
