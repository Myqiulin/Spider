# coding=utf-8

import subprocess

filename = "paixu.png"
subprocess.call(['tesseract','-l','chi_sim',filename,'paixu'])
with open('paixu.txt','r') as f:
    print f.read()