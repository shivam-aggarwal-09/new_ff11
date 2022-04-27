# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 11:09:17 2022

@author: shiva
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter import Tk, filedialog
import hashlib
import pandas as pd
import datetime
import getpass
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

h = hashlib.blake2b(key=b"pseudorandom key", digest_size = 10)

root =Tk()
root.withdraw()
root.attributes('-topmost',True)
file_loc = filedialog.askopenfilename()
print(file_loc)

df = pd.read_csv(file_loc)

root =Tk()
root.withdraw()
root.attributes('-topmost',True)
open_file = filedialog.askdirectory()
files = os.listdir(open_file)

sender = input("Your Email ID: ")
password = getpass.getpass("Enter Your Password: ")

i = 0
for x in files:
    if x.endswith(".pdf"):
        with open(open_file + f"\{x}" , "rb") as in_file:
            input_pdf = PdfFileReader(in_file)
            output_pdf = PdfFileWriter()
            output_pdf.appendPagesFromReader(input_pdf)
            
            
            h.update(b"{x}")
            pas = h.hexdigest()
            output_pdf.encrypt(pas)
            
            email = df['email'].iloc[i]
            f = datetime.datetime.now().strftime("%y_%m_%d-%H_%M_%S")
            with open(open_file+"/"+x[:-4]+"_"+f+".pdf","wb") as out_file:
                output_pdf.write(out_file)
            
            
            to = df['email'][i]
            i = i+1
            data = MIMEMultipart()
            data['From'] = sender
            data['To'] = to
            data['Subject'] = "Your File"
            body = "Your file is attached below \n Your password is: {}".format(pas)
            data.attach(MIMEText(body, 'plain'))
            filename = x[:-4]+"_"+f+".pdf"
            attachment = open(open_file + f"\{filename}", "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            data.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            
            s.login(sender, password)
            text = data.as_string()
            s.sendmail(sender, to, text)
            s.quit()

            

