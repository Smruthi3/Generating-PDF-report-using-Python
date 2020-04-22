# Generating-PDF-report-using-Python

# Required Package:

FPDF

Install FPDF package, by type following command in terminal:

pip install fpdf

-------------------------------------------------------------------------------------------------------------------------------------

# Input Requirements

Two folders named static_images and Saved_Analysis_files should be created and it contains the following information:

static_images : contains header,footer and logo (User can place their specific format of header footer and logo here)
Saved_Analysis_files - Contains anlaysis results in the form images,text files ( User can place their respective analysis results here)

Note: The name of the Saved_Analysis_files folder can be changed (user choice) 


# Output 

pdf_generation() function takes two arguments and generate pdf report:- 

1. Location of the analysis charts,text files ( here it is "Saved_Analysis_files")
2. Analysis varibales 
   * It is a dataframe containing the analysis variable name and variable type, refer Analysis_Vars.csv in Inputfile folder
   * This file is required to identify the variables with different datatypes, which is used to pick corresponding analysis images/text      files from the Saved_Analysis_files
   
# Usage
import pandas as pd

analysis_vars = pd.read_csv("~/Analysis_Vars.csv")

pdf_generation("~/Saved_Analysis_files/",analysis_vars)

The above function return the pdf report and the report gets saved in Saved_Analysis_files folder

For easy access the final pdf file is saved in Output folder
