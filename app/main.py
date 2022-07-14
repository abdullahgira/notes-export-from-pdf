import os
from flask import Flask, request, jsonify
from datetime import datetime
from .extractor import extract_notes

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_pdf():
    dt_obj = datetime.utcnow()
    millisec = int(dt_obj.timestamp() * 1000)
    file_name = './uploads/file_' + str(millisec) + '.pdf'

    pdf = request.files['file']
    pdf.save(file_name)
    
    notes = extract_notes(file_name)

    if os.path.exists(file_name):
      os.remove(file_name)

    return jsonify(notes)
