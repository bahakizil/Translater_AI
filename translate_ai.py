import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path


def voice_to_voice():

    #ceviri
    transcription_response = audio_transcription(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text

    es_translation, en_translation, ja_translation = text_translation(text)

    es_audio_path = text_to_speech(es_translation)
    en_audio_path = text_to_speech(en_translation)
    ja_audio_path = text_to_speech(ja_translation)
    
    es_path = Path(es_audio_path)
    en_path = Path(en_audio_path)
    ja_path = Path(ja_audio_path)
    return ja_path,en_path,es_path

    





def audio_translation():

    aai.settings.api_key = "d502d55e78d54bff9c03b19031129069"

    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)
    return transcription





def text_translation():

    translator_es(from_lang="tr", to_lang="es")
    es_text = translator_es.translate(text)

    translator_en(from_lang="tr", to_lang="en")
    en_text = translator_en.translate(text)

    translator_ja(from_lang="tr", to_lang="ja")
    ja_text = translator_ja.translate(text)

    return es_text, en_text, ja_text

def text_to_speech(text):

    ELEVENLABS_API_KEY = os.getenv("sk_c65e00fa906e4d07b84d74a83cc2e6661a4a57261ae714ea")
    client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)
    
     # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # baha
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)   


demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs = [gr.Audio(label="Spanish"), gr.Audio(label="Turkish"), gr.Audio(label="Japanese")]
)


if __name__ == "__main__":
    demo.launch(share=True)

