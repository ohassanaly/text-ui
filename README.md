## EMR-UI

This project aims at providing a User Interface for several Eletronic Medical Records used at ICHC FMUSP

Most of the project is based on [Streamlit](https://docs.streamlit.io/)<br>
Fuzzy search is based on [Fuzzysearch](https://pypi.org/project/fuzzysearch/)<br>
ICHC built-in modules rely on the registro package developped by the ICHC team (see below for details)

It includes :

### Custom Search

1 upload a CSV with a rghc column (patient_id), a data column (record_date) and a full_text column<br>
text must be lowercased and accents removed

2 perform a similarity search based on fuzzy matching (using Levhenstein distance)

3 visualize results either at cohort level or focusing on one single rghc ;
tools like highlighting matches and downlaod full text are available

Nota : during the dev stage, data used was the concatenation of the different fields of haematology consultations scrapped from Tasy EHR (cf registro.tasy pkg), however, custom search was built to adapt to any EHR

### ICHC built-in modules

1 Tasy search
    Based on an extract from registro.tasy, performs json visualisation and fuzzy search

2 HCMed lab exams
    Extract and visualize exam lab results ; based on registro.exames

___________

Later improvements include :<br>

- Implementing other similarity search methods <br>
- Automatic highlighting of entities such as dates <br>
- Manage boolean operators search <br>

___________
The Tazi Page needs a data/tasy_records.json file to run
The project (for the exams page needs the registro package ; it was installed using registro-2.3.0.tar.gz file)
___________


For questions about the different registro packages, contact ICHC Team : registrotmo.ichc@hc.fm.usp.br (Rafael Oliveira, Joaquim Gasparini, Gustavo Acarvalho)
