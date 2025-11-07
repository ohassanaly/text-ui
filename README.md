## EMR-UI

This project aims at providing a User Interface for several Eletronic Medical Records used at ICHC FMUSP

Most of the project is based on [Streamlit](https://docs.streamlit.io/)

It includes :

### Custom Search

1 upload a CSV with a rghc column (patient_id) and a full_text column
text must be lowercased and accents removed

2 perform a search based on regex

3 visualize results either at cohort level or focusing on one single rghc ;
tools like highlighting matches and downlaod full text are available

Nota : during the dev stage, data used was the concatenation of the different fields of haematology consultations scrapped from Tasy EHR (cf registro.tasy pkg), however, custom search was built to adapt to any EHR

### ICHC built-in modules

1 Tasy search
    Based on an extract from registro.tasy, performs json visualisation

2 HCMed lab exams
    Extract and visualize exam lab results ; based on registro.exames

___________

Later improvements include adding a similarity / fuzzy text search instead of the regex based current one
Automatic highlighting of entities such as dates

___________
The Tazi Page needs a data/tasy_records.json file to run
The project (for the exams page needs the registro package ; it was installed using registro-2.3.0.tar.gz file)
___________


For questions about the different registro packages, contact ICHC Team : registrotmo.ichc@hc.fm.usp.br (Rafael Oliveira, Joaquim Gasparini, Gustavo Acarvalho)
