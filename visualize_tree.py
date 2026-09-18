import json
import os
import textwrap

try:
    from pyvis.network import Network
except ImportError:
    print("Erro: A biblioteca 'pyvis' não está instalada.")
    print("Instale usando: pip install pyvis")
    exit(1)

def generate_visualization(kb_path="knowledge_base.json", output_file="tree_visualization.html"):
    if not os.path.exists(kb_path):
        print(f"Erro: Arquivo '{kb_path}' não encontrado no diretório atual.")
        return
        
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
        
    # Inicializa a rede com fundo escuro e fontes claras
    net = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=True)
    
    # Adicionando Transtornos (Nós principais)
    disorders = kb.get("disorders", [])
    for d in disorders:
        d_id = d["id"]
        d_name = d.get("name", d_id)
        # Nomes quebram em várias linhas se forem grandes
        d_title = "<br>".join(textwrap.wrap(d_name, width=30))
        net.add_node(d_id, label=d_id, title=f"<b>TRANSTORNO:</b><br>{d_title}", color="#FF5733", shape="box")
        
    # Adicionando Perguntas (Sintomas / Investigação)
    questions = kb.get("questions", [])
    for q in questions:
        q_id = q["id"]
        q_text = q.get("text", q_id)
        q_title = "<br>".join(textwrap.wrap(q_text, width=40))
        
        # Umbrella tem cor verde, normais tem cor azul
        node_color = "#33FF57" if q.get("type") == "umbrella" else "#33C3FF"
        shape = "ellipse"
        
        net.add_node(q_id, label=q_id, title=f"<b>PERGUNTA ({q_id}):</b><br>{q_title}", color=node_color, shape=shape)
        
        # Conexões baseadas em 'depends_on' (Pergunta Pai -> Pergunta Filha)
        depends = q.get("depends_on")
        if depends:
            net.add_edge(depends, q_id, color="#AAAAAA", title="Depende de")

        # Conexões Umbrella -> Transtornos (Pergunta Umbrella -> Transtorno)
        if q.get("type") == "umbrella":
            for target in q.get("targets", []):
                net.add_edge(q_id, target, color="#33FF57", value=2, title="Alvo Umbrella")

    # Conexões Transtorno -> Sintomas
    # Vamos fazer a seta Pergunta -> Transtorno (O sintoma/pergunta aponta para a doença)
    for d in disorders:
        d_id = d["id"]
        
        for ks in d.get("key_symptoms", []):
            net.add_edge(ks, d_id, color="#FF5733", value=3, title="Sintoma Chave")
            
        for ss in d.get("secondary_symptoms", []):
            net.add_edge(ss, d_id, color="#FFC300", value=1, title="Sintoma Secundário")
            
    # Configurações de física para organizar a árvore
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    # Salva o arquivo HTML
    net.write_html(output_file)
    print(f"✅ Visualização gerada com sucesso: {output_file}")
    print("Abra este arquivo no seu navegador (ex: Chrome, Edge, Firefox) para visualizar e interagir com o grafo.")

if __name__ == "__main__":
    generate_visualization()
