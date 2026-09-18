import json

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    "q_borderline_impulsividade": "Você age por impulso em áreas que podem te prejudicar seriamente? (Ex: gastar dinheiro sem ter, comer compulsivamente até passar mal, abuso de álcool/drogas, sexo irresponsável ou direção perigosa).",
    "q_borderline_abandono": "Você faz esforços desesperados e até exagerados para evitar ser abandonado, seja de forma real ou imaginária? (Ex: implorar, ameaçar se machucar ou entrar em pânico extremo se alguém demorar a responder ou desmarcar um encontro).",
    "q_borderline_instabilidade": "Seu humor muda de forma muito brusca e intensa no mesmo dia, indo de uma alegria normal para uma raiva, ansiedade ou tristeza paralisante em questão de horas?",
    "q_delirios": "Você costuma ter crenças muito fixas e inflexíveis, mesmo quando as outras pessoas dizem e provam ser irreais? (Ex: achar que está sendo perseguido, que há complôs contra você, ou que consegue ler a mente dos outros).",
    "q_tdah_desatencao": "Você tem dificuldade crônica de manter o foco em tarefas não estimulantes? (Ex: comete erros por descuido, perde chaves/celular com frequência, sua mente 'viaja' ou parece que não escuta quando falam diretamente com você).",
    "q_tdah_padrao": "Você costuma deixar tarefas pela metade, pular de um interesse para outro rapidamente e lutar muito contra o tédio para terminar obrigações diárias (como ler um texto longo ou organizar o quarto)?",
    "q_evitativa_inibicao": "Você evita ao máximo situações sociais, fazer novos amigos ou aceitar promoções no trabalho por um medo intenso de ser criticado, rejeitado ou passar vergonha?",
    "q_ansiedade_excessiva": "Você tem preocupações constantes e uma expectativa ruim de que o pior vai acontecer com várias coisas do dia a dia (trabalho, saúde, família), de uma forma que te deixa paralisado?",
    "q_tea_comunicacao": "Você frequentemente acha difícil entender o tom de voz das pessoas, ironias, ou percebe que os outros te acham 'grosseiro(a)' ou 'estranho(a)' nas conversas, mesmo você não tendo a intenção?",
    "q_toc_compulsoes": "Você sente necessidade incontrolável de repetir ações ou rituais físicos/mentais (como lavar as mãos, conferir portas, contar mentalmente ou alinhar coisas) para aliviar uma aflição ou evitar algo ruim?",
    "q_bipolar_1_risco_excessivo": "Você já teve fases onde tomou atitudes por forte impulso, assumindo riscos absurdos que normalmente não faria? (Ex: compras extravagantes, investimentos insensatos, pedir demissão sem plano ou indiscrições sexuais).",
    "q_depressivo_maior_perda_interesse": "Você perdeu quase todo o interesse, a motivação ou o prazer até nas atividades e hobbies que antes você gostava muito? (Anedonia).",
    "q_antissocial_violacao": "Você tem um padrão de desconsiderar e violar os direitos das outras pessoas? (Ex: mentir repetidamente para obter vantagem, agir impulsivamente sem ligar para a segurança dos outros, ou ter comportamentos que são motivos de prisão)."
}

for q in data["questions"]:
    if q["id"] in replacements:
        q["text"] = replacements[q["id"]]

with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Textos das perguntas atualizados com descrições do DSM-5.")
