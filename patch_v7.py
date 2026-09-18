import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Conversões genéricas
for q in data["questions"]:
    t = q["text"]
    # Conversões heurísticas simples
    if t.startswith("Você sente "):
        t = t.replace("Você sente ", "Eu sinto ")
    elif t.startswith("Você tem "):
        t = t.replace("Você tem ", "Eu tenho ")
    elif t.startswith("Você costuma "):
        t = t.replace("Você costuma ", "Eu costumo ")
    elif t.startswith("Você já "):
        t = t.replace("Você já ", "Eu já ")
    elif t.startswith("Você "):
        t = t.replace("Você ", "Eu ")
    elif t.startswith("Sua mente "):
        t = t.replace("Sua mente ", "Minha mente ")
    elif t.startswith("Seu humor "):
        t = t.replace("Seu humor ", "Meu humor ")
        
    if t.endswith("?"):
        t = t[:-1] + "."
    elif t.endswith("?).") or t.endswith(").?"):
        t = t.replace("?).", ").").replace(").?", ").")
    elif t.endswith("?)") or t.endswith(")?"):
        t = t.replace("?)", ").").replace(")?", ").")
        
    q["text"] = t

new_questions = [
    # Paranoide Especificidades
    {"id": "q_paranoide_desconfianca_frequente", "text": "Eu frequentemente suspeito, sem nenhuma prova real, de que as outras pessoas estão me explorando, me prejudicando ou me enganando.", "type": "specific", "targets": ["tp_paranoide"], "depends_on": "q_personalidade_umbrella"},
    {"id": "q_paranoide_rancor", "text": "Eu guardo rancor por muito tempo e tenho extrema dificuldade em perdoar insultos ou pequenos erros que os outros cometeram comigo.", "type": "specific", "targets": ["tp_paranoide"], "depends_on": "q_personalidade_umbrella"},
    {"id": "q_paranoide_lealdade", "text": "Eu fico o tempo todo duvidando da lealdade e da fidelidade dos meus amigos, colegas ou parceiros amorosos, mesmo sem motivo.", "type": "specific", "targets": ["tp_paranoide"], "depends_on": "q_personalidade_umbrella"},
    
    # Borderline Especificidades
    {"id": "q_borderline_identidade", "text": "Eu sinto que não sei quem eu sou de verdade; minha autoimagem, meus gostos e meus valores mudam o tempo todo dependendo de com quem eu estou.", "type": "specific", "targets": ["tp_borderline"], "depends_on": "q_personalidade_umbrella"},
    {"id": "q_borderline_vazio", "text": "Eu sinto um vazio existencial e uma sensação de tédio crônica profunda, como se faltasse um pedaço de mim.", "type": "specific", "targets": ["tp_borderline", "depressivo_maior"]},
    {"id": "q_borderline_raiva", "text": "Eu tenho acessos de raiva muito intensos e difíceis de controlar, frequentemente brigando fisicamente ou gritando quando estou frustrado.", "type": "specific", "targets": ["tp_borderline", "bipolar_1"], "depends_on": "q_personalidade_umbrella"},

    # Narcisista Especificidades
    {"id": "q_narcisista_grandiosidade", "text": "Eu sinto que sou uma pessoa especial e única, e que só posso ser compreendido por pessoas que também tenham alto status ou inteligência.", "type": "specific", "targets": ["tp_narcisista"], "depends_on": "q_personalidade_umbrella"},
    {"id": "q_narcisista_admiracao", "text": "Eu preciso e exijo ser constantemente admirado, elogiado e tratado como o centro das atenções.", "type": "specific", "targets": ["tp_narcisista"], "depends_on": "q_personalidade_umbrella"},
]

new_disorder = {
    "id": "tp_narcisista",
    "name": "Transtorno de Personalidade Narcisista",
    "key_symptoms": ["q_narcisista_grandiosidade", "q_narcisista_admiracao", "q_personalidade_umbrella"],
    "secondary_symptoms": [],
    "threshold": 0.8
}

existing_ids = set(q["id"] for q in data["questions"])
for q in new_questions:
    if q["id"] not in existing_ids:
        data["questions"].append(q)

disorder_ids = set(d["id"] for d in data["disorders"])
if "tp_narcisista" not in disorder_ids:
    data["disorders"].append(new_disorder)

# Adicionar symptoms nos transtornos
for d in data["disorders"]:
    if d["id"] == "tp_paranoide":
        if "q_paranoide_desconfianca_frequente" not in d["key_symptoms"]:
            d["key_symptoms"].extend(["q_paranoide_desconfianca_frequente", "q_paranoide_lealdade"])
        if "q_paranoide_rancor" not in d["secondary_symptoms"]:
            d["secondary_symptoms"].append("q_paranoide_rancor")
    if d["id"] == "tp_borderline":
        if "q_borderline_identidade" not in d["key_symptoms"]:
            d["key_symptoms"].extend(["q_borderline_identidade", "q_borderline_vazio"])
        if "q_borderline_raiva" not in d["secondary_symptoms"]:
            d["secondary_symptoms"].append("q_borderline_raiva")
    
with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("V7 patch concluído com sucesso.")
