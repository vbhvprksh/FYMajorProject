#Imports
from django.shortcuts import redirect
from itsdangerous import json
from app import app
from flask import request, render_template,redirect
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
from flask_mail import Mail,Message
from random import *
from flask import session
import sqlite3









# Main function
if __name__ == '__main__':
    app.run(debug=True)
