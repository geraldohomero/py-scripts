## Cada canal presente no arquivo ytChannels.csv será convertido em um arquivo .md
## O arquivo .md conterá as seguintes informações: name,url,id,numberOfVideos,numberOfSubscribers,dataCollected da seguinte forma:

## ---
## tags:
##   - nova-direita
##   - youtube
##   - canal
## ---
## ### <Nome do canal>
## ### URL do Canal:
## <url do canal>
## ### ID do Canal:
## <id do canal>
## ### Número de Vídeos:
## <número de vídeos>
## ### Número de Inscritos: 
## <número de inscritos>
## ### Data da Coleta:
## <data da coleta>
## YYYY-MM-DD HH:MM:SS

## O arquivo .md será salvo no diretório /channels
## O arquivo .md será nomeado com o nome do canal

import csv
import os

# Criação do diretório /channels
if not os.path.exists('channels'):
    os.makedirs('channels')

# Abertura do arquivo ytChannels.csv
with open('ytChannels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Criação do arquivo .md
        with open('channels/' + row['name'] + '.md', 'w') as file:
            file.write('---\n')
            file.write('tags:\n')
            file.write('  - nova-direita\n')
            file.write('  - youtube\n')
            file.write('  - canal\n')
            file.write('---\n')
            file.write('### URL do Canal:\n')
            file.write(row['url'] + '\n')
            file.write('### ID do Canal:\n')
            file.write(row['id'] + '\n')
            file.write('### Número de Vídeos:\n')
            file.write(row['numberOfVideos'] + '\n')
            file.write('### Número de Inscritos:\n')
            file.write(row['numberOfSubscribers'] + '\n')
            file.write('### Data da Coleta:\n')
            file.write(row['dataCollected'] + '\n') 
            file.write('YYYY-MM-DD HH:MM:SS\n')
print('Arquivos .md criados com sucesso!')
