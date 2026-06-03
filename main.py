"""
ZULU - AI Assistant
Inspired by J.A.R.V.I.S from Iron Man
"""

from dotenv import load_dotenv

load_dotenv()

from zulu.gui import ZuluGUI


def main():
    app = ZuluGUI()
    app.run()


if __name__ == "__main__":
    main()
