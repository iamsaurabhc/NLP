import customNLTKDefn as custLib
import nltk

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
'''
#Get court Name
court_name = custLib.extractCourtName(words)
print("\nCOURT:\nCourt Name:  "+court_name)

#Get parties involved
parties, pt, rt = custLib.extractParties(words)
print("\nPARTIES:\nPetitioner:  "+parties[0]+"\tPetitioner Type:  "+pt)
print("\nRespondent:  "+parties[1]+"\tRespondent Tye:  "+rt)

#Get Counsel groups for both Applicant and Respondent
ac = custLib.extractApplicantCounselGroup(words)
print("\nCOUNSEL GROUP:\nforApplicant:\n")
for counsel in ac:
    print(counsel)
print("\nforRespondent:\n")
rc = custLib.extractRespondentCounselGroup(words)
for counsel in rc:
    print(counsel)
'''
#Get Coram group
judge,judgeType,day,date,month,year = custLib.extractCoramGroup(words)
print("\nJudge: "+judge[0])
