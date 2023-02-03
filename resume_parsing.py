#!/usr/bin/env python
# coding: utf-8

# In[2]:


import spacy
import pdfminer
import re
import os
import pandas as pd


# In[3]:


import pdff2txt


# In[4]:


# converting pdf to txt, 
def convert_pdf(f):
  output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
  output_filepath = os.path.join("output/txt/", output_filename)
  pdff2txt.main(args=[f, "--outfile", output_filepath])
  print(output_filepath + " saved successfully!!!")
  return open(output_filepath).read()


# In[5]:


# load the language model
nlp = spacy.load("en_core_web_sm")


# In[6]:


result_dict = {"name": [], "phone": [], "email":[], "skills": []}
names = []
phones = []
emails = []
skills = []


# In[7]:


#
def parse_content(text):
  skillset = re.compile("python|java|sql|hadoop|tableu")
  phone_num = re.compile(
    "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
  )
  doc = nlp(text)
  name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0]
  print(name)
  email = [word for word in doc if word.like_email == True][0]
  print(email)
  phone = str(re.findall(phone_num, text.lower()))
  skills_list = re.findall(skillset, text.lower())
  unique_skills_list = str(set(skills_list))
  names.append(name)
  emails.append(email)
  phones.append(phone)
  skills.append(unique_skills_list)
  print("Extraction completed succesfully!!!")


# In[17]:


for file in os.listdir("resumes/"):
  if file.endswith("pdf"):
    txt = convert_pdf(os.path.join("resumes/", file))
    print("\nReading..." + file)
    parse_content(txt)


# In[13]:


result_dict["name"] = names
result_dict["phone"] = phones
result_dict["email"] = emails
result_dict["skills"] = skills


# In[15]:


result_df = pd.DataFrame(result_dict)
result_df


# In[16]:


result_df.to_csv("output/csv/parsed_resumes.csv")

