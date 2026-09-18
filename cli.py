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

def ask_yes_no(prompt: str) -> bool:
    # Usando textwrap para evitar linhas muito compridas no terminal
    wrapped_prompt = textwrap.fill(prompt, width=75)
    sys.stdout.write(f"\n{wrapped_prompt}\n")
    sys.stdout.flush()
    selected = True  # True = Sim, False = Não
    while True:
        sim_str = " \033[92m❯ [ Sim ]\033[0m" if selected else "   [ Sim ]"
        nao_str = " \033[91m❯ [ Não ]\033[0m" if not selected else "   [ Não ]"
        
        # Retorna o cursor para o começo da linha e limpa
        sys.stdout.write(f"\r\033[K{sim_str}    {nao_str}")
        sys.stdout.flush()
        
        key = get_key()
        if key == '\x1b[C': # Seta Direita
            selected = False
        elif key == '\x1b[D': # Seta Esquerda
            selected = True
        elif key in ('\r', '\n'): # Enter
            sys.stdout.write("\n")
            return selected
        elif key == '\x03': # Ctrl+C
            sys.stdout.write("\nOperação cancelada pelo usuário.\n")
            sys.exit(0)

def main():
    print("=" * 70)
    print("🧠 Sistema de Inferência de Transtornos Mentais (CLI)")
    print("=" * 70)
    print("⚠️  AVISO CLÍNICO:")
    print("Este sistema é um experimento algorítmico de inferência probabilística.")
    print("NÃO substitui, de forma alguma, a avaliação, diagnóstico médico ou")
    print("tratamento fornecido por um profissional de saúde mental qualificado.")
    print("=" * 70)
    print("Instruções: Use as setas ⬅️ ➡️ para escolher e pressione ENTER para confirmar.")
    print("-" * 70)

    try:
        engine = InferenceEngine("knowledge_base.json")
    except FileNotFoundError:
        print("Erro: O arquivo 'knowledge_base.json' não foi encontrado no diretório atual.")
        sys.exit(1)
    
    question_count = 0
    max_questions = 40
    
    while question_count < max_questions:
        # Checar se já temos um vencedor
        stop, result = engine.check_stop_conditions()
        if stop:
            if result:
                print(f"\n✅ Diagnóstico provável atingido: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
            else:
                print("\n❌ Nenhum transtorno reconhecido com base nas respostas fornecidas (espaço de busca esgotado).")
            return

        q = engine.get_next_question()
        if not q:
            break
            
        # Obter resposta do usuário via setas
        prompt_text = f"Pergunta [{question_count+1}/{max_questions}]: {q['text']}"
        answer_bool = ask_yes_no(prompt_text)
        
        engine.process_answer(q["id"], answer_bool)
        question_count += 1
        
    # Se o loop terminar por atingir o limite de perguntas
    stop, result = engine.check_stop_conditions()
    if result:
        print(f"\n✅ Diagnóstico provável atingido no limite de perguntas: {result['name']} (Score: {engine.scores[result['id']]:.2f})")
    else:
        print("\n❌ Limite de 40 perguntas atingido. Nenhum transtorno reconhecido com segurança.")
        
        # Mostrar as doenças mais prováveis restantes que não atingiram o threshold
        if engine.active_disorders:
            best_id = max(engine.scores, key=engine.scores.get)
            best_score = engine.scores[best_id]
            if best_score > 0:
                print(f"Transtorno mais próximo do limiar: {engine.active_disorders[best_id]['name']} (Score: {best_score:.2f})")

if __name__ == "__main__":
    main()
