import io
import pyaudio
import os
import google.cloud.texttospeech as tts

def text_to_speech(text: str):
    voice_name = "en-US-Standard-I"
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    return response

def text_to_audio(text: str):
    response = text_to_speech(text)

    audio_stream = io.BytesIO(response.audio_content)
    
    p = pyaudio.PyAudio()
    data = audio_stream.read(1024)
    
    stream = p.open(format = p.get_format_from_width(2),
                    channels = 1,
                    rate = 24000,
                    output = True)
    while data:
        stream.write(data)
        data = audio_stream.read(1024)

    stream.stop_stream()
    stream.close()

    p.terminate()
    

# New function to read text from a file
def read_text_from_file(file_path: str):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-cloud-api-key.json'

    text_to_audio("Hello. This is Chef Companion. I am your assistant.")