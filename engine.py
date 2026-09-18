import json
import math
from typing import List, Dict, Set, Optional, Tuple

class InferenceEngine:
    def __init__(self, kb_path: str):
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)
        
        self.disorders = self.kb.get("disorders", [])
        self.questions = {q["id"]: q for q in self.kb.get("questions", [])}
        
        # Estado de inferência
        self.active_disorders = {d["id"]: d for d in self.disorders}
        self.scores = {d["id"]: 0.0 for d in self.disorders}
        self.asked_questions = set()
        self.answers = {}  # {q_id: bool}
        
        # Pré-computar total de sintomas (key + secondary) para calcular a pontuação
        self.total_symptoms = {}
        for d in self.disorders:
            total = len(d.get("key_symptoms", [])) + len(d.get("secondary_symptoms", []))
            self.total_symptoms[d["id"]] = total

    def process_answer(self, question_id: str, weight: float):
        """
        Processa a resposta do usuário usando uma escala de peso (0.0 a 1.0).
        0.0 = Nunca (Penalidade)
        > 0.0 = Bônus proporcional à frequência do sintoma.
        """
        self.asked_questions.add(question_id)
        self.answers[question_id] = weight
        
        q_data = self.questions.get(question_id)
        if not q_data:
            return
            
        if weight == 0.0:
            # Resposta 'Nunca': penalidade para não cancelar instantaneamente (soft-pruning)
            for d_id, d in self.active_disorders.items():
                if question_id in d.get("key_symptoms", []):
                    self.scores[d_id] -= 0.15
                elif q_data.get("type") == "umbrella" and d_id in q_data.get("targets", []):
                    self.scores[d_id] -= 0.15
                elif question_id in d.get("secondary_symptoms", []):
                    self.scores[d_id] -= 0.05
        else:
            # Resposta > 0.0: atualizar pontuações multiplicadas pela intensidade
            for d_id, d in self.active_disorders.items():
                if question_id in d.get("key_symptoms", []):
                    self.scores[d_id] += (2.0 * weight) / self.total_symptoms[d_id]
                elif question_id in d.get("secondary_symptoms", []):
                    self.scores[d_id] += (1.2 * weight) / self.total_symptoms[d_id]
                elif q_data.get("type") == "umbrella" and d_id in q_data.get("targets", []):
                    self.scores[d_id] += (0.3 * weight)

    def get_next_question(self) -> Optional[Dict]:
        """
        Calcula a próxima pergunta mesclando Ganho de Informação com "Focus Mode".
        Se alguma doença já estiver se destacando (score alto), o algoritmo
        será 'sugado' para confirmar os sintomas restantes dessa doença.
        """
        if not self.active_disorders:
            return None
            
        remaining_questions = set(self.questions.keys()) - self.asked_questions
        if not remaining_questions:
            return None
            
        # Descobrir o líder atual e sua pontuação
        leader_id = max(self.scores, key=self.scores.get)
        leader_score = self.scores[leader_id]
        
        best_question = None
        max_score = -9999.0
        
        active_ids = set(self.active_disorders.keys())
        total_active = len(active_ids)
        
        for q_id in remaining_questions:
            q_data = self.questions[q_id]
            
            # Checar pré-requisitos lógicos (Árvore de Dependência)
            dependency = q_data.get("depends_on")
            if dependency:
                # Se a pergunta raiz ainda não foi feita, ou se a resposta foi 'Nunca' (0.0), pulamos essa pergunta
                if dependency not in self.answers or self.answers[dependency] == 0.0:
                    continue
            
            targets_in_active = 0
            
            is_leader_question = False
            
            if q_data.get("type") == "umbrella":
                targets = set(q_data.get("targets", []))
                targets_in_active = len(targets.intersection(active_ids))
                if leader_id in targets:
                    is_leader_question = True
            else:
                for d_id in active_ids:
                    d = self.active_disorders[d_id]
                    if q_id in d.get("key_symptoms", []) or q_id in d.get("secondary_symptoms", []):
                        targets_in_active += 1
                        if d_id == leader_id:
                            is_leader_question = True
                        
            if targets_in_active == 0:
                continue
                
            # Probabilidade de a pergunta ser relevante para o conjunto ativo
            p = targets_in_active / total_active
            
            # Cálculo de Entropia base
            if p == 0.0 or p == 1.0:
                entropy = 0.0
            else:
                entropy = - (p * math.log2(p)) - ((1 - p) * math.log2(1 - p))
                
            score = entropy
            
            # Preferência estrutural
            if q_data.get("type") == "umbrella":
                score += 0.01 
                
            # FOCUS MODE REDUZIDO: Se o líder já tem um score positivo relevante, 
            # forçamos o algoritmo a investigar as perguntas do líder, mas com multiplicador bem menor.
            # O peso do foco cresce proporcionalmente ao quão provável o líder está.
            if leader_score > 0.15 and is_leader_question:
                score += (leader_score * 2.0)  # Multiplicador moderado de foco (era 5.0)
                
            if score > max_score:
                max_score = score
                best_question = q_data
                
        return best_question

    def check_stop_conditions(self) -> Tuple[bool, Optional[Dict]]:
        """
        Verifica se atingiu o threshold para alguma doença.
        Aplica trava de cautela: nunca fecha antes de 15 perguntas.
        """
        if not self.active_disorders:
            return True, None
            
        best_disorder_id = max(self.scores, key=self.scores.get)
        best_score = self.scores[best_disorder_id]
        disorder = self.active_disorders[best_disorder_id]
        
        # Trava de cautela: obrigar um mínimo de 15 perguntas investigativas
        if best_score >= disorder.get("threshold", 0.8) and len(self.asked_questions) >= 15:
            return True, disorder
            
        return False, None
