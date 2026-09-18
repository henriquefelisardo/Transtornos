# Akinator Clínico (DSM-5) - Inferência Probabilística

Bem-vindo ao **Akinator Clínico**, um sistema avançado de inferência probabilística projetado para triagem de Transtornos Mentais e de Personalidade com base rigorosa nos critérios do manual diagnóstico DSM-5.

Este projeto funciona como um "motor de árvore de decisão dinâmica", que calcula em tempo real o Ganho de Informação de cada pergunta e realiza uma entrevista psiquiátrica interativa. Ele oferece **duas** interfaces de uso: uma elegante Interface Web (via Django) e uma interface raiz de Linha de Comando (CLI). Ambas operam exatamente com o mesmo cérebro probabilístico.

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

O projeto é modular e as camadas são extremamente bem separadas:

* **Banco de Dados (Conhecimento):**
  * `knowledge_base.json`: Mapeia os 19 transtornos, os pesos dos sintomas (`key_symptoms` vs `secondary_symptoms`), os agrupamentos guarda-chuva (`umbrella`) e a hierarquia de dependência clínica (`depends_on`).
  * `disorder_details.json`: Mapeia os relatórios clínicos extensos. Após o diagnóstico, as descrições, critérios clínicos e condutas profissionais são resgatados deste arquivo.

* **O Cérebro (Lógica):**
  * `engine.py`: O coração matemático do projeto. Contém a classe `InferenceEngine`, que carrega o banco JSON, gerencia os cálculos e a árvore de probabilidade, e toma as decisões do sistema. Não tem dependências e é `stateless-friendly`.

* **O Frontend (Django):**
  * Diretório `web_app/` e `manage.py`: Uma aplicação Web minimalista e elegante em Django que roda o sistema pelo navegador. Para garantir velocidade máxima, a interface usa a funcionalidade de "Sessões" nativa do Django. Cada resposta é salva no navegador do cliente em tempo real, eliminando a necessidade de banco de dados (`SQLite`) e acelerando absurdamente o carregamento de cada pergunta.
  * Além do mouse, as interfaces suportam captura de teclado (via JavaScript Vanilla) para emular o terminal!

* **O Terminal (CLI):**
  * `cli.py`: A versão inicial "Raiz". Utiliza buffers crus (`tty`/`termios`) para criar uma experiência de jogo interativa dentro do terminal Linux, permitindo selecionar alternativas com as setinhas e re-renderizando in-place as linhas da interface, garantindo logs e debugging extremamente enxutos.

---

## 🚀 Como Instalar e Rodar

Você pode escolher rodar a versão moderna pela WEB ou a versão clássica pelo Terminal. Ambas partilham da mesma inteligência.

### Pré-requisitos Gerais
Caso escolha rodar a interface WEB, você precisa ter a biblioteca do **Django** instalada no seu sistema ou no seu ambiente virtual.
```bash
pip install django
# Ou no Ubuntu: sudo apt install python3-django
```

### Opção 1: Interface Web (Browser)
Se quiser a experiência visual rica:

1. Ative seu ambiente virtual (se aplicável).
2. Na raiz do projeto, inicie o servidor:
   ```bash
   python manage.py runserver 2222
   ```
   *(Substitua `2222` pela porta que desejar).*
3. Abra seu navegador de preferência e acesse **http://127.0.0.1:2222/**.
4. **Dica de Ouro:** A interface web possui suporte total a teclado! Utilize as **Setas (⬅️ ➡️)** do teclado para alternar entre "Discordo" e "Concordo", e **Espaço / Enter** para enviar sua resposta e pular para a próxima tela sem tocar no mouse!

### Opção 2: Linha de Comando (Terminal)
Se quiser a experiência nerd e rápida, o terminal não exige instalação de bibliotecas externas (funciona 100% com o Python nativo do Linux):

1. Vá até a raiz do projeto.
2. Execute o script principal:
   ```bash
   python cli.py
   ```
3. Use a **Seta Esquerda (⬅️)** e **Direita (➡️)** para alternar entre as respostas, e aperte **ENTER** para prosseguir. No terminal, se você solicitar a visualização do ranking na primeira tela, verá o *Leaderboard* das top 5 doenças atualizando a cada apertada de botão em tempo real.

---
**Aviso Legal:** O resultado gerado pelo algoritmo probabilístico deste projeto é um experimento matemático-lógico e de forma alguma substitui uma avaliação profissional, psiquiátrica ou psicológica clínica e humana. Procure sempre um profissional habilitado da saúde.
