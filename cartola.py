import requests,datetime,os, sys, json

strURL = 'https://api.cartolafc.globo.com/atletas/mercado'
strDiretorio = os.path.abspath(__file__)
strDiretorio = os.path.dirname(strDiretorio)
Ano_atual = datetime.datetime.now().year

while True:
  try:
    ano = int(input("Escolha um ano ou digite 0 para sair:"))

    if ano == 0:
        print("Você está saindo do programa")
        sys.exit()

    if ano > Ano_atual:
        break
    elif ano == Ano_atual:
        dic_cartola = requests.get(strURL, verify=True).json()
        break
    else:
        strNomeArq = f"{strDiretorio}/cartola_fc_{ano}.json"
        with open(strNomeArq, "r", encoding='UTF-8') as dictOpen:
            dic_cartola = json.load(dictOpen)
            dictOpen.close()
            break
        
  except ValueError:
   print("\nERROR: O valor informado precisa ser inteiro de base10!")
   continue
  except FileNotFoundError:
   print("\nERROR: O ano desejado não possui arquivo!")
  except:
    print(f"\nERROR: {sys.exc_info()[0]}")

clubes = dic_cartola.get('clubes')
clubes_dic = {}
for id_clube, info_clube in clubes.items():
    nome_clube = info_clube['nome']
    clubes_dic[id_clube] = nome_clube

atletas = dic_cartola.get('atletas')
maiores_pontuacoes = {}
posicoes = {1: 'goleiro', 2: 'lateral', 3: 'zagueiro', 4: 'meia', 5: 'atacante', 6: 'tecnico'}

for atleta in atletas:
    nome = atleta['nome']
    apelido = atleta['apelido']
    clube_id = atleta['clube_id']
    clube = clubes_dic[str(clube_id)]
    posicao_id = atleta['posicao_id']
    jogos_num = atleta['jogos_num']
    media_num = atleta['media_num']
    maior_pontuacao = round(jogos_num * media_num, 2)
    maiores_pontuacoes[nome] = {'pontuacao': maior_pontuacao, 'posicao': posicoes[posicao_id], 'apelido': apelido,
                                'clube': clube}

escalações = ["343", "352", "433", "442", "451", "532", "541"]


escala_usuario = str(input("Escolha uma escalação ou digite 0 para sair: ").replace(".", "").replace(",", "").replace("", "").replace("-", ""))

if escala_usuario == "0":
    print("O programa foi finalizado.")
    sys.exit()

elif escala_usuario not in escalações:
    print("Escalação inválida. Escolha uma das opções válidas.")
    sys.exit()
else:
    dic_Atletas = {atleta: dic_cartola["atletas"] for atleta in range(len(dic_cartola["atletas"]))}
    maiores_pontuacoes[nome] = {'pontuacao': maior_pontuacao, 'posicao': posicoes[posicao_id], 'apelido': apelido,
                                'clube': clube}

    melhores_atletas = sorted(maiores_pontuacoes.items(), key=lambda x: x[1]['pontuacao'], reverse=True)


melhores_goleiros = {}
melhores_zagueiros = {}
melhores_laterais = {}
melhores_meias = {}
melhores_atacantes = {}
melhores_tecnicos = {}

for jogador, info in melhores_atletas:
    posicao = info["posicao"]
    if posicao == 'goleiro':
        melhores_goleiros[jogador] = info
    elif posicao == 'lateral':
        melhores_laterais[jogador] = info
    elif posicao == 'zagueiro':
        melhores_zagueiros[jogador] = info
    elif posicao == 'meia':
        melhores_meias[jogador] = info
    elif posicao == 'atacante':
        melhores_atacantes[jogador] = info
    elif posicao == 'tecnico':
        melhores_tecnicos[jogador] = info

melhores_goleiros = sorted(melhores_goleiros.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
melhores_zagueiros = sorted(melhores_zagueiros.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
melhores_laterais = sorted(melhores_laterais.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
melhores_meias = sorted(melhores_meias.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
melhores_atacantes = sorted(melhores_atacantes.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
melhores_tecnicos = sorted(melhores_tecnicos.items(), key=lambda x: x[1]['pontuacao'], reverse=True)

print("Time Ideal:")
for i in range(11):
    if i < 3:
        print(f"Zagueiro: {melhores_zagueiros[i][0]}")
    elif i < 7:
        print(f"Meia: {melhores_meias[i-3][0]}")
    elif i < 10:
        print(f"Atacante: {melhores_atacantes[i-7][0]}")
    else:
        print(f"Goleiro: {melhores_goleiros[0][0]}")
        

print("\nTécnico Destaque:")
print(f"Técnico: {melhores_tecnicos[0][0]}")