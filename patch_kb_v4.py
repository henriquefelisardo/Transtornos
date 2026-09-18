import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Mapeamento de dependências: ID da pergunta filha -> ID da pergunta pai (raiz)
dependencies = {
    # TEPT (Depende de Trauma Umbrella ou Exposição a trauma)
    "q_trauma_exposicao": "q_trauma_umbrella",
    "q_trauma_intrusao": "q_trauma_umbrella",
    "q_trauma_evitacao": "q_trauma_umbrella",
    "q_trauma_cognicao": "q_trauma_umbrella",
    "q_trauma_amnesia": "q_trauma_umbrella",
    "q_trauma_crencas": "q_trauma_umbrella",
    "q_trauma_reatividade": "q_trauma_umbrella",
    "q_trauma_imprudencia": "q_trauma_umbrella",
    "q_trauma_sono_concentracao": "q_trauma_umbrella",
    "q_trauma_duracao": "q_trauma_umbrella",

    # Pânico (Depende de Ataques de Pânico)
    "q_medo_novos_ataques": "q_ataques_panico",
    "q_evitacao_panico": "q_ataques_panico",
    "q_panico_fisico_coracao": "q_ataques_panico",
    "q_panico_fisico_tremor": "q_ataques_panico",
    "q_panico_fisico_ar": "q_ataques_panico",
    "q_panico_fisico_dor": "q_ataques_panico",
    "q_panico_fisico_enjoo": "q_ataques_panico",
    "q_panico_fisico_calafrio": "q_ataques_panico",
    "q_panico_psicologico": "q_ataques_panico",

    # Bipolaridade (Depende de Humor Umbrella ou de Episódio Maníaco/Hipomaníaco)
    "q_aumento_energia": "q_humor_umbrella",
    "q_mania_duracao": "q_episodio_maniaco",
    "q_autoestima_inflada": "q_humor_umbrella",
    "q_reducao_sono": "q_humor_umbrella",
    "q_loquacidade": "q_humor_umbrella",
    "q_fuga_ideias": "q_humor_umbrella",
    "q_distratibilidade": "q_humor_umbrella",
    "q_risco_excessivo": "q_humor_umbrella",
    "q_bipolar_1_risco_excessivo": "q_humor_umbrella",
    
    # Psicoses (Dependem do Guarda-chuva Psicótico)
    "q_psicotico_duracao_breve": "q_psicotico_umbrella",
    "q_psicotico_retorno_normal": "q_psicotico_umbrella",
    "q_sintomas_negativos": "q_psicotico_umbrella",
    "q_psicotico_duracao_media": "q_psicotico_umbrella",
    "q_psicotico_queda_funcionamento": "q_psicotico_umbrella",
    "q_psicotico_duracao_longa": "q_psicotico_umbrella",
    
    # TOC (Depende de Toc Umbrella ou Obsessoes)
    "q_compulsoes": "q_toc_umbrella",
    "q_tentativa_ignorar_obsessoes": "q_toc_umbrella",
    "q_compulsoes_objetivo": "q_toc_umbrella",
    "q_compulsoes_excessivas": "q_toc_umbrella",
    "q_toc_tempo": "q_toc_umbrella",
    "q_toc_sofrimento": "q_toc_umbrella"
}

for q in data["questions"]:
    q_id = q["id"]
    if q_id in dependencies:
        q["depends_on"] = dependencies[q_id]

with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("V4: Pré-requisitos (depends_on) adicionados com sucesso ao banco de dados.")
