# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:00:34 2025

@author: Franco
"""

import sqlite3
conn = sqlite3.connect("condominio.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(avaliacoes);")
print(cursor.fetchall())
conn.close()