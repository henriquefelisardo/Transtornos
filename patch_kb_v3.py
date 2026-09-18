import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Novas perguntas transversais e super guarda-chuvas
new_questions = [
    {
        "id": "q_disforia_rejeicao",
        "text": "Você sente uma dor emocional extrema e desproporcional quando acha que alguém te rejeitou, ignorou ou criticou?",
        "type": "specific",
        "targets": ["tp_borderline", "tp_evitativa", "tdah"]
    },
    {
        "id": "q_desregulacao_emocional",
        "text": "Você tem muita dificuldade de controlar suas emoções, passando rapidamente de estar bem para acessos de raiva ou choro intenso?",
        "type": "umbrella",
        "targets": ["tp_borderline", "bipolar_1", "bipolar_2", "tdah", "tea"]
    },
    {
        "id": "q_isolamento_social_extremo",
        "text": "Você prefere ficar completamente isolado(a) e tem pouquíssimo ou nenhum interesse em interações sociais?",
        "type": "umbrella",
        "targets": ["tp_esquizoide", "tp_evitativa", "tea", "depressivo_maior"]
    },
    {
        "id": "q_mente_acelerada_noturna",
        "text": "Sua mente fica tão acelerada à noite com pensamentos que é quase impossível conseguir desligar para dormir?",
        "type": "specific",
        "targets": ["ansiedade_generalizada", "bipolar_1", "bipolar_2", "tdah"]
    },
    {
        "id": "q_rigidez_mudancas",
        "text": "Você sente um desconforto ou irritação muito forte quando seus planos ou sua rotina precisam ser mudados de última hora?",
        "type": "specific",
        "targets": ["tea", "toc", "tp_obsessivo_compulsiva"]
    },
    {
        "id": "q_hiperfoco_intenso",
        "text": "Quando você se interessa por um assunto, você consegue passar horas ou dias obcecado por aquilo, esquecendo de comer ou dormir?",
        "type": "specific",
        "targets": ["tdah", "tea", "bipolar_2"]
    }
]

# Filtrar para evitar duplicidade caso o script rode duas vezes
existing_ids = set(q["id"] for q in data["questions"])
added_any = False
for q in new_questions:
    if q["id"] not in existing_ids:
        data["questions"].append(q)
        added_any = True

# Mapear os novos targets paras as respectivas doenças
mapping = {
    "tp_borderline": ["q_disforia_rejeicao"],
    "tp_evitativa": ["q_disforia_rejeicao"],
    "tdah": ["q_disforia_rejeicao", "q_mente_acelerada_noturna", "q_hiperfoco_intenso"],
    "ansiedade_generalizada": ["q_mente_acelerada_noturna"],
    "bipolar_1": ["q_mente_acelerada_noturna"],
    "bipolar_2": ["q_mente_acelerada_noturna", "q_hiperfoco_intenso"],
    "tea": ["q_rigidez_mudancas", "q_hiperfoco_intenso"],
    "toc": ["q_rigidez_mudancas"],
    "tp_obsessivo_compulsiva": ["q_rigidez_mudancas"]
}

for d in data["disorders"]:
    d_id = d["id"]
    if d_id in mapping:
        for new_sym in mapping[d_id]:
            if new_sym not in d["secondary_symptoms"] and new_sym not in d["key_symptoms"]:
                d["secondary_symptoms"].append(new_sym)

if added_any:
    with open("knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("V3: Novas perguntas injetadas com sucesso!")
else:
    print("V3: Perguntas já existiam no banco.")
