/* AUTO-GERADO por src/auroraarm/codegen.py; não editar.
 * Rastreabilidade: REQ-CTRL-AA-001..004; teste SIL em src/auroraarm/sil.py.
 * Protótipo acadêmico, não certificado para hardware real.
 */
#include <math.h>
#define TS 0.002f
#define VMAX 48f
#define KP 120f
#define KI 8f
#define KD 2f
#define ILIM 5f
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
