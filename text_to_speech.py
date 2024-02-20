import os
import google.cloud.texttospeech as tts

# Set the environment variable for the API key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'arched-pier-411007-1127fcd65f07.json'

def text_to_wav(voice_name: str, text: str):
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

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')

# New function to read text from a file
def read_text_from_file(file_path: str):
    with open(file_path, 'r') as file:
        return file.read()


