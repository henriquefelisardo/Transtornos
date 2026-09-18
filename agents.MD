# Configuração de Agentes

Para a construção do sistema Akinator DSM-5, o trabalho é dividido entre três agentes especializados:

## Agente 1: Pesquisador Clínico
**Objetivo:** Levantar e estruturar os critérios diagnósticos baseados no DSM-5 para as condições alvo.
**Responsabilidades:**
- Analisar os critérios do DSM-5 para cada transtorno listado no `gemini.MD`.
- Extrair os 10 critérios diagnósticos mais recorrentes por transtorno.
- Classificar cada critério em **"Sintomas-chave"** (obrigatórios para o diagnóstico, peso eliminatório se negados) e **"Sintomas Secundários"** (peso cumulativo).
- Fornecer um relatório estruturado para o Agente 2.

## Agente 2: Arquiteto de Inferência
**Objetivo:** Traduzir dados clínicos em uma matriz de probabilidade pesquisável (JSON) e formular as perguntas.
**Responsabilidades:**
- Criar perguntas de "Sim/Não" em linguagem natural, acessíveis e não enviesadas, com base nos critérios levantados pelo Agente 1.
- Desenvolver perguntas "guarda-chuva" (generalistas) para nós superiores da árvore (ex: sintomas que abrangem todo o Cluster B de personalidade ou quadros psicóticos gerais).
- Desenvolver perguntas específicas para os nós folha (diferenciação fina entre transtornos semelhantes).
- Estruturar o `knowledge_base.json`, mapeando as perguntas para os transtornos, definindo os limiares (thresholds) e categorizando os impactos (sintoma chave vs secundário).

## Agente 3: Desenvolvedor Python
**Objetivo:** Desenvolver o motor algorítmico, a lógica de inferência e a interface.
**Responsabilidades:**
- Criar a classe/módulo do Motor de Inferência (`engine.py`).
- Implementar a lógica matemática de seleção da próxima pergunta (Ganho de Informação / Entropia / Redução de Espaço de Busca).
- Implementar a lógica de atualização de probabilidades baseada nas respostas e nos pesos do JSON (podar transtornos descartados, somar probabilidade nos prováveis).
- Criar a Interface de Terminal (`cli.py`) isolada da engine, para interagir com o usuário.
- Desenvolver o script de exportação (`export.py`) que converte o estado/matriz em um diagrama legível (ex: Mermaid.js).
