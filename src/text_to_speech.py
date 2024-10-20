from concurrent.futures import ThreadPoolExecutor
import logging
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Azure Speech service
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name = 'en-US-AndrewMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Create a ThreadPoolExecutor for running the talk function in a separate thread
executor = ThreadPoolExecutor(max_workers=1)

def talk(text: str):
    """Convert text to speech using Azure Cognitive Services."""
    def synthesize():
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info(f"Speech synthesized for text: {text}")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            logging.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    logging.error(f"Error details: {cancellation_details.error_details}")

    # Use ThreadPoolExecutor to run the synthesis in a non-blocking manner
    executor.submit(synthesize)
