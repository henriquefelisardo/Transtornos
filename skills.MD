# Habilidades (Skills) Necessárias

Este documento descreve as competências técnicas e teóricas requeridas pelos agentes para executar o projeto com sucesso.

## 1. Conhecimento Clínico (DSM-5)
- **Pesquisa Psiquiátrica:** Capacidade de extrair e resumir critérios diagnósticos oficiais do Manual Diagnóstico e Estatístico de Transtornos Mentais (5ª Edição).
- **Taxonomia de Transtornos:** Compreensão dos agrupamentos de transtornos (ex: Clusters de Personalidade A, B e C, Espectro da Esquizofrenia, Transtornos de Humor).
- **Tradução Clínica para Leigos:** Habilidade de converter jargões médicos (ex: "afeto embotado", "delírios persecutórios") em perguntas simples e compreensíveis de Sim/Não.

## 2. Engenharia do Conhecimento e Estruturação de Dados
- **Modelagem JSON:** Capacidade de criar esquemas JSON relacionais eficientes que modelem árvores de decisão e matrizes de pesos.
- **Lógica de Árvores de Decisão:** Habilidade para criar perguntas hierárquicas, minimizando a profundidade da árvore através de perguntas "guarda-chuva".
- **Visualização de Dados:** Capacidade de escrever sintaxe Mermaid.js (`flowchart`, `graph`) para representar o fluxo lógico.

## 3. Matemática e Algoritmos de Inferência
- **Teorema de Bayes (Adaptado):** Conhecimento para implementar atualização de probabilidades a cada nova evidência (resposta do usuário).
- **Teoria da Informação (Ganho de Informação / Entropia):** Habilidade matemática para calcular qual pergunta divide os transtornos candidatos de forma mais simétrica ou elimina a maior quantidade de incerteza.
- **Sistemas Baseados em Regras (Pesos):** Capacidade de implementar "hard-pruning" (podar um galho da árvore se um sintoma eliminatório for negado) combinado com acúmulo de pesos.

## 4. Engenharia de Software (Python)
- **Design Patterns:** Habilidade de desacoplar regras de negócio (Inference Engine) da camada de apresentação (CLI).
- **Manipulação de Estado:** Gerenciamento seguro do estado da sessão do usuário (perguntas já feitas, histórico de respostas, probabilidades dinâmicas).
- **Tipagem Estática:** Uso de `typing` no Python para garantir que os objetos vindos do JSON sejam corretamente validados e interpretados pela Engine.
