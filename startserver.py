#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 06-Jun-2020
"""

from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
