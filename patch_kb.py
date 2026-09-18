import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Novas perguntas (nuances para Borderline, TDAH, Autismo)
new_questions = [
    {
        "id": "q_borderline_vazio_cronico",
        "text": "Você frequentemente sente um 'vazio' enorme por dentro, como se não soubesse quem você realmente é ou o que quer da vida?",
        "type": "specific",
        "targets": ["tp_borderline"]
    },
    {
        "id": "q_borderline_automutilacao",
        "text": "Quando a dor emocional é muito forte, você já se cortou, se machucou de propósito ou ameaçou tirar a própria vida?",
        "type": "specific",
        "targets": ["tp_borderline", "depressivo_maior"]
    },
    {
        "id": "q_borderline_idealizacao",
        "text": "Você costuma idolatrar uma pessoa rapidamente no início da relação, mas pouco tempo depois passa a odiá-la ou achá-la péssima por uma pequena falha?",
        "type": "specific",
        "targets": ["tp_borderline"]
    },
    {
        "id": "q_tdah_paralisia",
        "text": "Você sofre de 'paralisia de tarefas', onde quer muito fazer algo importante mas seu cérebro simplesmente não deixa você começar?",
        "type": "specific",
        "targets": ["tdah"]
    },
    {
        "id": "q_tea_masking",
        "text": "Você sente que precisa criar um 'personagem' ou forçar contato visual para parecer normal perto das outras pessoas, o que te deixa exausto(a)?",
        "type": "specific",
        "targets": ["tea"]
    }
]

data["questions"].extend(new_questions)

# Atualizar sintomas das doenças
for d in data["disorders"]:
    if d["id"] == "tp_borderline":
        if "q_borderline_vazio_cronico" not in d["secondary_symptoms"]:
            d["secondary_symptoms"].extend(["q_borderline_vazio_cronico", "q_borderline_automutilacao", "q_borderline_idealizacao"])
    elif d["id"] == "tdah":
        if "q_tdah_paralisia" not in d["secondary_symptoms"]:
            d["secondary_symptoms"].append("q_tdah_paralisia")
    elif d["id"] == "tea":
        if "q_tea_masking" not in d["secondary_symptoms"]:
            d["secondary_symptoms"].append("q_tea_masking")

with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Base de dados atualizada com novas nuances.")
