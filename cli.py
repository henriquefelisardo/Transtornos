import sys
import tty
import termios
import textwrap
import os
from engine import InferenceEngine

def get_engine_state(engine: InferenceEngine):
    return {
        'scores': engine.scores.copy(),
        'asked_questions': engine.asked_questions.copy(),
        'answers': engine.answers.copy()
    }

def restore_engine_state(engine: InferenceEngine, state: dict):
    engine.scores = state['scores'].copy()
    engine.asked_questions = state['asked_questions'].copy()
    engine.answers = state['answers'].copy()

def render_header(engine: InferenceEngine, prompt_text: str, show_log: bool):
    print("=" * 80)
    print("🧠 Akinator DSM-5 - Inferência Probabilística")
    print("=" * 80)
    
    if show_log:
        print("  🏆 LEADERBOARD (Top 5 Diagnósticos):")
        sorted_disorders = sorted(engine.scores.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_disorders[:5]
        
        for i, (d_id, score) in enumerate(top_5):
            name = engine.active_disorders.get(d_id, engine.disorders[0]).get("name", d_id) if d_id in engine.active_disorders else d_id
            name = (name[:45] + '...') if len(name) > 45 else name
            print(f"  {i+1}. {name.ljust(48)} ({score:+.2f})")
        print("=" * 80)
    
    if prompt_text:
        wrapped_prompt = textwrap.fill(prompt_text, width=80)
        print(f"{wrapped_prompt}")

def interactive_menu(engine: InferenceEngine, prompt_text: str, options: list, default_idx: int, show_log: bool, can_go_back: bool):
    selected_idx = default_idx
    
    sys.stdout.write('\033[?25l') # Esconder cursor
    
    # Limpa a tela inteira UMA vez por pergunta para evitar que a tela pisque (flicker)
    sys.stdout.write('\033[2J\033[H')
    
    render_header(engine, prompt_text, show_log)
    
    if can_go_back:
        print("\n\033[90m(Pressione Seta Esquerda para voltar à pergunta anterior)\033[0m")
    else:
        print()
        
    print("Selecione uma opção (Cima/Baixo para navegar, Enter para confirmar):")
    print()
    
    # Pré-imprime as linhas vazias para podermos mover o cursor para cima depois
    for _ in options:
        print()
        
    sys.stdout.flush()
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        # tty.setcbreak impede que a digitação seja ecoada no terminal ("ins desnecessário")
        tty.setcbreak(fd)
        while True:
            # Volta o cursor N linhas para cima para redesenhar APENAS as opções
            sys.stdout.write(f"\033[{len(options)}A")
            
            for i, (label, val) in enumerate(options):
                if i == selected_idx:
                    sys.stdout.write(f"\r\033[K  \033[96m❯ {label}\033[0m\n")
                else:
                    sys.stdout.write(f"\r\033[K    {label}\n")
            
            sys.stdout.flush()
            
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    key = '\x1b[' + ch3
                else:
                    key = ch
            else:
                key = ch
                
            if key == '\x1b[B': # Baixo
                selected_idx = min(len(options) - 1, selected_idx + 1)
            elif key == '\x1b[A': # Cima
                selected_idx = max(0, selected_idx - 1)
            elif key == '\x1b[D': # Esquerda (Voltar)
                if can_go_back:
                    return 'BACK'
            elif key in ('\x08', '\x7f'): # Backspace
                if can_go_back:
                    return 'BACK'
            elif key in ('\r', '\n', '\x1b[C'): # Enter ou Direita para confirmar
                return options[selected_idx][1]
            elif key == '\x03': # Ctrl+C
                sys.stdout.write("\nOperação cancelada pelo usuário.\n")
                sys.stdout.write('\033[?25h')
                sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write('\033[?25h') # Mostrar cursor
        sys.stdout.write('\033[2J\033[H') # Limpar tela ao sair do menu para manter limpo
        sys.stdout.flush()

def ask_yes_no(engine: InferenceEngine, prompt: str) -> bool:
    options = [("Sim", True), ("Não", False)]
    return interactive_menu(engine, prompt, options, default_idx=0, show_log=False, can_go_back=False)

def ask_frequency(engine: InferenceEngine, question_count: int, max_questions: int, prompt: str, show_log: bool, can_go_back: bool):
    prompt_text = f"Pergunta [{question_count+1}/{max_questions}]: {prompt}"
    
    options = [
        ("Discordo Totalmente", 0.0),
        ("Discordo", 0.25),
        ("Não Sei", 0.5),
        ("Concordo um pouco", 0.75),
        ("Concordo Totalmente", 1.0)
    ]
    
    return interactive_menu(engine, prompt_text, options, default_idx=2, show_log=show_log, can_go_back=can_go_back)

def print_diagnosis_details(disorder_id: str, engine_instance):
    import json
    try:
        with open("disorder_details.json", "r", encoding="utf-8") as f:
            details = json.load(f)
    except FileNotFoundError:
        print("\033[93m[Aviso] Detalhamento do transtorno não encontrado (disorder_details.json ausente).\033[0m")
        return

    info = details.get(disorder_id)
    if not info:
        return

    print(f"\033[1;36m=== DETALHAMENTO CLÍNICO ===\033[0m")
    
    desc_str = f"O que é: {info.get('descricao', '')}"
    print(textwrap.fill(desc_str, width=80).replace("O que é:", "\033[1mO que é:\033[0m", 1) + "\n")
    
    sintomas_str = f"Sintomas Principais: {info.get('sintomas_principais', '')}"
    print(textwrap.fill(sintomas_str, width=80).replace("Sintomas Principais:", "\033[1mSintomas Principais:\033[0m", 1) + "\n")
    
    criterios_str = f"Critérios Clínicos: {info.get('criterios_clinicos', '')}"
    print(textwrap.fill(criterios_str, width=80).replace("Critérios Clínicos:", "\033[1mCritérios Clínicos:\033[0m", 1) + "\n")
    
    proceder_str = f"Como Proceder: {info.get('como_proceder', '')}"
    print(textwrap.fill(proceder_str, width=80).replace("Como Proceder:", "\033[1mComo Proceder:\033[0m", 1))
    
    print("=" * 80)

def main():
    try:
        engine = InferenceEngine("knowledge_base.json")
    except FileNotFoundError:
        print("Erro: O arquivo 'knowledge_base.json' não foi encontrado no diretório atual.")
        sys.exit(1)
    
    show_log = ask_yes_no(engine, "Ativar log de debug (ranking de diagnósticos)?")
    
    history = []
    max_questions = 50
    
    while True:
        stop, result = engine.check_stop_conditions()
        if stop:
            print("=" * 80)
            if result:
                print(f"✅ DIAGNÓSTICO ATINGIDO: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
                print("=" * 80)
                print_diagnosis_details(result['id'], engine)
            else:
                print("❌ Nenhum transtorno reconhecido com base nas respostas fornecidas.")
                print("=" * 80)
            return

        if len(history) >= max_questions:
            break

        q = engine.get_next_question()
        if not q:
            break
            
        current_state = get_engine_state(engine)
        
        weight = ask_frequency(engine, len(history), max_questions, q['text'], show_log, can_go_back=len(history) > 0)
        
        if weight == 'BACK':
            if history:
                prev_state = history.pop()
                restore_engine_state(engine, prev_state)
            continue
            
        history.append(current_state)
        engine.process_answer(q["id"], weight)
        
    stop, result = engine.check_stop_conditions()
    print("=" * 80)
    if result:
        print(f"✅ DIAGNÓSTICO ATINGIDO NO LIMITE: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
        print("=" * 80)
        print_diagnosis_details(result['id'], engine)
    else:
        print("Diagnóstico inconclusivo, não indicando nenhum transtorno.")
        if engine.active_disorders:
            best_id = max(engine.scores, key=engine.scores.get)
            best_score = engine.scores[best_id]
            print(f"Transtorno mais próximo: {engine.active_disorders[best_id]['name']} (Score: {best_score:.2f})")
        print("=" * 80)

if __name__ == "__main__":
    main()
