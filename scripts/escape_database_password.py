#!/usr/bin/env python3

import sys
import urllib.parse

if len(sys.argv) < 2:
    print(f"Usage ./{sys.argv[0]} <password>")
    print(' Example: python escape_database_password.py "bla?something!cool" ')
    sys.exit()

password_escaped = urllib.parse.quote_plus(sys.argv[1])
print(password_escaped)
