import os
import logging
import boto3
from botocore.exceptions import ClientError
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO
import requests
import os
import s3FileManager as s3fm 
import util


bucket_name = "cmtx-bot-storage"
region = "us-east-1"
load_dotenv()
# TODO: Add logging
# TODO: Add error handling
# TODO: Fix to return a client

util = util       

s3_manager = s3fm.S3FileManager(aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
                                aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
                                region_name=region,
                                bucket_name=bucket_name)


def get_public_url(file_name,text='Open Pdf'):
    url = s3_manager.get_public_url(file_name)
    link_text = text
    link_html = f'<a href="{url}" target="_blank">{link_text}</a>'
    return link_html

def get_s3_client():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
    )
    return s3_client


def get_s3(): 
    s3 = boto3.resource('s3', aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                         aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])   
    return s3 

def save_file(fl): 
    try:
        file_name = fl.name 
        s3 = get_s3() 
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=fl,
                                             ContentType='application/pdf')
                    
    except ClientError as e:
        print(e)


def get_files():
    # Create an S3 client
    s3 = get_s3_client()
    

    # Specify the bucket name
    bucket_name = 'cmtx-bot-storage'

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    return response


def load_pdf_from_s3(file_name):
    s3 = get_s3()
    obj = s3.Object(bucket_name, file_name)
    response = obj.get()
    pdf_data = response['Body'].read()
    
    pdf_reader = PdfReader(BytesIO(pdf_data))
    return pdf_reader

    
