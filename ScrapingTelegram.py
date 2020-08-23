from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

# área de conexão com o API do Telegram
api_id = input('Entre com o API_id: ')
api_hash = input('Entre com o API_hash: ')
phone = input('Entre com o telefone no formato +551191234567: ')
client = TelegramClient(phone, api_id, api_hash)

# checagem de segurança - onde será dado entrada do código enviado por mensagem para o seu Telegram
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Entre com o código enviado para você: '))

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))

chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue
# apresenta a lista de grupos que o numero de celular possui no Telegram
print('Escolha um dos grupos listados abaixo')
i = 0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i += 1
# aqui você entra com o numero correspondente ao grupo escolhido para executar o Screpe
g_index = input("Entre com o numero correspondente ao grupo: ")
target_group = groups[int(g_index)]

# cria uma lista com o dos participantes do grupo selecionado
print('Buscando membros deste Grupo {}'.format(target_group.title))
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
client.get_participants()
# neste ponto inicia a criação e gravação dos registros em arquivo com nome do grupo e extenção .CSV
print('Salvando no arquivo -> {}.csv ...'.format(target_group.title))
csv_file = '{}.csv'.format(target_group.title)
with open(csv_file, "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
# neste ponto inicia a passagem por todos os registros da lista (all_participants) para o arquivo .CSV

    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
# neste ponto faz a concatenação de nome e sobrenome
        name = (first_name + ' ' + last_name).strip()

# neste ponto fas a gravação do registro em uma linha conforme lista de rótulos abaixo
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

# adicionado a função para fechar conecção com o telefone via API
client.disconnect()
print('Serviço terminado.... :)')