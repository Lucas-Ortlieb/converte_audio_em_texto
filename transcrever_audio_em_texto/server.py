# Realize os seguintes comandos via terminal
# pip install flask
# pip install SpeechRecognition

from flask import Flask, request, send_file
import speech_recognition as sr

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Obtendo os dados do formulário
    audio_file = request.files['audio']

    # Salvar o arquivo de áudio no servidor
    audio_path = 'audio.wav'
    audio_file.save(audio_path)

    # Inicializar o reconhecedor de fala
    r = sr.Recognizer()

    # Abrir o arquivo de áudio
    with sr.AudioFile(audio_path) as source:
        # Ler o áudio do arquivo
        audio = r.record(source)

        try:
            # Usar o reconhecedor de fala para transcrever o áudio em texto
            text = r.recognize_google(audio, language="pt-BR")
            print("Texto transcrito:")
            print(text)
        except sr.UnknownValueError:
            return "Não foi possível transcrever o áudio."
        except sr.RequestError as e:
            return f"Erro ao requisitar serviço de reconhecimento de fala: {e}"
            
    # Salvar o texto transcrito em um arquivo .txt
    output_file = "texto_transcrito.txt"
    with open(output_file, "w") as file:
        file.write(text)

    print("Texto transcrito salvo em:", output_file)

    # Enviar o arquivo .txt como resposta para download
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run()



