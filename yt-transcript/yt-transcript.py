from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id():
    url_or_id = input("Digite a URL do YouTube ou o ID do vídeo: ")
    # Extrair ID se for uma URL completa
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        if "v=" in url_or_id:
            # URL formato youtube.com/watch?v=ID
            video_id = url_or_id.split("v=")[1].split("&")[0]
        else:
            # URL formato youtu.be/ID
            video_id = url_or_id.split("/")[-1].split("?")[0]
    else:
        # Assume que é diretamente o ID
        video_id = url_or_id
    
    return video_id

def main():
    video_id = get_video_id()
    
    try:
        # Listar todas as transcrições disponíveis
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        
        print("\nTranscrições disponíveis:")
        available_languages = []
        
        for i, transcript in enumerate(transcripts):
            lang_code = transcript.language_code
            lang_name = transcript.language
            is_generated = "gerada automaticamente" if transcript.is_generated else "criada manualmente"
            print(f"{i+1}. {lang_name} [{lang_code}] ({is_generated})")
            available_languages.append((lang_code, transcript))
        
        # Obter a escolha do usuário
        choice = int(input("\nEscolha o número da transcrição desejada: ")) - 1
        
        if 0 <= choice < len(available_languages):
            selected_lang, selected_transcript = available_languages[choice]
            transcript_data = selected_transcript.fetch()
            
            # Opção para incluir ou não timestamps
            include_timestamps = input("Incluir timestamps? (s/n): ").lower() == 's'
            
            # Nome do arquivo de saída
            output_file = f"transcript_{video_id}_{selected_lang}.txt"
            
            # Escrever a transcrição no arquivo
            with open(output_file, 'w', encoding='utf-8') as file:
                for entry in transcript_data:
                    if include_timestamps:
                        # Formatar tempo como minutos:segundos
                        start_time = entry.start
                        minutes = int(start_time // 60)
                        seconds = int(start_time % 60)
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        file.write(f"{timestamp} {entry.text}\n")
                    else:
                        file.write(f"{entry.text}\n")
            
            print(f"Transcrição salva em '{output_file}'")
        else:
            print("Escolha inválida!")
    
    except Exception as e:
        print(f"Erro ao obter a transcrição: {str(e)}")

if __name__ == "__main__":
    main()
