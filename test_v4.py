from engine import InferenceEngine

engine = InferenceEngine("knowledge_base.json")

# Checar se a pergunta q_trauma_evitacao pode ser perguntada inicialmente
q1 = engine.questions["q_trauma_evitacao"]
print("Pode perguntar trauma evitacao no inicio?", q1.get("depends_on") in engine.answers)

# Processar "Não" para o umbrella
engine.process_answer("q_trauma_umbrella", False)

# Checar novamente
can_ask_now = "q_trauma_umbrella" in engine.answers and engine.answers["q_trauma_umbrella"] == True
print("Pode perguntar trauma evitacao apoś 'Não'?", can_ask_now)

# Processar "Sim" para o umbrella
engine.process_answer("q_trauma_umbrella", True)
can_ask_now2 = "q_trauma_umbrella" in engine.answers and engine.answers["q_trauma_umbrella"] == True
print("Pode perguntar trauma evitacao apoś 'Sim'?", can_ask_now2)
