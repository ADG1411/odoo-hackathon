#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Technician table
"""
from backend.models import db, Technician
from app import create_app

app = create_app()
app.app_context().push()
db.create_all()
print('Technician table created successfully')
