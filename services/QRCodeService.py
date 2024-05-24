from model.QRCode import QrCode,session

from sqlalchemy import select

import qrcode
from uuid import uuid4

import cloudinary
from cloudinary import uploader
from io import BytesIO

import os
from dotenv import load_dotenv


class QrCodeQenerate():
  __cloud_name = os.getenv("cloud_name")
  __api_key = os.getenv("api_key")
  __api_secret = os.getenv("api_secret")

  def addQrCode(self):
    unique_uuid =uuid4()
    session.add(
      QrCode(
        Link = self.__saveToCloud(unique_uuid),
        uuid = unique_uuid 
        )
    )
    session.commit()

  def getQrCode(self):
    qrCodes = []
    stmt = select(QrCode.Link,QrCode.ID,QrCode.read,QrCode.uuid)
    for code in session.execute(stmt):
      new = {"id":code.ID,"link":code.Link,"read":code.read,"uuid":code.uuid}
      qrCodes.append(new)
    
    return qrCodes

  def readQrCode(self,uuid):
    qrCode = session.query(QrCode).filter(QrCode.uuid == uuid).first()
    if(qrCode.read):
      return """
        <h1>User has already bean read</h1>
        """
    else:
      qrCode.read=True
      session.commit()
      return "<h1>User is new</h1>"


  def __generateQrCode(self,unique_uuid):
    
    unique_data = f"http://16.170.53.222:8090/get/{unique_uuid}"
    
    # Generate QR code
    qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=4,
      )
    qr.add_data(unique_data)
    qr.make(fit=True)

      # Create an image from the QR code
    return qr.make_image(fill_color="black", back_color="white")


  def __saveToCloud(self,unique_uuid):
    # Convert PilImage to bytes
    image_bytes = BytesIO()
    qr_image = self.__generateQrCode(unique_uuid)
    qr_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)  # Reset the file pointer to the beginning

    # Configure Cloudinary
    cloudinary.config(
        cloud_name=f"{self.__cloud_name}",
        api_key=f"{self.__api_key}",
        api_secret=f"{self.__api_secret}"
    )

    # Upload the image to Cloudinary
    uploaded_image = uploader.upload(image_bytes, folder="qrcodes")
    print(uploaded_image)
    return uploaded_image["url"]
