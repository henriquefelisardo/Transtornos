# Akinator Clínico (DSM-5) - Inferência Probabilística

Bem-vindo ao **Akinator Clínico**, um sistema avançado de inferência probabilística projetado para triagem de Transtornos Mentais e de Personalidade com base rigorosa nos critérios do manual diagnóstico DSM-5.

Este projeto funciona como um "motor de árvore de decisão dinâmica", que calcula em tempo real o Ganho de Informação de cada pergunta e realiza uma entrevista psiquiátrica interativa por meio de um CLI (Interface de Linha de Comando) responsivo.

---

## 🧠 Como Funciona (Lógica e Matemática)

Ao contrário de sistemas clássicos que usam fluxogramas rígidos (`Se X, vá para Y`), este sistema é puramente dinâmico. A cada resposta do usuário, o algoritmo recalcula todas as probabilidades e escolhe ativamente a melhor próxima pergunta utilizando as seguintes lógicas:

### 1. Seleção por Entropia de Shannon (Information Gain)
O núcleo do `engine.py` utiliza o cálculo de Entropia. Ele avalia o cenário atual das doenças "vivas" e escolhe a pergunta que divide o espaço de probabilidade mais próximo de 50/50. O motor sempre fará perguntas altamente abrangentes ("Umbrella") no começo para descartar grandes blocos de transtornos, e só fará perguntas específicas quando estiver tentando afunilar o diagnóstico.

### 2. Focus Mode (Drill-Down)
Se a pontuação de uma doença específica começa a subir muito (ex: o usuário relata extrema desatenção e hiperatividade), o algoritmo detecta que existe um "Líder Provável". Quando isso acontece, ele aplica um multiplicador na entropia e "suga" a entrevista temporariamente para focar nos outros sintomas daquela doença (Focus Mode). Se o paciente negar os próximos sintomas, o Focus Mode desarma e o motor volta a investigar a base geral.

### 3. Escala de Concordância (Likert Scale)
O sistema não usa o engessado `Sim` / `Não`. Ele utiliza uma escala de peso fracionado de 5 pontos:
- **Discordo Totalmente (0.0):** Penalidade pesada. A pontuação da doença afunda. Se for a raiz de uma árvore de dependência, a árvore é trancada.
- **Discordo (0.25):** Penalidade leve.
- **Não Sei (0.50):** Resposta Neutra. Impacto matemático zero no motor, a doença nem ganha nem perde pontos.
- **Concordo Um Pouco (0.75):** Bônus parcial de pontuação (libera a árvore de dependência).
- **Concordo Totalmente (1.00):** Bônus total de pontuação para a doença.

### 4. Árvore de Dependências Lógicas (`depends_on`)
O sistema compreende hierarquia de eventos clínicos. É impossível ter *Estresse Pós-Traumático* sem ter tido um *Trauma*.
No `knowledge_base.json`, perguntas de "detalhamento" estão ancoradas em perguntas "raiz". Se o usuário responder "Discordo Totalmente" para a ocorrência de um trauma, o algoritmo **exclui permanentemente** da sessão todas as perguntas detalhadas (ex: esquiva do trauma, pesadelos do trauma). O sistema nunca fará perguntas impossíveis.

### 5. Cautela Diagnóstica Máxima
Transtornos como a Personalidade Paranoide possuem poucos sintomas documentados, enquanto o Transtorno Borderline possui muitos. Isso criava uma falha em que a Paranoia atingia o limite probabilístico (`threshold`) rapidamente.
Para corrigir, a `InferenceEngine` está matematicamente travada e **proibida de dar um diagnóstico antes de realizar pelo menos 30 perguntas**. O paciente é testado por caminhos paralelos mesmo que a pontuação passe do limiar, garantindo maturidade no diagnóstico final. (O limite máximo é de 50 perguntas).

---

## 🏗️ Arquitetura do Projeto

O projeto não requer bibliotecas externas gigantes. Ele foi escrito 100% em Python nativo.

* `knowledge_base.json`: O banco de dados construído pelos Agentes IA. Ele mapeia os transtornos, o peso (`key_symptoms` vs `secondary_symptoms`), os agrupamentos de perguntas cruzadas e a hierarquia de dependência clínica (`depends_on`).
* `engine.py`: O Cérebro. Contém a classe `InferenceEngine`, responsável por carregar o banco JSON, gerenciar as pontuações e penalidades (Soft-Pruning), armazenar as respostas pregressas e calcular a matriz de entropia de Shannon para retornar a próxima questão.
* `cli.py`: A Interface Single-Page. Utiliza `sys` e `termios` para ler diretamente o buffer do teclado no terminal linux, permitindo navegação via "setinhas" (⬅️ ➡️). A cada interação, ele limpa a tela e renderiza um *Leaderboard* atualizado em tempo real no topo, listando os 5 transtornos mais cotados no momento.
* `clinical_data.json`: Arquivo bruto residual contendo a extração direta dos critérios do DSM-5 usada como base.

---

## 🚀 Como Executar

**Pré-requisitos:** O sistema foi construído puramente com as bibliotecas built-in do Python e preparado para rodar em terminais TTY (Linux/Mac). **Nenhum** `pip install` é necessário.

Para iniciar sua avaliação psiquiátrica automatizada, basta executar:

```bash
cd /home/henryfelisardo/code/Transtornos
python3 cli.py
```

**Controles:**
- Use a **Seta Esquerda (⬅️)** e a **Seta Direita (➡️)** para alternar entre os botões de Discordância e Concordância.
- Pressione **ENTER** para confirmar a resposta.
- Pressione **CTRL+C** a qualquer momento para abandonar a sessão de triagem.

**Aviso Legal:** O resultado gerado pelo algoritmo probabilístico é um experimento e de forma alguma substitui uma avaliação profissional psiquiátrica clínica e humana.
