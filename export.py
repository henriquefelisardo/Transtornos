import json

def export_to_mermaid(kb_path: str, output_path: str):
    """
    Lê a base de conhecimento e exporta a estrutura de conexões
    (transtornos -> sintomas/umbrellas) para um diagrama Mermaid.
    """
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{kb_path}' não encontrado.")
        return
        
    disorders = kb.get("disorders", [])
    questions = {q["id"]: q for q in kb.get("questions", [])}
    
    lines = ["graph TD"]
    
    # Criar nós para os transtornos
    for d in disorders:
        name = d["name"].replace('"', "'")
        lines.append(f'    {d["id"]}["{name}"]')
        
    # Criar nós para as perguntas e conectar
    for q_id, q in questions.items():
        q_text = q["text"].replace('"', "'")
        # Encurtando texto da pergunta para o diagrama não ficar ilegível
        short_text = q_text[:35] + "..." if len(q_text) > 35 else q_text
        lines.append(f'    {q_id}["{short_text}"]')
        
        # Conexões de categorias umbrella para transtornos
        if q.get("type") == "umbrella":
            for target in q.get("targets", []):
                lines.append(f'    {q_id} -->|umbrella| {target}')
                
    # Conexões de transtornos para seus sintomas chave e secundários
    for d in disorders:
        d_id = d["id"]
        for ks in d.get("key_symptoms", []):
            lines.append(f'    {d_id} -->|key_symptom| {ks}')
            
        for ss in d.get("secondary_symptoms", []):
            lines.append(f'    {d_id} -->|secondary_symptom| {ss}')

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"Sucesso: Diagrama Mermaid exportado para '{output_path}'")
    except Exception as e:
        print(f"Erro ao salvar arquivo exportado: {e}")

if __name__ == "__main__":
    export_to_mermaid("knowledge_base.json", "tree.mmd")
