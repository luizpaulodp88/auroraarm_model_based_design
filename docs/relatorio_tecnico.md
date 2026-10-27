# Relatório técnico — Operação Linha Viva: AuroraArm

## Resumo
O pacote acadêmico demonstra fluxo de modelagem, controle, supervisão de segurança, análise
temporal, geração C e testes para a junta do cotovelo AuroraArm.

## 1. Problema
O enunciado descreve um quase-acidente por torque não zerado a tempo após aproximação humana.
O objetivo é produzir artefatos reprodutíveis e rastreáveis, evitando depender exclusivamente
de firmware manual sem verificação.

## 2. Planta
O modelo usa corrente, velocidade e posição do eixo do motor. A equação elétrica considera
resistência, indutância e força contraeletromotriz; a equação mecânica considera torque do motor,
atrito e carga. A saída da transmissão 100:1 é a posição/velocidade do motor dividida por 100.

## 3. Controle
Foi implementado PID discreto com Ts=2 ms, saturação de tensão ±48 V e anti-windup condicional.
A limitação de tensão não garante limitar corrente a 8 A em todos os transitórios: uma solução
industrial requer limite de corrente no drive e proteção independente. Ganhos são iniciais.
Sobressinal ≤8%, acomodação ≤300 ms e erro estacionário nulo devem ser comprovados por simulação
de malha fechada e cenários de carga antes de afirmar atendimento.

## 4. Requisitos e verificação
REQ-CTRL-AA-001 erro estacionário nulo: desempenho. REQ-CTRL-AA-002 sobressinal ≤8%: desempenho.
REQ-CTRL-AA-003 acomodação ≤300 ms: desempenho. REQ-CTRL-AA-004 tensão ≤48 V e corrente ≤8 A:
limite de atuação. REQ-SAFE-AA-001 torque zero em até 100 ms: segurança, pois evita exceder prazo.
REQ-SAFE-AA-002 não retomar sem rearme: segurança. REQ-SAFE-AA-003 retomar após área livre e
rearme: vivacidade condicionada à revalidação. REQ-SAFE-AA-004 velocidade linear ≤250 mm/s:
segurança. O supervisor tem quatro estados e requer rearme explícito. A varredura temporal
cobre 189 combinações e calcula pior caso de 24 ms com as hipóteses declaradas.

## 5. Código gerado e SIL
O gerador produz C por template a partir dos ganhos do módulo Python e inclui rastreabilidade.
O teste SIL compila o C e compara saídas, se gcc/clang estiver instalado. Isso é demonstração
acadêmica, não ferramenta de geração qualificada.

## 6. Rastreabilidade
A matriz está em `docs/rastreabilidade.csv`, relacionando os oito requisitos a modelo, código,
teste e evidência esperada.

## 7. Conclusão e limites
O pacote demonstra método e evidências de software, mas não libera um robô real para operação.
Faltam análise de risco da célula, validação de sensores/atuadores reais, medição de força/pressão,
parada física, análise de falhas, verificação independente e processo formal de conformidade.
ISO/TS 15066 não equivale a um limite universal de velocidade; a aplicação depende do cenário e
da análise de risco.
