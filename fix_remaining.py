import json
import re

with open('knowledge_base_fixed.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

for q in kb['questions']:
    text = q['text']
    text = text.replace("você já me cortei", "você já se cortou")
    text = text.replace("você se interesso", "você se interessa")
    text = text.replace("você consigo", "você consegue")
    text = text.replace("Você frequentemente suspeito", "Você frequentemente suspeita")
    text = text.replace("quem você realmente sou", "quem você realmente é")
    text = text.replace("meus planos", "seus planos")
    text = text.replace("falam comigo", "falam com você")
    text = text.replace("eu não tendo", "você não tendo")
    text = text.replace("quando eu me ", "quando você se ")
    text = text.replace("eu consigo ", "você consegue ")
    text = text.replace("eu passei ", "você passou ")
    text = text.replace("eu tive ", "você teve ")
    text = text.replace("eu fiquei ", "você ficou ")
    text = text.replace("eu sentia ", "você sentia ")
    text = text.replace("eu queria ", "você queria ")
    
    q['text'] = text

with open('knowledge_base_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(kb, f, indent=2, ensure_ascii=False)
