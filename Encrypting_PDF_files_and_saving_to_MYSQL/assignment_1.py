# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:22:53 2022

@author: shiva
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy
import os
import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter import Tk, filedialog
root =Tk()
root.withdraw()
root.attributes('-topmost',True)
open_file = filedialog.askdirectory()
files = os.listdir(open_file)

t = 'rec'

engine = create_engine(f"mysql+pymysql://root:shivam@localhost/new_ff11")
meta = MetaData()

if sqlalchemy.inspect(engine).has_table(t):
    pass
else:
    tb = Table(t, meta,
               Column('id', Integer,primary_key=True, autoincrement=True),
               Column('file_name', String(50), nullable=False),
               Column('file_size', String(50), nullable=False),
               Column('time_of_encryption',  String(50), nullable=False)
               )
    tb.create(engine)


i = 1
for x in files:
    if x.endswith(".pdf"):
        with open(open_file + f"\{x}" , "rb") as in_file:
            
            input_pdf = PdfFileReader(in_file)
            output_pdf = PdfFileWriter()
            output_pdf.appendPagesFromReader(input_pdf)
            output_pdf.encrypt(x[:-4])
            f = datetime.datetime.now().strftime("%y_%m_%d-%H_%M_%S")
            n = datetime.datetime.now().strftime("%H_%M_%S")
            z=x[:-4]+"_"+f+".pdf"
            file_size = str(os.path.getsize(open_file+f"/{x}"))
            engine.execute(f"INSERT INTO {t} VALUES ('{i}', '{z}', '{file_size+' bytes'}', '{n}')")
            with open(open_file+"/"+x[:-4]+"_"+f+".pdf","wb") as out_file:
                output_pdf.write(out_file)
            i = i+1
                

