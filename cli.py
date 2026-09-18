import sys
import tty
import termios
import textwrap
from engine import InferenceEngine

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Caracter de escape para setas
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def render_header(engine: InferenceEngine, prompt_text: str):
    # Cabeçalho
    print("=" * 80)
    print("🧠 Akinator DSM-5 - Inferência Probabilística")
    print("=" * 80)
    
    # Leaderboard (Top 5)
    print("  🏆 LEADERBOARD (Top 5 Diagnósticos):")
    sorted_disorders = sorted(engine.scores.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_disorders[:5]
    
    for i, (d_id, score) in enumerate(top_5):
        name = engine.active_disorders.get(d_id, engine.disorders[0]).get("name", d_id) if d_id in engine.active_disorders else d_id
        # Limita tamanho do nome para não quebrar layout
        name = (name[:45] + '...') if len(name) > 45 else name
        print(f"  {i+1}. {name.ljust(48)} ({score:+.2f})")
    print("=" * 80)
    
    # Pergunta
    wrapped_prompt = textwrap.fill(prompt_text, width=80)
    print(f"{wrapped_prompt}")

def ask_frequency(engine: InferenceEngine, question_count: int, max_questions: int, prompt: str) -> float:
    prompt_text = f"Pergunta [{question_count+1}/{max_questions}]: {prompt}"
    
    options = [
        ("Discordo Totalmente", 0.0),
        ("Discordo", 0.25),
        ("Não Sei", 0.5),
        ("Concordo um pouco", 0.75),
        ("Concordo Totalmente", 1.0)
    ]
    selected_idx = 2  # Começa no "Não Sei" por padrão
    
    render_header(engine, prompt_text)
    
    while True:
        menu_parts = []
        for i, (label, weight) in enumerate(options):
            if i == selected_idx:
                menu_parts.append(f"\033[96m❯ [{label}]\033[0m")
            else:
                menu_parts.append(f"  [{label}]")
        
        menu_str = " ".join(menu_parts)
        
        # Redraw only the menu line
        sys.stdout.write(f"\r\033[K{menu_str}")
        sys.stdout.flush()
        
        key = get_key()
        if key == '\x1b[C': # Seta Direita
            selected_idx = min(len(options) - 1, selected_idx + 1)
        elif key == '\x1b[D': # Seta Esquerda
            selected_idx = max(0, selected_idx - 1)
        elif key in ('\r', '\n'): # Enter
            sys.stdout.write("\n\n") # Give space for next question
            return options[selected_idx][1]
        elif key == '\x03': # Ctrl+C
            sys.stdout.write("\nOperação cancelada pelo usuário.\n")
            sys.exit(0)

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
    print(f"\033[1mO que é:\033[0m {info.get('descricao', '')}")
    print(f"\033[1mSintomas Principais:\033[0m {info.get('sintomas_principais', '')}")
    print(f"\033[1mCritérios Clínicos:\033[0m {info.get('criterios_clinicos', '')}")
    print(f"\033[1mComo Proceder:\033[0m {info.get('como_proceder', '')}")
    print("=" * 80)

def main():
    try:
        engine = InferenceEngine("knowledge_base.json")
    except FileNotFoundError:
        print("Erro: O arquivo 'knowledge_base.json' não foi encontrado no diretório atual.")
        sys.exit(1)
    
    question_count = 0
    max_questions = 50
    
    while question_count < max_questions:
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

        q = engine.get_next_question()
        if not q:
            break
            
        weight = ask_frequency(engine, question_count, max_questions, q['text'])
        engine.process_answer(q["id"], weight)
        question_count += 1
        
    # Limite de perguntas atingido
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
