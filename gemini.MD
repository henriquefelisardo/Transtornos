# Diretrizes Gerais: Sistema de Inferência Probabilística (Akinator DSM-5)

## Objetivo
Criar um sistema especialista em Python inspirado no Akinator para identificar transtornos mentais e de personalidade utilizando rigorosamente os critérios do DSM-5.

## Regras de Negócio e Restrições
1. **Limite de Perguntas:** O sistema deve fazer no máximo 25 perguntas (respostas exclusivamente Sim/Não).
2. **Critérios Diagnósticos:** O mapeamento deve cobrir os 10 principais critérios diagnósticos de cada transtorno.
3. **Sistema de Pesos:**
   - **Sintomas-chave (Obrigatórios):** Possuem peso alto. Se forem negados (ex: consecutivamente), a condição correspondente é "podada" da árvore de possibilidades.
   - **Sintomas Secundários:** Possuem peso cumulativo. Se confirmados, aumentam a probabilidade da condição.
4. **Condição de Parada:** 
   - A probabilidade de um transtorno atinge o limiar (threshold) de diagnóstico.
   - O limite de 25 perguntas é alcançado.
   - Se nenhuma condição atingir o limiar, o sistema retorna: "Nenhum transtorno reconhecido".
5. **Seleção da Próxima Pergunta:** O algoritmo deve utilizar o conceito de **Ganho de Informação** (ou similar, baseado em Entropia/Probabilidade). A próxima pergunta deve ser aquela que elimina o maior número de transtornos restantes ou divide melhor o espaço de busca (ex: perguntas guarda-chuva para clusters).
6. **Estado e Dados:** Toda a lógica de estado, perguntas e matriz de pesos deve estar em um arquivo local (JSON ou SQLite). *Não utilizar Vector DB*.
7. **Arquitetura Modular:** O "Motor de Inferência" deve ser isolado da "Interface de Terminal" (CLI).
8. **Exportação Visual:** O mapeamento/matriz deve ser facilmente exportável para um formato visual, como Mermaid.js ou um JSON altamente legível.
9. **Tecnologias:** Uso exclusivo de ferramentas gratuitas, locais e open-source.

## Condições Mapeadas
1. Transtorno Psicótico Breve
2. Transtorno Esquizofreniforme
3. Esquizofrenia
4. Transtorno Bipolar (Tipos I e II)
5. Transtorno Depressivo Maior
6. Transtorno de Ansiedade Generalizada
7. Transtorno do Pânico
8. Transtorno Obsessivo-Compulsivo
9. Transtorno de Estresse Pós-Traumático
10. Transtornos de Personalidade (Paranoide, Esquizoide, Antissocial, Borderline, Narcisista, Evitativa, Obsessivo-Compulsiva)
11. TDAH
12. Transtorno do Espectro Autista

## Disclaimer
Este sistema possui fins puramente educacionais e de demonstração tecnológica, não substituindo o diagnóstico clínico realizado por profissionais de saúde qualificados.
