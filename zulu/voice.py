"""
ZULU Voice — speech recognition and text-to-speech
"""

import pyttsx3
import speech_recognition as sr

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 175)   # speaking speed
        _engine.setProperty("volume", 1.0)
        # Try to set a more robotic/professional voice
        voices = _engine.getProperty("voices")
        for v in voices:
            if "male" in v.name.lower() or "daniel" in v.name.lower():
                _engine.setProperty("voice", v.id)
                break
    return _engine


def speak(text: str):
    """Convert text to speech."""
    print(f"ZULU: {text}")
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS error: {e}]")


def listen(timeout: int = 5, phrase_limit: int = 10) -> str:
    """Listen from microphone and return transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[Speech recognition error: {e}]")
            return ""
