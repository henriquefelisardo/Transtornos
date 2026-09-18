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

def render_screen(engine: InferenceEngine, prompt_text: str, menu_str: str):
    # Limpar tela
    sys.stdout.write("\033[2J\033[H")
    
    # Cabeçalho
    print("=" * 70)
    print("🧠 Akinator DSM-5 - Inferência Probabilística (v6.0)")
    print("=" * 70)
    
    # Leaderboard (Top 5)
    print("  🏆 LEADERBOARD (Top 5 Diagnósticos):")
    sorted_disorders = sorted(engine.scores.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_disorders[:5]
    
    for i, (d_id, score) in enumerate(top_5):
        name = engine.active_disorders.get(d_id, engine.disorders[0]).get("name", d_id) if d_id in engine.active_disorders else d_id
        # Limita tamanho do nome para não quebrar layout
        name = (name[:45] + '...') if len(name) > 45 else name
        print(f"  {i+1}. {name.ljust(48)} ({score:+.2f})")
    print("=" * 70)
    
    # Pergunta
    wrapped_prompt = textwrap.fill(prompt_text, width=70)
    print(f"\n{wrapped_prompt}\n")
    
    # Menu (na última linha de renderização)
    sys.stdout.write(f"{menu_str}")
    sys.stdout.flush()

def ask_frequency(engine: InferenceEngine, question_count: int, max_questions: int, prompt: str) -> float:
    prompt_text = f"Pergunta [{question_count+1}/{max_questions}]: {prompt}"
    
    options = [
        ("Nunca", 0.0),
        ("Raramente", 0.25),
        ("Às vezes", 0.5),
        ("Frequentemente", 0.75),
        ("Sempre", 1.0)
    ]
    selected_idx = 0
    
    while True:
        menu_parts = []
        for i, (label, weight) in enumerate(options):
            if i == selected_idx:
                menu_parts.append(f"\033[96m❯ [{label}]\033[0m")
            else:
                menu_parts.append(f"  [{label}]")
        
        menu_str = " ".join(menu_parts)
        render_screen(engine, prompt_text, menu_str)
        
        key = get_key()
        if key == '\x1b[C': # Seta Direita
            selected_idx = min(len(options) - 1, selected_idx + 1)
        elif key == '\x1b[D': # Seta Esquerda
            selected_idx = max(0, selected_idx - 1)
        elif key in ('\r', '\n'): # Enter
            return options[selected_idx][1]
        elif key == '\x03': # Ctrl+C
            sys.stdout.write("\nOperação cancelada pelo usuário.\n")
            sys.exit(0)

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
            sys.stdout.write("\033[2J\033[H")
            print("=" * 70)
            if result:
                print(f"✅ DIAGNÓSTICO ATINGIDO: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
            else:
                print("❌ Nenhum transtorno reconhecido com base nas respostas fornecidas.")
            print("=" * 70)
            return

        q = engine.get_next_question()
        if not q:
            break
            
        weight = ask_frequency(engine, question_count, max_questions, q['text'])
        engine.process_answer(q["id"], weight)
        question_count += 1
        
    # Limite de perguntas atingido
    stop, result = engine.check_stop_conditions()
    sys.stdout.write("\033[2J\033[H")
    print("=" * 70)
    if result:
        print(f"✅ DIAGNÓSTICO ATINGIDO NO LIMITE: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
    else:
        print("❌ Limite de 50 perguntas atingido. Diagnóstico inconclusivo.")
        if engine.active_disorders:
            best_id = max(engine.scores, key=engine.scores.get)
            best_score = engine.scores[best_id]
            print(f"Transtorno mais próximo: {engine.active_disorders[best_id]['name']} (Score: {best_score:.2f})")
    print("=" * 70)

if __name__ == "__main__":
    main()
