import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    "ou sentiu sua mente": "ou senti minha mente",
    "em que se sentiu": "em que me senti",
    "agir e se relacionar": "agir e me relacionar",
    "Desde a sua infância, eu apresenta": "Desde a minha infância, eu apresento",
    "eu tem sido": "eu tenho sido",
    "eu tem": "eu tenho",
    "que eu gosta": "que eu gosto",
    "eu se sente": "eu me sinto",
    "sua preocupação": "minha preocupação",
    "eu acredita": "eu acredito",
    "eu apresenta": "eu apresento",
    "eu já teve": "eu já tive",
    "eu percebe": "eu percebo",
    "eu reluta": "eu reluto",
    "eu percebe": "eu percebo",
    "eu guarda": "eu guardo",
    "eu demonstra": "eu demonstro",
    "eu não tem": "eu não tenho",
    "eu usa": "eu uso",
    "eu age": "eu ajo",
    "eu idealiza": "eu idealizo",
    "eu se perde": "eu me perco",
    "eu exige": "eu exijo",
    "eu convive": "eu convivo",
    "eu se recusa": "eu me recuso",
    "eu se vê": "eu me vejo",
    "eu se preocupa": "eu me preocupo",
    "eu costuma": "eu costumo",
    "eu acha": "eu acho",
    "eu possui": "eu possuo",
    "eu sinto que tem": "eu sinto que tenho",
    "eu é": "eu sou",
    "suas obrigações": "minhas obrigações",
    "sua rotina": "minha rotina",
    "seus interesses": "meus interesses"
}

for q in data["questions"]:
    t = q["text"]
    for old, new in replacements.items():
        t = t.replace(old, new)
        # Handle case variations
        t = t.replace(old.capitalize(), new.capitalize())
    q["text"] = t

with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Final grammar sweep.")
