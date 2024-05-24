from flask import Flask,request,jsonify
from services.QRCodeService import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

qr = QrCodeQenerate() 

@app.get("/generate")
def generateCode():
  qr.addQrCode()
  return {'message' : "saved"}

@app.get("/codes")
def getqrCodes():
  # we will have to get the row of qrCode not the whole list
  return jsonify(qr.getQrCode())

@app.get("/get/<code>")
def readCode(code):
  return qr.readQrCode(code),201