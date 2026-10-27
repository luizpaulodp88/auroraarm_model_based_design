# Memorial de cálculo

## Dados e equações
R=0,8 Ω; L=1,2 mH; Kt=Ke=0,085; J=4,2×10⁻⁴ kg·m²; b=1,5×10⁻⁴ N·m·s/rad;
N=100; Vmax=48 V; Imax=8 A; Ts=2 ms; τL=0,25 N·m; ωmotor=450 rad/s.

Estados x=[i, ω, θ]ᵀ no eixo do motor. Equação elétrica: L di/dt=u−Ri−Keω.
Equação mecânica: J dω/dt=Kt i−bω−τL. Cinemática: dθ/dt=ω.
A=[[-R/L,-Ke/L,0],[Kt/J,-b/J,0],[0,1,0]], B=[[1/L],[0],[0]],
E=[[0],[-1/J],[0]], C=[[0,0,1]]. Implementação: `src/auroraarm/model.py`.

## Ponto de operação
Em regime permanente: i=(τL+bω)/Kt=(0,25+1,5×10⁻⁴×450)/0,085≈3,7353 A.
u=Ri+Keω=0,8×3,6765+0,085×450≈41,2382 V.
Folga nominal de tensão ≈6,7618 V; folga de corrente ≈4,2647 A. Os valores pressupõem
que o torque informado já é refletido no eixo modelado.

## Constantes de tempo e amostragem
τe=L/R=1,5 ms. Constante mecânica desacoplada aproximada τm=J/b=2,8 s.
A aproximação J/b ignora acoplamento eletromecânico; o código também calcula autovalores
da matriz A. Ts=2 ms dá 1,4 amostras por τe e cerca de 1400 por τm aproximado: a amostragem
fixada no enunciado é lenta em relação à constante elétrica, exigindo cautela na validação.

## Controlabilidade/observabilidade
O código constrói [B AB A²B] e [C; CA; CA²] e calcula os postos. Testes esperam posto 3
para ambas no modelo linear ideal; isso não inclui ruído, quantização ou falha de sensor.

## Prazo de segurança
Hipótese: atraso de sensor 20 ms + jitter/perda de ciclo 2 ms + fase de amostragem 2 ms = 24 ms.
A varredura verifica (21)(3)(3)=189 combinações inteiras; pior caso 24 ms, margem aritmética
76 ms em relação ao limite de 100 ms. Isso prova apenas o orçamento até emitir o comando
de torque zero sob essas hipóteses; não prova parada física nem conformidade normativa.

## Equivalência modelo-código
`python -m auroraarm.codegen` gera C automaticamente dos ganhos PID. `python -m auroraarm.sil`
compila com gcc/clang se disponível e compara uma sequência Python/C, reportando erro absoluto
máximo. A tolerância de teste é 1e-4 por comparação float64/float32; não se afirma igualdade
bit a bit nem que isso substitua qualificação de ferramenta.
