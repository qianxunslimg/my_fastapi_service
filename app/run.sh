#!/bin/bash
# aerich init -t db.db.TORTOISE_ORM
# aerich init-db
aerich migrate && aerich upgrade
uvicorn app:app --reload --host 0.0.0.0 --port 8000