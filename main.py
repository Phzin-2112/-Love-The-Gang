import random
import time # Adicionado para pausas dramáticas
 
print("🎮 Bem-vindo ao Vida de Bairro, mano! Se prepara pra vida na quebrada!\n")
 
# Nome da gangue
gangue = input("Manda o nome da tua gangue, maluco: ").strip()

# Repete enquanto o usuário digitar vazio ou apenas espaços
while not gangue:
    gangue = input("Sua gangue tem que ter um nome, bro! Fala aí: ").strip()

print(f"\nBoa! Sua gangue '{gangue}' vai dominar a quebrada, parceiro!\n")

 
escolhi = input("Qual teu vulgo na quebrada? ")
print(f"\nAí sim, {escolhi}! Tamo junto!\n")
 
# Criação do personagem
print("Escolhe tua faixa etária, mano:")
print("1. Criança (0-12 anos)\n2. Jovem (13-20 anos)\n3. Adulto (21-59 anos)\n4. Idoso (60+ anos)")
faixa_etaria = input("> ")
while faixa_etaria not in ["1", "2", "3", "4"]:
    faixa_etaria = input("Opção inválida, parça. Manda de novo (1-4): ")
 
 
print("\nEscolhe tua cor de pele (vai definir a dificuldade do rolê):")
print("1. Branca (Fácil)\n2. Amarela (Média)\n3. Parda (Difícil)\n4. Negra (Muito difícil)")
cor_pele = input("> ")
while cor_pele not in ["1", "2", "3", "4"]:
    cor_pele = input("Opção inválida, truta. Manda de novo (1-4): ")
 
 
# Dificuldade pelo tom de pele
dificuldade = {
    "1": 1.0, # Fácil
    "2": 1.2, # Média
    "3": 1.8, # Difícil
    "4": 2.2  # Muito Difícil
}
mult = dificuldade.get(cor_pele, 1.0)
 
# Player inicial
player = {
    "nome": escolhi,
    "dinheiro": int(150 / mult),
    "fome": 30,
    "respeito": int(25 / mult),
    "saude": int(100 / mult),
    "inteligencia": 10, # Novo atributo
    "tempo_total": 0,  # horas acumuladas, 0 = 8h da manhã do dia 1
    "faixa_etaria": faixa_etaria,
    "cor_pele": cor_pele,
    "gangue": gangue,
    "fadiga": 0,
    "prisao": False,
    "dias_preso": 0,
}
 
# Constantes
MAX_FOME = 100
MAX_SAUDE = 100
MAX_FADIGA = 100
MAX_RESPEITO = 200 # Defina um teto para o respeito, se quiser
MIN_RESPEITO_GAME_OVER = -50
MIN_DINHEIRO_GAME_OVER = -200
HORAS_ACORDAR = 8
 
# --- Funções Auxiliares ---
def mostrar_hora():
    hora_do_dia = (player["tempo_total"] + HORAS_ACORDAR) % 24
    minuto_do_dia = int(((player["tempo_total"] + HORAS_ACORDAR) % 1) * 60) # Para horas fracionadas
    print(f"🕗 Tá na rua agora: {int(hora_do_dia):02d}h{minuto_do_dia:02d}")
 
def mostrar_status():
    cores = {"1": "Branca", "2": "Amarela", "3": "Parda", "4": "Negra"}
    idades = {"1": "Criança", "2": "Jovem", "3": "Adulto", "4": "Idoso"}
 
    print(f"\n--- STATUS DE {player['nome'].upper()} ---")
    print(f"🌇 Dia {int(player['tempo_total'] // 24) + 1} na quebrada")
    mostrar_hora()
    print(f"🛡️ Gangue: {player['gangue']}")
    # print(f"👤 Vulgo: {player['nome']}") # Já está no título do status
    print(f"🎂 Faixa Etária: {idades.get(player['faixa_etaria'], 'Desconhecida')}")
    print(f"🎨 Cor da Pele: {cores.get(player['cor_pele'], 'Desconhecida')} (Mult: {mult}x)")
    print(f"💰 Dinheiro: R${player['dinheiro']:.2f}")
    print(f"🍖 Fome: {player['fome']}/{MAX_FOME}")
    print(f"💪 Respeito: {player['respeito']}/{MAX_RESPEITO}")
    print(f"❤️ Saúde: {player['saude']}/{MAX_SAUDE}")
    print(f"🧠 Inteligência: {player['inteligencia']}")
    print(f"😩 Fadiga: {player['fadiga']}/{MAX_FADIGA}")
    if player["prisao"]:
        print(f"⚠️ TÁ PRESO, MANO! Faltam {player['dias_preso']} dia(s) de pena ou desenrola essa situação.")
    print("-------------------------\n")
 
def avancar_tempo(horas):
    player["tempo_total"] += horas
    player["fome"] = min(MAX_FOME, player["fome"] + int(horas * 2.5)) # Fome aumenta com o tempo
    player["fadiga"] = min(MAX_FADIGA, player["fadiga"] + int(horas * 2)) # Fadiga aumenta
    # A cada 24h de jogo, chance de mudar de faixa etária (simplificado)
    # if player["tempo_total"] % (24*365) == 0 and player["tempo_total"] > 0 : # A cada ano
        # print("FELIZ ANIVERSÁRIO! Você está mais velho!")
        # Poderia adicionar lógica de envelhecimento aqui
 
def checar_condicoes_perigo():
    if player["fome"] >= 95:
        player["saude"] -= 15
        print("❗ FOME CRÍTICA! Sua saúde está se esvaindo rapidamente!")
    elif player["fome"] >= 80:
        player["saude"] -= 5
        player["respeito"] -=2
        print("😖 Tá com fome braba, isso tá te fazendo mal e te deixando sem moral...")
 
    if player["fadiga"] >= 95:
        player["saude"] -= 10
        print("❗ FADIGA EXTREMA! Você está à beira de um colapso!")
    elif player["fadiga"] >= 80:
        player["respeito"] -= 5
        player["saude"] -=3
        print("😴 Tá cansado demais, tá perdendo respeito e saúde na rua...")
 
    if player["saude"] <= 0:
        print("\n☠️ GAME OVER ☠️")
        print("Você não aguentou o trampo da vida e virou saudade na quebrada.")
        print(f"Viveu por {int(player['tempo_total'] // 24) + 1} dias. Descanse em paz, {player['nome']}.")
        exit()
    if player["respeito"] <= MIN_RESPEITO_GAME_OVER:
        print("\n☠️ GAME OVER ☠️")
        print("Seu respeito chegou no fundo do poço. Ninguém mais te leva a sério na quebrada.")
        print("Você foi esquecido.")
        exit()
    if player["dinheiro"] <= MIN_DINHEIRO_GAME_OVER:
        print("\n☠️ GAME OVER ☠️")
        print("As dívidas te engoliram, mano. Agiotas e cobradores te acharam.")
        print("Não tem mais pra onde correr.")
        exit()
    # Condição de vitória simples
    if player["dinheiro"] >= 10000 and player["respeito"] >= 150:
        print("\n🏆 VOCÊ VENCEU, CAMPEÃO! 🏆")
        print(f"Parabéns, {player['nome']}! Você se tornou uma lenda da quebrada {player['gangue']}!")
        print(f"Com R${player['dinheiro']:.2f} no bolso e {player['respeito']} de respeito, você é o rei do bairro!")
        print("Agora pode curtir a vida boa... ou continuar dominando!")
        exit()
 
 
def dormir():
    print("\nVai descansar que o corre é forte... zzz 💤")
    hora_atual_no_dia = (player["tempo_total"] + HORAS_ACORDAR) % 24
   
    if hora_atual_no_dia < HORAS_ACORDAR : # Se já for madrugada/manhã antes das 8h
        horas_para_dormir = HORAS_ACORDAR - hora_atual_no_dia
    else: # Se for depois das 8h
        horas_para_dormir = (24 - hora_atual_no_dia) + HORAS_ACORDAR
 
    player["tempo_total"] += horas_para_dormir
    player["fome"] = min(MAX_FOME, player["fome"] + 20) # Acorda com um pouco mais de fome
    player["saude"] = min(MAX_SAUDE, player["saude"] + int(60 / mult) + (player["inteligencia"] // 5) ) # Inteligência ajuda a descansar melhor
    player["fadiga"] = max(0, player["fadiga"] - 80)
 
    # Limites
    player["fome"] = min(MAX_FOME, max(0, player["fome"]))
    player["saude"] = min(MAX_SAUDE, max(0, player["saude"]))
 
    print(f"Você acordou às {HORAS_ACORDAR}h do dia seguinte, mais disposto!")
    time.sleep(1)
 
def comer_algo():
    print("\n--- HORA DO RANGO ---")
    print("O que vai querer matar a fome?")
    print("1. Salgado da tia (R$5, -15 Fome, +5 Saúde) [0.5h]")
    print("2. PF no boteco (R$15, -40 Fome, +10 Saúde, +2 Respeito) [1h]")
    print("3. Marmita caprichada (R$25, -60 Fome, +20 Saúde, +5 Respeito) [1h]")
    print("4. Voltar (não comer nada)")
    escolha_comida = input("> ")
 
    horas_comer = 0
    custo = 0
    fome_menos = 0
    saude_mais = 0
    respeito_mais = 0
 
    if escolha_comida == "1":
        custo, fome_menos, saude_mais, horas_comer = 5, 15, 5, 0.5
        print("Mandou pra dentro um salgado que tava na estufa...")
    elif escolha_comida == "2":
        custo, fome_menos, saude_mais, respeito_mais, horas_comer = 15, 40, 10, 2, 1
        print("Bateu aquele PF responsa no boteco da esquina!")
    elif escolha_comida == "3":
        custo, fome_menos, saude_mais, respeito_mais, horas_comer = 25, 60, 20, 5, 1
        print(" rango caprichado, hein? Deu até uma moral!")
    elif escolha_comida == "4":
        print("Deixou pra depois... a fome espera.")
        return
    else:
        print("Opção de rango inválida.")
        return
 
    if player["dinheiro"] >= custo:
        player["dinheiro"] -= custo
        player["fome"] = max(0, player["fome"] - fome_menos)
        player["saude"] = min(MAX_SAUDE, player["saude"] + saude_mais)
        player["respeito"] += respeito_mais
        player["fadiga"] = min(MAX_FADIGA, player["fadiga"] + 5) # Comer cansa um tiquinho
        avancar_tempo(horas_comer)
        print(f"Fome: -{fome_menos}, Saúde: +{saude_mais}. Você gastou R${custo:.2f}.")
    else:
        print("Tá sem din pra esse rango, parça. Faz um corre primeiro.")
    time.sleep(1.5)
 
 
def ir_ao_postinho():
    horas = 2
    custo_base = 50
    if player["faixa_etaria"] == "4": # Idoso paga menos
        custo = custo_base / 2
        print(f"\n🚑 Indo dar um confere na saúde no postinho... Idoso tem desconto! (Custo: R${custo:.2f}) [{horas}h]")
    else:
        custo = custo_base
        print(f"\n🚑 Indo dar um confere na saúde no postinho... (Custo: R${custo:.2f}) [{horas}h]")
 
    if player["dinheiro"] >= custo:
        player["dinheiro"] -= custo
        recupera_saude = random.randint(20, int(50 / mult))
        player["saude"] = min(MAX_SAUDE, player["saude"] + recupera_saude)
        print(f"Os médicos te deram um trato. Saúde recuperada em +{recupera_saude} pontos.")
        avancar_tempo(horas)
    else:
        print("Sem grana pra consulta, mano. Melhor se cuidar de outro jeito ou aguentar a dor.")
    time.sleep(1.5)
 
# --- Eventos Aleatórios ---
def evento_aleatorio():
    # Chance de evento na quebrada rolar a cada ação
    chance = random.randint(1, 100)
    if chance <= 25 and not player["prisao"]: # Aumentei a chance de evento
        print("\n✨ ALGO INESPERADO ACONTECEU NA QUEBRADA! ✨")
        time.sleep(1)
        eventos = ["briga", "furto", "amizade", "prisao_evento", "batida_policial", "oportunidade_trampo", "doenca", "festa"]
        evento = random.choice(eventos)
 
        if evento == "briga":
            print("⚔️ Ih, rapaz! Arrumaram caô contigo na rua e te chamaram pra briga.")
            resultado = random.choice(["ganhou", "perdeu", "empatou"])
            if resultado == "ganhou":
                player["respeito"] += int(20 / mult)
                player["saude"] -= random.randint(5, 15)
                player["fadiga"] += 10
                print("Você meteu a mão e ganhou a treta! Ganhou respeito, mas saiu arranhado.")
            elif resultado == "perdeu":
                player["respeito"] -= int(15 * mult)
                player["saude"] -= random.randint(15, 30)
                player["fadiga"] += 20
                print("Que pena! Você tomou um atraso e perdeu respeito. Tá todo quebrado!")
            else:
                player["respeito"] += 5
                player["saude"] -= 5
                player["fadiga"] += 5
                print("A briga foi tensa, mas ninguém caiu. Saiu no zero a zero, mas ganhou uma moralzinha.")
 
        elif evento == "furto":
            print("🚨 Vacilou, perdeu! Tentaram te roubar na mão grande.")
            if player["dinheiro"] > 0:
                perda = random.randint(10, min(int(player["dinheiro"] * 0.3), 100)) # Perde até 30% ou 100
                player["dinheiro"] -= perda
                player["respeito"] -= 5
                print(f"Moscou e levaram R${perda:.2f} seu. Menos umas moral também.")
            else:
                print("Mas você já tava zerado, os maluco saíram de mão abanando. Ufa!")
 
        elif evento == "amizade":
            print("🤝 Um camarada gente fina da quebrada te deu uma ajuda!")
            tipo_ajuda = random.choice(["dinheiro", "moral", "dica"])
            if tipo_ajuda == "dinheiro":
                ganho = random.randint(int(20/mult), int(80/mult))
                player["dinheiro"] += ganho
                player["respeito"] += 5
                print(f"Ele te adiantou R${ganho:.2f} e ainda te deu moral.")
            elif tipo_ajuda == "moral":
                player["respeito"] += 15
                player["fome"] = max(0, player["fome"] - 10)
                print("Ele te pagou um lanche e trocou uma ideia responsa. Respeito aumentou!")
            else: # dica
                player["inteligencia"] += 2
                print("Ele te deu uma dica quente sobre os esquemas da área. Sua malandragem aumentou.")
 
 
        elif evento == "prisao_evento": # Renomeado para evitar conflito com player["prisao"]
            # Só pega se estiver com pouco respeito ou muito azar
            if player["respeito"] < (15 * mult) or random.randint(1,100) < 10:
                print("\n🚔 SUJOU! A polícia te enquadrou e achou motivo pra te levar!")
                print("Motivo: Vadiagem / Atitude suspeita / Tava no lugar errado na hora errada.")
                player["prisao"] = True
                player["dias_preso"] = random.randint(2, 5) # Pena em dias
                player["respeito"] -= 20
                print(f"Você vai passar uns {player['dias_preso']} dias vendo o sol nascer quadrado.")
            else:
                print("\n🚔 A polícia deu uma geral, mas você tava na moral e te liberaram.")
                player["respeito"] += 2 # Ganha um pouco por ser desenrolado
 
        elif evento == "batida_policial":
            print("\n🚓 OPERAÇÃO POLICIAL NA ÁREA! CORRE OU ENCARA?")
            acao_batida = input("1. Tentar se esconder (discreto)\n2. Sair de fininho (arriscado)\n3. Encarar e ser revistado (moral)\n> ")
            if acao_batida == "1":
                if random.randint(1,100) > 40 - (player["inteligencia"]//2) : # Inteligência ajuda
                    print("Você achou um bom esconderijo e esperou a poeira baixar. Ufa!")
                    avancar_tempo(0.5)
                else:
                    print("Não deu! Te acharam escondido e tomaram um dinheiro pra te liberar.")
                    perda = random.randint(10, max(10,int(player["dinheiro"]*0.2)))
                    player["dinheiro"] -= perda
                    player["respeito"] -=5
                    print(f"Perdeu R${perda:.2f}.")
                    avancar_tempo(1)
            elif acao_batida == "2":
                if random.randint(1,100) > 60:
                    print("Você foi mais rápido que eles e conseguiu vazar sem ser visto!")
                    player["respeito"] +=5
                    avancar_tempo(0.5)
                else:
                    print("Te pegaram tentando fugir! Agora a coisa ficou feia...")
                    player["saude"] -= 10
                    player["respeito"] -=15
                    if player["dinheiro"] > 20:
                        player["dinheiro"] -= 20 # Multa informal
                        print("Ainda levaram uma parte da sua grana.")
                    player["prisao"] = True
                    player["dias_preso"] = random.randint(1,3)
                    avancar_tempo(1)
            else:
                print("Você encarou a revista. Os policiais foram truculentos mas te liberaram.")
                player["respeito"] += 5 # Ganhou moral por não dever
                player["saude"] -= random.randint(0,5) # Podem ter sido um pouco brutos
                avancar_tempo(1)
 
        elif evento == "oportunidade_trampo":
            print("💡 PINTA UMA CHANCE DE TRAMPO RÁPIDO!")
            aceita = input("Um conhecido te ofereceu um bico. Paga bem, mas é corrido. Aceita? (s/n): ")
            if aceita.lower() == 's':
                horas_trampo = random.randint(3,6)
                ganho_trampo = int(random.randint(50,150) / mult)
                print(f"Você ralou por {horas_trampo} horas e fez R${ganho_trampo:.2f}!")
                player["dinheiro"] += ganho_trampo
                player["fadiga"] += horas_trampo * 5
                player["respeito"] += 5
                avancar_tempo(horas_trampo)
            else:
                print("Deixou passar a oportunidade. Quem sabe na próxima.")
 
        elif evento == "doenca":
            print("🤒 XI... Parece que você pegou uma zica braba.")
            player["saude"] -= random.randint(15, int(30 * mult)) # Doença afeta mais os mais vulneráveis
            player["fadiga"] += 20
            print("Sua saúde caiu e você tá se sentindo mal. Melhor se cuidar!")
 
        elif evento == "festa":
            print("🎉 É FESTA NA QUEBRADA! Som estralando e a galera reunida!")
            participar = input("Vai colar pra curtir e socializar? (s/n): ")
            if participar.lower() == 's':
                custo_festa = random.randint(10, int(50*mult))
                if player["dinheiro"] >= custo_festa:
                    player["dinheiro"] -= custo_festa
                    player["respeito"] += random.randint(10,25)
                    player["fadiga"] += random.randint(15,30)
                    player["fome"] += 10 # Come e bebe na festa
                    avancar_tempo(random.randint(3,6))
                    print(f"Você curtiu a noite, gastou R${custo_festa:.2f}, ganhou moral mas tá cansado!")
                else:
                    print("Queria ir, mas tá sem din pra bancar a entrada/consumo.")
            else:
                print("Preferiu ficar em casa dessa vez.")
        time.sleep(1)
    # Limpar status negativos se recuperado
    if player["fome"] < 0: player["fome"] = 0
    if player["saude"] < 0: player["saude"] = 0 # Game over será checado depois
    if player["saude"] > MAX_SAUDE: player["saude"] = MAX_SAUDE
    if player["fadiga"] < 0: player["fadiga"] = 0
    if player["respeito"] > MAX_RESPEITO: player["respeito"] = MAX_RESPEITO
 
 
# --- Ações do Jogador ---
def mostrar_opcoes():
    print("--- SUAS OPÇÕES NA QUEBRADA ---")
    if player["prisao"]:
        print("1. Cumprir a pena restante (passa os dias)")
        print("2. Tentar subornar um guarda (R$100, arriscado)")
        print(f"3. Pagar advogado (R${150 + player['dias_preso']*50:.2f}, chance alta de reduzir pena ou sair)") # Custo varia
        print("4. Tentar fugir (risco MUITO alto!)")
        return
 
    # Opções Comuns a quase todos (exceto se especificado)
    print("0. Comer Algo")
    if player["saude"] < 70 :
        print("H. Ir ao Postinho (cuidar da saúde)")
 
    if player["faixa_etaria"] == "1":  # Criança
        print("1. Estudar na escola do bairro (3h, +Respeito, +Inteligência)")
        print("2. Brincar na rua (2h, +Respeito, -Fome leve)")
        print("3. Fazer um pequeno corre (catar latinha/papelão) (2h, +Dinheiro pouco, -Respeito)")
        print("4. Pedir dinheiro na rua (1h, +Dinheiro mínimo, --Respeito)")
        print("D. Dormir (pula até 8h do dia seguinte)")
    elif player["faixa_etaria"] == "2":  # Jovem
        print("1. Estudar na escola/curso (4h, +Respeito, ++Inteligência)")
        print("2. Malhar na praça/academia improvisada (2h, +Saúde, +Respeito)")
        print("3. Procurar trampo (bico) (3h, chance de ganhar Dinheiro)")
        print("4. Sair pro rolê com a galera (4h, +Respeito, -Dinheiro)")
        print("5. Fazer um corre ilegal (pequeno furto) (2h, arriscado, pode dar B.O.)")
        print("6. Grafite (Arte de Rua) (3h, +/-Respeito, pode dar B.O)")
        print("D. Dormir (pula até 8h do dia seguinte)")
    elif player["faixa_etaria"] == "3":  # Adulto
        print("1. Trabalhar na firma (registrado ou não) (8h, ++Dinheiro, --Saúde)")
        print("2. Estudar (curso técnico/faculdade) (4h, +Respeito, +++Inteligência)")
        print("3. Fazer um bico (freela) (3-6h, +Dinheiro)")
        print("4. Cuidar da família/casa (3h, +Respeito, -Fadiga leve)")
        print("5. Jogar futebol/socializar com a galera (2h, +Respeito, +Saúde)")
        print("D. Dormir (pula até 8h do dia seguinte)")
    elif player["faixa_etaria"] == "4":  # Idoso
        print("1. Exercício leve na praça (1h, +Saúde, -Fadiga)")
        print("2. Ir no médico (rotina) (2h, +Saúde / descobre problema)") # Já tem o 'H' pro postinho
        print("3. Contar causos/jogar dominó na praça (2h, +Respeito)")
        print("4. Cuidar dos netos/jardim (3h, +Respeito, -Fadiga leve)")
        print("D. Dormir (pula até 8h do dia seguinte)")
 
def executar_acao(escolha):
    horas = 0
    if player["prisao"]:
        if escolha == "1":
            print(f"Você decidiu esperar a pena passar... Dias restantes: {player['dias_preso']}")
            while player['dias_preso'] > 0:
                avancar_tempo(24) # Passa um dia
                player["fome"] = min(MAX_FOME, player["fome"] + 30) # Comida da prisão é ruim
                player["saude"] = max(0, player["saude"] - 5)    # Condições ruins
                player["fadiga"] = min(MAX_FADIGA, player["fadiga"] + 10)
                player['dias_preso'] -=1
                print(f"Mais um dia se foi na cela... faltam {player['dias_preso']}.")
                time.sleep(0.5)
            player["prisao"] = False
            player["respeito"] -= 10 # Sair da prisão não te dá moral automaticamente
            print("Finalmente livre! Mas a experiência te marcou.")
        elif escolha == "2":
            custo_suborno = 100
            print(f"Tentando desenrolar com o guarda... (custo: R${custo_suborno:.2f})")
            if player["dinheiro"] >= custo_suborno:
                player["dinheiro"] -= custo_suborno
                if random.randint(1,100) > (60 - player["inteligencia"]//2): # Inteligência ajuda
                    print("O guarda aceitou a grana e fez vista grossa! Você tá livre!")
                    player["prisao"] = False
                    player["dias_preso"] = 0
                    player["respeito"] -= 25 # Perdeu moral por subornar
                else:
                    print("O guarda não só recusou como aumentou sua pena! Vacilou!")
                    player["dias_preso"] += 2
                    player["respeito"] -= 10
            else:
                print("Sem grana pra tentar o suborno, parceiro.")
        elif escolha == "3":
            custo_advogado = 150 + player['dias_preso']*50
            print(f"Contratando um advogado da quebrada... (custo: R${custo_advogado:.2f})")
            if player["dinheiro"] >= custo_advogado:
                player["dinheiro"] -= custo_advogado
                player["inteligencia"] +=1 # Aprendeu algo com o processo
                if random.randint(1,100) > (40 - player["inteligencia"]): # Inteligência é chave
                    reducao_pena = random.randint(1, player["dias_preso"])
                    player["dias_preso"] -= reducao_pena
                    print(f"O advogado conseguiu reduzir sua pena em {reducao_pena} dia(s)!")
                    if player["dias_preso"] <= 0:
                        player["prisao"] = False
                        player["dias_preso"] = 0
                        print("E com isso, você está livre! O advogado era bom mesmo.")
                        player["respeito"] += 5
                else:
                    print("O advogado tentou, mas não conseguiu nada. Dinheiro jogado fora.")
                    player["respeito"] -=5
            else:
                print("Sem grana pro advogado, vai ter que ser na raça.")
        elif escolha == "4":
            print("Tentando uma fuga cinematográfica... Isso é loucura!")
            time.sleep(1)
            if random.randint(1,100) > (90 - player["inteligencia"]//3) : # Quase impossível
                print("INACREDITÁVEL! Você conseguiu fugir! Agora é um foragido!")
                player["prisao"] = False
                player["dias_preso"] = 0
                player["respeito"] += 50 # Feito histórico
                player["saude"] -= 30 # Saiu quebrado
                player["fadiga"] = MAX_FADIGA
                # Poderia adicionar status "Foragido" que atrai polícia
            else:
                print("Você foi pego na tentativa de fuga! Agora sim sua situação piorou.")
                player["saude"] -= 40
                player["fadiga"] += 60
                player["dias_preso"] += random.randint(3,7)
                player["respeito"] -= 30
                print(f"Pena aumentada e você tá todo arrebentado.")
        else:
            print("Opção inválida na prisão.")
        avancar_tempo(1) # Ação na prisão gasta um tempo mínimo
        return
 
    # Ações comuns
    if escolha.upper() == "D":
        dormir()
        return
    elif escolha.upper() == "0":
        comer_algo()
        return
    elif escolha.upper() == "H" and player["saude"] < 70:
        ir_ao_postinho()
        return
    elif escolha.upper() == "H" and player["saude"] >= 70:
        print("Você tá bem de saúde, não precisa de médico agora.")
        return
 
 
    # Ações por Faixa Etária
    if player["faixa_etaria"] == "1":  # Criança
        if escolha == "1":
            horas = 3
            print(f"Você foi pra escola e tentou aprender algo por {horas} horas.")
            player["inteligencia"] += random.randint(1,3)
            player["respeito"] += 5
            player["fadiga"] += 15
        elif escolha == "2":
            horas = 2
            print(f"Você brincou na rua com os outros pivetes por {horas} horas.")
            player["respeito"] += 7
            player["fome"] = max(0, player["fome"] - 5) # Brincar abre o apetite mas se diverte
            player["saude"] += 2
            player["fadiga"] += 10
        elif escolha == "3":
            horas = 2
            ganho = random.randint(5, int(15/mult))
            print(f"Você catou material reciclável por {horas} horas e fez R${ganho:.2f}.")
            player["dinheiro"] += ganho
            player["respeito"] -= 2 # Trabalho infantil não é bem visto por todos
            player["fadiga"] += 20
            player["saude"] -= 3
        elif escolha == "4":
            horas = 1
            ganho = random.randint(1, int(5/mult))
            print(f"Você pediu uns trocados no farol por {horas}h e conseguiu R${ganho:.2f}.")
            player["dinheiro"] += ganho
            player["respeito"] -= 5
            player["fadiga"] += 5
        else:
            print("Opção de pivete inválida, menor.")
            return
 
    elif player["faixa_etaria"] == "2":  # Jovem
        if escolha == "1":
            horas = 4
            print(f"Você se dedicou aos estudos por {horas} horas.")
            player["inteligencia"] += random.randint(2,5)
            player["respeito"] += 10
            player["fadiga"] += 20
        elif escolha == "2":
            horas = 2
            print(f"Você puxou ferro na academia da praça por {horas} horas. Tá ficando monstro!")
            player["saude"] = min(MAX_SAUDE, player["saude"] + random.randint(5,10))
            player["respeito"] += 5
            player["fadiga"] += 25
        elif escolha == "3":
            horas = 3
            print(f"Você saiu pra procurar um trampo por {horas} horas...")
            if random.randint(1,100) > (60 - player["inteligencia"]//2) : # Inteligência ajuda
                ganho_bico = random.randint(int(30/mult), int(80/mult))
                print(f"Conseguiu um bico rápido e levantou R${ganho_bico:.2f}!")
                player["dinheiro"] += ganho_bico
                player["respeito"] += 5
            else:
                print("Não pintou nada dessa vez... continue tentando.")
            player["fadiga"] += 15
        elif escolha == "4":
            horas = 4
            custo_role = random.randint(int(10*mult), int(30*mult))
            print(f"Você colou no rolê com a galera por {horas} horas.")
            if player["dinheiro"] >= custo_role:
                player["dinheiro"] -= custo_role
                player["respeito"] += 15
                player["fadiga"] += 25
                print(f"Gastou R${custo_role:.2f}, mas fortaleceu as amizades.")
            else:
                print("Queria ir pro rolê mas tá sem din pra acompanhar.")
                player["respeito"] -=5 # Fica mal com a galera
        elif escolha == "5": # Corre ilegal
            horas = 2
            print("Você foi tentar um corre arriscado (pequeno furto)...")
            time.sleep(1)
            # Chance de sucesso depende da inteligência e um pouco de sorte, e do multiplicador de dificuldade
            if random.randint(1,100) > (50 + (10 * mult) - player["inteligencia"]):
                ganho = random.randint(int(50/mult), int(150/mult))
                print(f"Deu bom! Você conseguiu R${ganho:.2f} no esquema e não foi pego.")
                player["dinheiro"] += ganho
                player["respeito"] += 5 # Entre os seus...
                player["fadiga"] += 20
            else:
                print("DEU RUIM! Você foi pego no pulo!")
                player["saude"] -= random.randint(10,20) # Pode apanhar
                player["respeito"] -= 25
                player["prisao"] = True
                player["dias_preso"] = random.randint(2,7)
                print(f"Além de perder moral, vai amargar uns dias na prisão.")
            player["fadiga"] += 30 # Mesmo que dê certo, é tenso
        elif escolha == "6": # Grafite
            horas = 3
            print(f"Você foi expressar sua arte nos muros da quebrada por {horas} horas...")
            if random.randint(1,100) > (70 - player["inteligencia"]): # Inteligência/talento
                player["respeito"] += random.randint(10,20)
                print("Sua arte foi reconhecida pela comunidade! Ganhou respeito.")
            else:
                if random.randint(1,100) < 30:
                    print("A polícia te pegou pichando! Consideraram vandalismo.")
                    player["respeito"] -= 10
                    player["prisao"] = True
                    player["dias_preso"] = 1
                    print("Vai passar uma noite na delegacia pra aprender.")
                else:
                    print("Ninguém deu muita bola pro seu grafite dessa vez...")
                    player["respeito"] += 1
            player["fadiga"] += 15
        else:
            print("Opção de jovem inválida, truta.")
            return
 
    elif player["faixa_etaria"] == "3":  # Adulto
        if escolha == "1":
            horas = 8
            salario_dia = random.randint(int(200/mult), int(390/mult))
            print(f"Mais um dia de trampo honesto (ou nem tanto) por {horas} horas. Fez R${salario_dia:.2f}.")
            player["dinheiro"] += salario_dia
            player["saude"] -= 10 # Trabalho desgasta
            player["respeito"] += 5 # Provedor
            player["fadiga"] += 50
        elif escolha == "2":
            horas = 4
            print(f"Você investiu no futuro e estudou por {horas} horas.")
            player["inteligencia"] += random.randint(3,7)
            player["respeito"] += 15
            player["fadiga"] += 30
        elif escolha == "3": # Bico
            horas_bico = random.randint(3,6)
            ganho_bico = random.randint(int(40/mult) * (horas_bico//2), int(100/mult)* (horas_bico//2) )
            print(f"Fez um bico por {horas_bico} horas e levantou R${ganho_bico:.2f}.")
            player["dinheiro"] += ganho_bico
            player["fadiga"] += horas_bico * 6
        elif escolha == "4":
            horas = 3
            print(f"Você dedicou tempo à família e à casa por {horas} horas.")
            player["respeito"] += 10
            player["fadiga"] = max(0, player["fadiga"]-10) # Cuidar da casa pode ser relaxante
            player["saude"] += 2
        elif escolha == "5":
            horas = 2
            print(f"Jogou aquela pelada/socializou com a galera por {horas} horas.")
            player["respeito"] += 10
            player["saude"] += 5
            player["fadiga"] += 20
        else:
            print("Opção de adulto inválida, camarada.")
            return
 
    elif player["faixa_etaria"] == "4":  # Idoso
        if escolha == "1":
            horas = 1
            print(f"Você fez uns exercícios leves na praça por {horas} hora. Saúde em dia!")
            player["saude"] = min(MAX_SAUDE, player["saude"] + random.randint(5,10))
            player["fadiga"] = max(0, player["fadiga"] - 15)
        elif escolha == "2": # Ir no médico (rotina)
            horas = 2
            print(f"Foi fazer um check-up no médico por {horas} horas.")
            if player["saude"] < 50 and random.randint(1,100) < 40:
                print("O médico descobriu um pequeno problema, mas te passou um tratamento.")
                player["saude"] += 5 # Começou a tratar
            else:
                print("Tudo certo com a saúde, doutor disse pra continuar se cuidando.")
                player["saude"] += 2
            player["fadiga"] += 10
        elif escolha == "3":
            horas = 2
            print(f"Você passou {horas} horas na praça contando suas histórias e jogando dominó.")
            player["respeito"] += 15
            player["fadiga"] = max(0, player["fadiga"] - 5)
            player["inteligencia"] +=1 # Mantém a mente ativa
        elif escolha == "4":
            horas = 3
            print(f"Você cuidou dos netos/do seu jardim por {horas} horas.")
            player["respeito"] += 10
            player["fadiga"] = max(0, player["fadiga"] - 10)
            player["saude"] += 3
        else:
            print("Opção de idoso inválida, meu velho.")
            return
    else:
        print("Faixa etária desconhecida para ações.") # Fallback
        return
 
    if horas > 0:
        avancar_tempo(horas)
    time.sleep(1)
 
 
# --- Loop Principal do Jogo ---
if __name__ == "__main__":
    while True:
        mostrar_status()
        checar_condicoes_perigo() # Verifica se algo ruim aconteceu devido aos status
       
        if not player["prisao"]: # Só tem evento aleatório se não estiver preso
             evento_aleatorio()
             checar_condicoes_perigo() # Eventos podem afetar status
             if player["saude"] <=0: continue # Se morreu no evento, não mostra opções
 
        mostrar_opcoes()
        escolha_jogador = input("\nO que vai ser, chefia? > ")
        executar_acao(escolha_jogador)
 
        # Limpeza final de status antes do próximo loop
        player["fome"] = min(MAX_FOME, max(0, player["fome"]))
        player["saude"] = min(MAX_SAUDE, max(0, player["saude"]))
        player["fadiga"] = min(MAX_FADIGA, max(0, player["fadiga"]))
        player["respeito"] = max(MIN_RESPEITO_GAME_OVER -1 , player["respeito"]) # Para não dar game over antes da checagem
 
        print("\n-----------------------------------------------------\n")
        time.sleep(0.5) # Pequena pausa para ler  
