# AuroraArm — Model-Based Design for Cyber-Physical Systems

## 1. Sobre o projeto

O **AuroraArm** é um projeto acadêmico desenvolvido para demonstrar conceitos de *Model-Based Design* aplicados a sistemas ciberfísicos.

O projeto inclui:

- Modelagem matemática do sistema.
- Lógica de controle.
- Verificações de condições de segurança representadas no modelo.
- Geração de código C.
- Testes automatizados em Python.
- Simulação Software-in-the-Loop (SIL).
- Documentação técnica e rastreabilidade.

Este README explica como preparar o ambiente, executar o projeto e resolver os erros mais comuns no Windows utilizando o Visual Studio Code.

> **Aviso de segurança:** este projeto é exclusivamente acadêmico. Os resultados dos testes não certificam a segurança de um equipamento físico. Não conecte o código a um braço robótico real sem validação técnica, análise de riscos e implementação das proteções necessárias.

---

## 2. Requisitos para executar o projeto

Antes de começar, verifique se você possui os seguintes programas:

| Programa | Finalidade |
|---|---|
| Python 3.10 ou superior | Executar o código Python |
| Visual Studio Code | Editar os arquivos e utilizar o terminal |
| pip | Instalar bibliotecas Python |
| GCC ou outro compilador C compatível | Necessário para a etapa SIL, conforme a implementação |

### 2.1. Verificar se o Python está instalado

Abra o Visual Studio Code e selecione:

**Terminal → New Terminal**

No terminal, digite:

```powershell
python --version
```

Pressione Enter.

Se aparecer algo semelhante a:

```text
Python 3.12.5
```

o Python está instalado. A versão exibida no seu computador pode ser diferente.

Se aparecer uma mensagem dizendo que `python` não é reconhecido, instale o Python pelo site oficial:

https://www.python.org/downloads/windows/

Durante a instalação, marque a opção **Add Python to PATH**. Depois, feche e abra novamente o VS Code.

---

## 3. Abrir a pasta correta do projeto

Esta etapa é importante para evitar erros ao executar os comandos.

1. Abra o Visual Studio Code.
2. Clique em **File → Open Folder...**.
3. Localize a pasta extraída do projeto.
4. Selecione a pasta principal `auroraarm_model_based_design`.
5. Clique em **Selecionar pasta**.
6. No menu superior, clique em **Terminal → New Terminal**.

O terminal deve estar aberto na pasta principal do projeto.

A estrutura deve ser semelhante a esta:

```text
auroraarm_model_based_design/
├── src/
│   └── auroraarm/
├── generated/
├── tests/
├── docs/
├── requirements.txt
├── pyproject.toml
└── README.md
```

Se o terminal estiver em outra pasta, os comandos seguintes podem falhar.

Para verificar a pasta atual no PowerShell, execute:

```powershell
Get-Location
```

Para verificar se o arquivo de dependências existe, execute:

```powershell
Test-Path requirements.txt
```

O resultado esperado é:

```text
True
```

Se aparecer `False`, confira se você abriu a pasta correta.

---

## 4. Criar o ambiente virtual Python

O ambiente virtual mantém as bibliotecas deste projeto separadas de outros projetos Python do computador.

### 4.1. Criar o ambiente

No terminal, execute:

```powershell
python -m venv .venv
```

Aguarde o comando terminar.

Esse comando cria uma pasta chamada `.venv` na raiz do projeto. Normalmente, ela só precisa ser criada uma vez.

### 4.2. Ativar o ambiente virtual

Execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando a ativação funcionar, o terminal deverá mostrar `(.venv)` antes do caminho da pasta.

Por exemplo:

```text
(.venv) PS C:\Users\Usuario\...\auroraarm_model_based_design>
```

Isso indica que o ambiente virtual está ativo.

### 4.3. Se o PowerShell bloquear a ativação

Se aparecer uma mensagem sobre política de execução, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois, tente ativar novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Essa configuração se aplica somente ao processo atual do PowerShell.

---

## 5. Instalar as dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias.

Primeiro, atualize o instalador de pacotes:

```powershell
python -m pip install --upgrade pip
```

Depois, instale as dependências listadas no projeto:

```powershell
python -m pip install -r requirements.txt
```

Aguarde a conclusão da instalação.

### 5.1. Se o pytest não for encontrado

Se aparecer:

```text
No module named pytest
```

instale o pytest:

```powershell
python -m pip install pytest
```

O pytest é a ferramenta utilizada para executar os testes automatizados do projeto.

---

## 6. Configurar o caminho do código Python

O código do AuroraArm fica dentro da pasta `src`. Por isso, precisamos informar ao Python onde encontrar o pacote `auroraarm`.

No terminal PowerShell, na pasta principal do projeto, execute:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Esse comando configura a variável de ambiente `PYTHONPATH` para o terminal atual.

**Importante:** se você fechar o terminal e abrir outro, precisará executar esse comando novamente.

### Por que essa configuração é necessária?

Quando você executa um módulo como:

```powershell
python -m auroraarm.codegen
```

o Python precisa localizar o pacote `auroraarm`. Como ele está dentro de `src`, configuramos o caminho para que o interpretador encontre os arquivos.

---

## 7. Executar o projeto passo a passo

Agora que o ambiente está preparado, podemos executar as diferentes partes do AuroraArm.

Execute cada comando separadamente e aguarde o resultado antes de passar para o próximo.

### Etapa 1 — Gerar o código C do controlador

Execute:

```powershell
python -m auroraarm.codegen
```

Esse módulo é responsável pela geração do código C do controlador.

O código gerado deve estar associado ao arquivo:

```text
generated/auroraarm_controller.c
```

Confira a mensagem exibida pelo programa e verifique se o arquivo foi criado ou atualizado.

### Etapa 2 — Executar os testes automatizados

Execute:

```powershell
python -m pytest
```

O pytest procurará os testes do projeto e tentará executá-los.

Na versão inicial do projeto, o resultado esperado é semelhante a:

```text
9 passed
```

Isso significa que nove testes foram aprovados.

Se algum teste falhar, leia a mensagem exibida no terminal. Um teste aprovado não comprova, sozinho, a segurança de um robô real.

### Etapa 3 — Executar as verificações de segurança modeladas

Execute:

```powershell
python -m auroraarm.safety
```

Esse módulo executa as verificações representadas no modelo acadêmico.

Observe os resultados e eventuais mensagens de erro.

**Atenção:** essas verificações não equivalem a certificação industrial nem comprovam o comportamento seguro de um equipamento físico.

### Etapa 4 — Executar a simulação SIL

SIL significa *Software-in-the-Loop*. Essa etapa permite testar software com apoio de uma simulação ou execução controlada, conforme a implementação do projeto.

Execute:

```powershell
python -m auroraarm.sil
```

Dependendo da implementação, essa etapa pode precisar de um compilador C instalado e disponível no terminal.

Se o programa informar que a simulação foi ignorada porque não encontrou um compilador, será necessário instalar e configurar um compilador compatível, como GCC.

---

## 8. Todos os comandos em sequência

Depois de abrir a pasta principal do projeto, siga esta sequência no PowerShell.

### Primeira execução

Use estes comandos quando ainda precisar criar o ambiente virtual:

**1. Criar o ambiente:**

```powershell
python -m venv .venv
```

**2. Ativar o ambiente:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Instalar as dependências:**

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**4. Configurar o caminho do código:**

```powershell
$env:PYTHONPATH = "$PWD\src"
```

**5. Gerar o código C:**

```powershell
python -m auroraarm.codegen
```

**6. Executar os testes:**

```powershell
python -m pytest
```

**7. Executar as verificações modeladas:**

```powershell
python -m auroraarm.safety
```

**8. Executar a simulação SIL:**

```powershell
python -m auroraarm.sil
```

Não é necessário executar tudo de uma vez. É recomendável executar um comando por vez para identificar facilmente qualquer erro.

### Nas próximas vezes

Se o ambiente `.venv` já existir, você não precisa criá-lo novamente.

Abra o projeto no VS Code e execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Depois:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Agora você pode executar o módulo desejado.

---

## 9. Entendendo os arquivos principais

| Arquivo ou pasta | Função |
|---|---|
| `src/auroraarm/model.py` | Contém o modelo do sistema |
| `src/auroraarm/controller.py` | Contém a lógica do controlador |
| `src/auroraarm/safety.py` | Implementa verificações de segurança modeladas |
| `src/auroraarm/codegen.py` | Responsável pela geração de código C |
| `src/auroraarm/sil.py` | Contém a execução da etapa SIL |
| `generated/` | Guarda código gerado |
| `tests/` | Contém os testes automatizados |
| `docs/` | Guarda a documentação técnica |
| `requirements.txt` | Lista as dependências Python |
| `pyproject.toml` | Contém configurações do projeto Python |

A função exata de cada arquivo deve ser confirmada no respectivo código-fonte.

---

## 10. Solução de problemas

### Erro: `No module named auroraarm`

**Possível causa:** o Python não encontrou o pacote dentro de `src`.

**Solução:** confirme que o terminal está na pasta principal do projeto e execute:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Depois, tente novamente:

```powershell
python -m auroraarm.codegen
```

### Erro: `No module named pytest`

**Possível causa:** o pytest não está instalado no ambiente virtual ativo.

**Solução:**

```powershell
python -m pip install pytest
```

Em seguida:

```powershell
python -m pytest
```

### Erro: `requirements.txt` não foi encontrado

**Possível causa:** o terminal está aberto em uma pasta diferente da pasta principal do projeto.

**Solução:** abra a pasta correta pelo menu **File → Open Folder...** e crie um novo terminal.

### Erro: `python` não é reconhecido

**Possível causa:** o Python não está instalado ou não foi adicionado ao PATH.

**Solução:** instale o Python pelo site oficial, marque **Add Python to PATH** e reinicie o terminal.

### Erro ao ativar `.venv`

**Possível causa:** o PowerShell bloqueou a execução do script de ativação.

**Solução:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Erro: compilador C não encontrado

**Possível causa:** o compilador necessário para a etapa SIL não está instalado ou não está disponível no PATH.

**Solução:** instale e configure um compilador compatível. Depois, abra um terminal novo e tente executar a simulação novamente.

### Um teste apresentou falha

**Possível causa:** o código, as dependências ou os valores esperados pelo teste podem estar inconsistentes.

**Solução:** examine a mensagem completa do pytest. Não altere os resultados esperados sem entender a causa da falha.

---

## 11. Boas práticas

- Execute os comandos a partir da pasta principal do projeto.
- Ative o ambiente virtual antes de instalar ou executar as dependências.
- Configure o `PYTHONPATH` em cada novo terminal.
- Execute os testes depois de modificar o código.
- Leia as mensagens de erro antes de tentar outros comandos.
- Não considere a aprovação dos testes uma certificação de segurança.
- Não utilize o código em um braço robótico real sem validação técnica adequada.

## 12. Conclusão

O fluxo básico de execução do AuroraArm é:

1. Preparar o ambiente Python.
2. Instalar as dependências.
3. Configurar o caminho de `src`.
4. Gerar o código C.
5. Executar os testes automatizados.
6. Executar as verificações de segurança modeladas.
7. Executar a simulação SIL, quando o ambiente necessário estiver disponível.

Seguindo essa sequência, é possível executar e avaliar as partes implementadas do projeto no ambiente de desenvolvimento.
