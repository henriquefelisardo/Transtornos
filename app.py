import streamlit as st
import json
from engine import InferenceEngine

st.set_page_config(page_title="Akinator DSM-5", page_icon="🧠", layout="centered")

def get_engine_state(engine: InferenceEngine):
    return {
        'scores': engine.scores.copy(),
        'asked_questions': engine.asked_questions.copy(),
        'answers': engine.answers.copy()
    }

def restore_engine_state(engine: InferenceEngine, state: dict):
    engine.scores = state['scores'].copy()
    engine.asked_questions = state['asked_questions'].copy()
    engine.answers = state['answers'].copy()

def init_session():
    if "engine" not in st.session_state:
        try:
            st.session_state.engine = InferenceEngine("knowledge_base.json")
        except FileNotFoundError:
            st.error("Erro: O arquivo 'knowledge_base.json' não foi encontrado no diretório atual.")
            st.stop()
    if "history" not in st.session_state:
        st.session_state.history = []
    if "show_log" not in st.session_state:
        st.session_state.show_log = False
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "result" not in st.session_state:
        st.session_state.result = None
    if "started" not in st.session_state:
        st.session_state.started = False

init_session()

def restart_game():
    for key in ["engine", "history", "game_over", "result", "started"]:
        if key in st.session_state:
            del st.session_state[key]
    init_session()

def render_leaderboard():
    if st.session_state.show_log:
        st.sidebar.title("🏆 LEADERBOARD")
        st.sidebar.subheader("Top 5 Diagnósticos")
        engine = st.session_state.engine
        sorted_disorders = sorted(engine.scores.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_disorders[:5]
        
        for i, (d_id, score) in enumerate(top_5):
            name = engine.active_disorders.get(d_id, engine.disorders[0]).get("name", d_id) if d_id in engine.active_disorders else d_id
            if len(name) > 45:
                name = name[:45] + '...'
            st.sidebar.markdown(f"**{i+1}.** {name} ({score:+.2f})")

def print_diagnosis_details(disorder_id: str):
    try:
        with open("disorder_details.json", "r", encoding="utf-8") as f:
            details = json.load(f)
    except FileNotFoundError:
        st.warning("[Aviso] Detalhamento do transtorno não encontrado (disorder_details.json ausente).")
        return

    info = details.get(disorder_id)
    if not info:
        return

    st.markdown("### === DETALHAMENTO CLÍNICO ===")
    
    st.markdown(f"**O que é:** {info.get('descricao', '')}")
    st.markdown(f"**Sintomas Principais:** {info.get('sintomas_principais', '')}")
    st.markdown(f"**Critérios Clínicos:** {info.get('criterios_clinicos', '')}")
    st.markdown(f"**Como Proceder:** {info.get('como_proceder', '')}")
    st.markdown("---")


st.title("🧠 DSM-5 - Inferência Probabilística")

if not st.session_state.started:
    #st.session_state.show_log = st.checkbox("Ativar log de debug (ranking de diagnósticos)?", value=st.session_state.show_log)
    if st.button("Iniciar Teste", use_container_width=True):
        st.session_state.started = True
        st.rerun()

else:
    render_leaderboard()
    
    engine = st.session_state.engine
    max_questions = 50
    
    # Check stop conditions
    if not st.session_state.game_over:
        stop, result = engine.check_stop_conditions()
        if stop or len(st.session_state.history) >= max_questions:
            st.session_state.game_over = True
            st.session_state.result = result

    if st.session_state.game_over:
        result = st.session_state.result
        
        def calculate_percentage(raw_score, disorder_id):
            if raw_score <= 0:
                return 0
                
            d = engine.active_disorders[disorder_id]
            threshold = d.get("threshold", 0.8)
            total_symp = engine.total_symptoms[disorder_id]
            max_possible = 0.0
            
            for q_id, q_data in engine.questions.items():
                if q_id in d.get("key_symptoms", []):
                    max_possible += 2.0 / total_symp
                elif q_id in d.get("secondary_symptoms", []):
                    max_possible += 1.2 / total_symp
                elif q_data.get("type") == "umbrella" and disorder_id in q_data.get("targets", []):
                    max_possible += 0.3
                    
            if max_possible <= threshold:
                max_possible = threshold + 0.5
                
            # Interpolação para tornar a escala mais natural:
            # 0 até threshold -> mapeia de 0 a 80%
            # threshold até max_possible -> mapeia de 80 a 100%
            if raw_score <= threshold:
                pct = (raw_score / threshold) * 80
            else:
                pct = 80 + ((raw_score - threshold) / (max_possible - threshold)) * 20
                
            return min(100, max(0, int(pct)))
            
        def render_scale_explanation():
            with st.expander("ℹ️ Entenda a Escala de Compatibilidade (0 a 100)"):
                st.markdown("""
                A escala mostra a Força de Evidência baseada nos critérios preenchidos:
                
                * **0 a 40%**: Baixa evidência (poucos ou nenhum sintoma).
                * **41 a 79%**: Evidência parcial (traços presentes, mas insuficientes para um diagnóstico clínico firme).
                * **80 a 99%**: Forte evidência (atingiu o limiar diagnóstico do DSM-5).
                * **100%**: Evidência extrema (todos os critérios primários e secundários confirmados com intensidade máxima).
                """)

        if result:
            limit_msg = " NO LIMITE" if len(st.session_state.history) >= max_questions and not engine.check_stop_conditions()[0] else ""
            raw_score = engine.scores[result['id']]
            pct_score = calculate_percentage(raw_score, result['id'])
            
            st.success(f"✅ DIAGNÓSTICO ATINGIDO{limit_msg}: **{result['name']}**")
            st.metric("Índice de Compatibilidade (Sintomas Apresentados)", f"{pct_score}/100")
            render_scale_explanation()
            
            print_diagnosis_details(result['id'])
        else:
            st.error("❌ Diagnóstico inconclusivo, não indicando nenhum transtorno de forma contundente.")
            if engine.active_disorders:
                best_id = max(engine.scores, key=engine.scores.get)
                raw_score = engine.scores[best_id]
                pct_score = calculate_percentage(raw_score, best_id)
                
                st.info(f"**Transtorno mais próximo:** {engine.active_disorders[best_id]['name']}")
                st.metric("Maior Índice de Compatibilidade Alcançado", f"{pct_score}/100")
                render_scale_explanation()
            st.markdown("---")
            
        if st.button("Reiniciar", use_container_width=True):
            restart_game()
            st.rerun()

    else:
        q = engine.get_next_question()
        if not q:
            st.session_state.game_over = True
            st.rerun()
            
        question_count = len(st.session_state.history)
        st.markdown(f"**Pergunta {question_count+1}/{max_questions}**")
        st.progress(question_count / max_questions)
        
        # Define uma altura fixa para a pergunta, garantindo que os botões não fiquem pulando de altura
        st.markdown(
            f"""
            <div style="height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <h3 style="margin: 0;">{q['text']}</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        options = [
            ("Discordo Totalmente", 0.0),
            ("Discordo", 0.25),
            ("Não Sei", 0.5),
            ("Concordo um pouco", 0.75),
            ("Concordo Totalmente", 1.0)
        ]
        
        def handle_answer(weight):
            current_state = get_engine_state(engine)
            st.session_state.history.append(current_state)
            engine.process_answer(q["id"], weight)
            
        def handle_back():
            prev_state = st.session_state.history.pop()
            restore_engine_state(engine, prev_state)
            
        for i, (label, weight) in enumerate(options):
            st.button(label, key=f"btn_{weight}_{q['id']}", use_container_width=True, on_click=handle_answer, args=(weight,))
                
        if question_count > 0:
            st.markdown("---")
            st.button("Voltar", use_container_width=True, on_click=handle_back)



