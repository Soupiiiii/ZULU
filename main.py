"""
ZULU - AI Assistant
Inspired by J.A.R.V.I.S from Iron Man
"""

import os
import sys
import threading
from zulu.core import ZuluCore


def main():
    print("=" * 50)
    print("  Z U L U  -  AI Assistant")
    print("  'At your service.'")
    print("=" * 50)

    zulu = ZuluCore()
    zulu.greet()
    zulu.run()


if __name__ == "__main__":
    main()
