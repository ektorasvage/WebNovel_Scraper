import sqlite3
import re
import os

# 1. Delete the old database so we start fresh every time
if os.path.exists('webnovel.db'):
    os.remove('webnovel.db')

