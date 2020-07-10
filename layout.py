import io
import re
from PIL import Image
import pytesseract
from wand.image import Image as wi
from crop_pdf import making_pdf
import json


def get_page(page_name):
        pdf = wi(filename =page_name, resolution = 500)
        pdfImage = pdf.convert('jpeg')

        imageBlobs=[]


        for img in pdfImage.sequence:
    	       imgPage = wi(image = img)
    	       imageBlobs.append(imgPage.make_blob('jpeg'))

        pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract'

        q = open('Questions.txt','a')
        o = open('Options.txt','a')
        page=[]
        for imgBlob in imageBlobs:
            im = Image.open(io.BytesIO(imgBlob))
            text = pytesseract.image_to_string(im, lang = 'eng')
            page.append(text)
            im.close()

        return page

def questions_extr(text,set,pdf,section):
    q = open('Questions.txt','a')
    o = open('Options.txt','a')
    #Pattern to select answers
    non_waste=re.compile('(?!.*(COMPETITIVE|EXAMS)).*[^%|FOR]$')
    options=re.compile('[a-d][.].*')#Pattern to select options
    lines=text.split('\n')
    length=len(lines)
    i=0
    tmp_dic={}
    tmp_dic["# QUESTION:"]=' '
    tmp_dic['Options']=' '
    while(i<length):
        if "ANSWERS" in lines[i]:
            pdf['SECTION-'+str(set)]=section
            section=[]
            s=json.dumps(pdf)
            set+=1
            with open("josndata.txt",'w') as f:
                f.write(s)
            f.close()
            while(True and i<length):
                if "SECTION-" in lines[i]:
                    break
                i+=1
        if options.match(lines[i]):
            tmp_dic['Options']=tmp_dic['Options']+lines[i]+" "
            #o.write(' '+lines[i]+'\n')
            if 'd.' in lines[i]:
                section.append(tmp_dic)
                tmp_dic={}
                tmp_dic["# QUESTION:"]=''
                tmp_dic['Options']=''
            i+=1
        else:
            if non_waste.match(lines[i]):
                while(True and i<length):
                    if 'a.' in lines[i]:
                        tmp_dic['Options']=tmp_dic['Options']+lines[i]+" "
                        i+=1
                        break
                    if lines[i]!='' or lines[i]!=" ":
                        tmp_dic['# QUESTION:']=tmp_dic['# QUESTION:']+(lines[i]+' ')
                    i+=1
                    #q.write(' '+lines[i]+'\n')
            i+=1
    q.close()
    o.close()
    return section,pdf


def answers_extr(text,set,pdf):
    a = open('Answers.txt','a')
    non_waste=re.compile('(?!.*(COMPETITIVE|EXAMS)).*[^%|FOR]$') #REMOVING TEXTS STARTING FROM WORDS INSIDE THE BRACKETS
    lines=text.split('\n')
    length=len(lines)
    i=0
    tmp_dic={}
    tmp_dic['Answers']=' '
    while(i<length):
        if "ANSWERS" in lines[i]:
            while(True and i<length):
                if "SECTION-" in lines[i]:
                    i+=1
                    break
                else:
                    if non_waste.match(lines[i]):
                        tmp_dic['Answers']=tmp_dic['Answers']+lines[i]
                        #a.write(' '+lines[i]+'\n')
                    i+=1
        else:
            i+=1

    a.close()
    return set

def instance_pdf(pdf_name):
    s_page=1
    e_page=6
    page=[]
    qsn_flag=0
    ans_flag=0
    set=1
    pdf={}
    section=[]
    while(s_page<=e_page):
        making_pdf(s_page)
        page=get_page("New.pdf")
        for text in page:
            if 'ANSWERS' in text or ans_flag==1:
                qsn_flag=0
                ans_flag=1
                set=answers_extr(text,set,pdf)
            if 'SECTION-' in text or qsn_flag==1:#Checking First Occ. questions(questions_start)
                ans_flag=0
                qsn_flag=1
                print(qsn_flag)
                section,pdf=questions_extr(text,set,pdf,section)
            s_page+=1

instance_pdf('Geography.pdf')
