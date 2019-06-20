# Generating-PDF-report-using-Python

Install FPDF package using following commond:

pip install fpdf

Two folders are created:

One for static images - header,footer and logo
Second for Saving Analysis files - images,text files 


pdf_generation() function takes two arguments and generate pdf report:- 

1. Location of the analysis charts,text files
2. Analysis varibales [ It is a dataframe containing the analysis variable name and variable type, refer Inputfile -> Analysis_Vars ]


The final output file is saved in Output folder
