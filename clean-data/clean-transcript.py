
import json
import re

input_path = 'Videos_202508261525.json'
output_path = 'Videos_202508261525_clean.json'

# Função para remover campos de timestamp
def remove_timestamps(obj):
	if isinstance(obj, dict):
		return {k: remove_timestamps(v) for k, v in obj.items() if not re.search(r'timestamp|created_at|updated_at', k, re.IGNORECASE)}
	elif isinstance(obj, list):
		return [remove_timestamps(item) for item in obj]
	else:
		return obj

# Função para limpar o campo videoTranscript
def clean_transcript(text):
	# Remove timestamps do tipo [00:01], [01:23], etc.
	text = re.sub(r'\[\d{2}:\d{2}\]', '', text)
	# Remove quebras de linha
	text = text.replace('\n', ' ')
	# Remove espaços duplicados
	text = re.sub(r'\s+', ' ', text)
	return text.strip()

# Ler o arquivo JSON, removendo quebras de linha
with open(input_path, 'r', encoding='utf-8') as f:
	content = f.read().replace('\n', '')
	data = json.loads(content)

# Remover campos de timestamp
cleaned_data = remove_timestamps(data)

# Limpar o campo videoTranscript em cada vídeo
if 'Videos' in cleaned_data:
	for video in cleaned_data['Videos']:
		if 'videoTranscript' in video and isinstance(video['videoTranscript'], str):
			video['videoTranscript'] = clean_transcript(video['videoTranscript'])

# Salvar o JSON limpo
with open(output_path, 'w', encoding='utf-8') as f:
	json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
