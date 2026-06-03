"""
ZULU Core — orchestrates all modules
"""

import re
from zulu.voice import speak, listen
from zulu.chat import ask_llm
from zulu.news import get_news
from zulu.computer import open_app, search_web


WAKE_WORD = "zulu"

COMMANDS = {
    "news": ["news", "current events", "what's happening", "headlines", "world"],
    "open": ["open", "launch", "start"],
    "search": ["search", "look up", "google", "find"],
    "exit": ["exit", "quit", "goodbye", "shut down", "bye"],
}


class ZuluCore:
    def __init__(self):
        self.active = False

    def greet(self):
        speak("ZULU online. How can I assist you?")

    def run(self):
        print("\nListening for wake word: 'ZULU'")
        print("Type your command or speak (voice requires microphone).\n")
        while True:
            try:
                user_input = self._get_input()
                if not user_input:
                    continue
                self._handle(user_input.lower().strip())
            except KeyboardInterrupt:
                speak("Shutting down. Goodbye.")
                break

    def _get_input(self):
        """Try voice input; fall back to text."""
        try:
            text = listen()
            if text:
                print(f"You (voice): {text}")
                return text
        except Exception:
            pass
        return input("You: ")

    def _handle(self, text: str):
        # Strip wake word if present
        if text.startswith(WAKE_WORD):
            text = text[len(WAKE_WORD):].strip()

        if not text:
            speak("Yes? How can I help?")
            return

        intent = self._detect_intent(text)

        if intent == "exit":
            speak("Shutting down. Goodbye.")
            raise KeyboardInterrupt

        elif intent == "news":
            articles = get_news()
            if articles:
                summary = "Here are the top headlines: " + ". ".join(articles[:5])
                speak(summary)
                print("\n--- Top Headlines ---")
                for i, a in enumerate(articles[:10], 1):
                    print(f"{i}. {a}")
            else:
                speak("I couldn't fetch the news right now.")

        elif intent == "open":
            app = self._extract_target(text, ["open", "launch", "start"])
            if app:
                speak(f"Opening {app}.")
                open_app(app)
            else:
                speak("What would you like me to open?")

        elif intent == "search":
            query = self._extract_target(text, ["search", "look up", "google", "find"])
            if query:
                speak(f"Searching for {query}.")
                search_web(query)
            else:
                speak("What should I search for?")

        else:
            # General conversation via LLM
            response = ask_llm(text)
            speak(response)
            print(f"ZULU: {response}")

    def _detect_intent(self, text: str) -> str:
        for intent, keywords in COMMANDS.items():
            if any(kw in text for kw in keywords):
                return intent
        return "chat"

    def _extract_target(self, text: str, verbs: list) -> str:
        for verb in verbs:
            if verb in text:
                return text.split(verb, 1)[-1].strip()
        return text.strip()
