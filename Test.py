import customNLTKDefn as custLib
import nltk

# First Step: Convert PDF to TEXT for further processing
pdfFile = "ordjud.pdf"
raw_text = custLib.convert_pdf_to_txt(pdfFile)

## Extra Step : Save the text in a .txt file for future processing
fp = open("ordjud.txt","w")
fp.write(raw_text)
fp.close()


# preprocess the Text extracted
text_preprocessed = custLib.preprocess(raw_text)
words = custLib.ie_preprocess(text_preprocessed)

#parties = extract_parties(text_preprocessed)
#print(parties)
#print(raw_text)
#ac = extractApplicantCounselGroup(text_preprocessed)
#print(s)
rc = custLib.extractRespondentCounselGroup(words)
print(rc[0])
#getCounselDetailPara(text_preprocessed)
