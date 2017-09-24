import customNLTKDefn as custLib
import nltk
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree

'''
from tkinter.filedialog import askopenfilename

#Read the PDF File
pdfFile = askopenfilename(filetypes=[("PDF Files","*.pdf")])
'''
pdfFile = "docsProvided/ordjud.pdf"
# First Step: Convert PDF to TEXT for further processing
raw_text = custLib.convert_pdf_to_txt(pdfFile)
'''
## Extra Step : Save the text in a .txt file for future processing
fp = open(pdfFile+".txt","w")
fp.write(raw_text)
fp.close()

'''
# Preprocess the Text extracted: Word processing, Tokenizing(Sentence & Word)
text_preprocessed = custLib.preProcess(raw_text) #Regular Expression
words = custLib.iePreprocess(text_preprocessed) #Information Extraction
#print(words)

#Get court Name
court_name = custLib.extractCourtName(words)
#print("\nCOURT:\nCourt Name:  "+court_name)

#Get parties involved
parties, pt, rt = custLib.extractParties(words)
#print("\nPARTIES:\nPetitioner:  "+parties[0]+"\tPetitioner Type:  "+pt)
#print("\nRespondent:  "+parties[1]+"\tRespondent Tye:  "+rt)

#Get Counsel groups for both Petitioner and Respondent
pc = custLib.extractPetitionerCounselGroup(words)
#print("\nCOUNSEL GROUP:\nforApplicant:\n")
#for counsel in pc:
#    print(counsel)
#print("\nforRespondent:\n")
rc = custLib.extractRespondentCounselGroup(words)
#for counsel in rc:
#    print(counsel)

#Get Coram group
judge,judgeType,day,dayType,date,month,year = custLib.extractCoramGroup(words)
#print(dayType)

# Extract Judgement Details
judgementType,citeTitle,citation,actId,actTitle,sectionId,sectionTitle = custLib.extractJudgementSection(words)
#print(sectionTitle)

#Generate XML File
xmlCase = etree.Element('Case')
xmlDoc = etree.ElementTree(xmlCase)

#Insert Court Details
xmlCourt = etree.SubElement(xmlCase, 'Court')
xmlCourtName = etree.SubElement(xmlCourt, 'CourtName')
xmlCourtName.text = court_name

#Insert Parties group
xmlPartiesGroup = etree.SubElement(xmlCase, 'PartiesGroup')
xmlParties = etree.SubElement(xmlPartiesGroup, 'Parties')
xmlPetitionerGroup = etree.SubElement(xmlParties, 'PetitionerGroup')
xmlPetitioner = etree.SubElement(xmlPetitionerGroup, 'Petitioner', Type=pt)
xmlPetitioner.text = parties[0]

xmlRespondentGroup = etree.SubElement(xmlParties, 'RespondentGroup')
xmlRespondent = etree.SubElement(xmlRespondentGroup, 'Respondent', Type=rt)
xmlPetitioner.text = parties[1]

#Insert Counsel group
xmlCounselGroup = etree.SubElement(xmlCase, 'CounselGroup')
xmlforPetitioner = etree.SubElement(xmlCounselGroup, 'forPetitioner')
for counsel in pc:
    xmlCounselName = etree.SubElement(xmlforPetitioner, 'CounselName')
    xmlCounselName.text = counsel

xmlforRespondent = etree.SubElement(xmlCounselGroup, 'forRespondent')
for counsel in rc:
    xmlCounselName = etree.SubElement(xmlforPetitioner, 'CounselName')
    xmlCounselName.text = counsel

#Insert Coram group
xmlCoramGroup = etree.SubElement(xmlCase, 'CoramGroup')
xmlJudge = etree.SubElement(xmlCoramGroup, 'Judge', Position = judgeType[0])
xmlJudge.text = judge[0]

#Insert Date:
for i,d in enumerate(day):
    xmlDate = etree.SubElement(xmlCase, 'Date', Month = month[i], Date = date[i], Year = year[i], Type = dayType[i])
    xmlDate.text = day[i]

tree = etree.ElementTree(xmlCase)
tree.write('ordjud.xml', pretty_print=True, xml_declaration=True,   encoding="utf-8")
