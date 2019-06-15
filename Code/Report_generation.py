from fpdf import FPDF
from datetime import datetime
import pandas as pd
from io import StringIO
import os
import sys
import logging

# logging
logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


def exceptionHandler(errorCode, methodName, exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    traceback = str(exc_type) + ", " + fname + ", " + str(exc_tb.tb_lineno)
    failedResponse = {'status': errorCode, 'body': {"methodname": methodName, "exception": str(exception), "traceback":traceback}}
    logger.info(failedResponse)
    return failedResponse

def fun_generate_pdf_report(var_name_list,static_img_loc,location,typ):
    try:
        from fpdf import FPDF
        from datetime import datetime
        import pandas as pd
        class PDF(FPDF):
            def header(self):
                header_loc=static_img_loc+'header.png'
                self.image(header_loc, 0, 0, 300,10)
                self.ln(10)

            # Page footer
            def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-17)
                self.set_font('', 'B', 10)
                self.set_text_color(0,75,126)
                # Page number
                self.cell(0,20,str(self.page_no()), 0, 0, 'R')
                footer_loc=static_img_loc+'footer.PNG'
                self.image(footer_loc, 0,190,282,20.5)

        ## First page template
        final_name='Analysis Report'
        date=datetime.today().strftime('%m-%d-%Y')

        pdf = PDF('L','mm','A4')
        pdf.add_page()
        effective_page_width = pdf.w - 2*pdf.l_margin
        ybefore = pdf.get_y()
        pdf.ln(h = 10)
        logo_loc=static_img_loc+'logo.PNG'
        pdf.image(logo_loc,w=300)
        divider_line_loc=static_img_loc+'divider_line.PNG'
        pdf.image(divider_line_loc,w=300)
        pdf.set_x(effective_page_width/3 + pdf.l_margin)
        pdf.set_text_color(0,75,126)
        pdf.set_font('Arial', 'B', 30)
        pdf.cell(0,30,final_name)
        pdf.ln(h = 20)
        pdf.set_x(effective_page_width/2.3 + pdf.l_margin)
        pdf.set_text_color(192,80,77)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0,30,date)
        error=location+'status_inference.txt'
        present=os.path.isfile(error)
        if(present):
            pdf.add_page()
            pdf.set_text_color(0,75,126)
            pdf.set_font('Arial', 'B', 30)
            pdf.cell(40, 10,"Data Error")
            pdf.ln(12)
            divider_line_loc=static_img_loc+'divider_line.PNG'
            pdf.image(divider_line_loc,w=300)
            txt=location+'status_inference.txt'
            txt_data = pd.read_csv(txt, header=None,sep='\t')
            pdf.ln(h = 10)
            pdf.set_font('Arial', '', 12)
            pdf.set_text_color(0,0,0)
            pdf.cell(0,10,txt_data.loc[0,0],0,0,align='L')
        else:
            for i in range(len(var_name_list)):
                error_var=location+var_name_list[i]+'_Dist.png'
                exists = os.path.isfile(error_var)
                if(exists):
                    metric1='Distribution:'
                    metric2='Statistical Tests:'
                    metric3='Segments with Distinctly Different Outcomes:'
                    metric4='Inference'
                    cell_width=[65,25,25]
                    cell_width1=[15,15,15,15,15,15]
                    pdf.add_page()
                    pdf.set_text_color(0,75,126)
                    pdf.set_font('Arial', 'B', 30)
                    pdf.cell(40, 10,var_name_list[i])
                    pdf.ln(12)
                    divider_line_loc=static_img_loc+'divider_line.PNG'
                    pdf.image(divider_line_loc,w=300)
                    ## image 1
                    effective_page_width = pdf.w - 2*pdf.l_margin
                    ybefore = pdf.get_y()
                    pdf.set_text_color(0,0,0)
                    pdf.set_font('Arial', 'U', 15)
                    pdf.cell(30,5,metric1,align='C')
                    pdf.cell(-90)
                    pdf.ln(h = 5)
                    img1=location+var_name_list[i]+'_Dist.png'
                    pdf.image(img1,w=pdf.w/2.5, h=pdf.h/2.5)
                    pdf.ln(h = 5)

                    ## Table
                    pdf.set_font('Arial', 'U', 15)
                    pdf.cell(40,5,metric2,align='C')
                    pdf.cell(-90)
                    pdf.ln(h = 10)
                    tbl=location+var_name_list[i]+'_stats_tab.csv'
                    values=pd.read_csv(tbl)
                    values=values.fillna('')
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_fill_color(0,75,126)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(cell_width[0],5,'  ',1,0,align='L',fill=True)
                    pdf.cell(cell_width[1],5,values.columns[1],1,0,align='L',fill=True)
                    pdf.cell(cell_width[2],5,values.columns[2],1,0,align='L',fill=True)
                    pdf.ln(h = 5)
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(0,0,0)
                    pdf.cell(cell_width[0],5,values.loc[0,'Name'],1,0,align='L')
                    pdf.cell(cell_width[1],5,str(round(values.loc[0,'Value'],3)) if(values.loc[0,'Value']!='') else values.loc[0,'Value'] ,1,0,align='L')
                    pdf.cell(cell_width[2],5,str(round(values.loc[0,'p Value'],3)) if(values.loc[0,'p Value']!='') else values.loc[0,'p Value'] ,1,0,align='L')

                    pdf.ln(h = 5)
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(0,0,0)
                    pdf.cell(cell_width[0],5,values.loc[1,'Name'],1,0,align='L')
                    pdf.cell(cell_width[1],5,str(round(values.loc[1,'Value'],3)) if(values.loc[1,'Value']!='') else values.loc[1,'Value'],1,0,align='L')
                    pdf.cell(cell_width[2],5,str(round(values.loc[1,'p Value'],3)) if(values.loc[1,'p Value']!='') else values.loc[1,'p Value'],1,0,align='L')

                    if(typ[i]=='Num'):
                        pdf.ln(h = 5)
                        pdf.set_font('Arial', '', 10)
                        pdf.set_text_color(0,0,0)
                        pdf.cell(cell_width[0],5,values.loc[2,'Name'],1,0,align='L')
                        pdf.cell(cell_width[1],5,str(round(values.loc[2,'Value'],3)) if(values.loc[2,'Value']!='') else values.loc[2,'Value'],1,0,align='L')
                        pdf.cell(cell_width[2],5,str(round(values.loc[2,'p Value'],3)) if(values.loc[2,'p Value']!='') else values.loc[2,'p Value'],1,0,align='L')

                    ## image 2
                    pdf.set_xy(effective_page_width/1.5 + pdf.l_margin, ybefore)
                    pdf.set_font('Arial', 'U', 15)
                    pdf.cell(40,6,metric3,align='C')
                    img2=location+var_name_list[i]+"_IV_based_BP.png"
                    pdf.image(img2,x=150,y=50,w=pdf.w/2.5, h=pdf.h/2.5)

                    ## Inference
                    ## image4
                    pdf.ln(h = 98)
                    pdf.set_x(effective_page_width/1.84 + pdf.r_margin)
                    pdf.set_font('Arial', 'U', 15)
                    pdf.set_text_color(0,0,0)
                    pdf.cell(0,0,metric4)
                    txt=location+var_name_list[i]+'_inference.txt'
                    txt_data = pd.read_csv(txt, header=None,sep='\t')
                    if(txt_data.shape[0]==1):
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.set_font('Arial', '', 12)
                        pdf.set_text_color(0,0,0)
                        pdf.cell(0,10,txt_data.loc[0,0],0,0,align='L')
                    elif(txt_data.shape[0]==2):
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.set_font('Arial', '', 12)
                        pdf.set_text_color(0,0,0)
                        pdf.cell(0,10,txt_data.loc[0,0],0,0,align='L')
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,15,txt_data.loc[1,0].split(':')[0]+":",0,0,align='L')
                        pdf.ln(h=5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,15,txt_data.loc[1,0].split(':')[1],0,0,align='L')
                    else:
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.set_font('Arial', '', 12)
                        pdf.set_text_color(0,0,0)
                        pdf.cell(0,10,txt_data.loc[0,0],0,0,align='L')
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,15,txt_data.loc[1,0].split(':')[0]+":",0,0,align='L')
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,15,txt_data.loc[1,0].split(':')[1],0,0,align='L')
                        pdf.ln(h = 8)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,20,txt_data.loc[2,0].split(':')[0]+":",0,0,align='L')
                        pdf.ln(h = 5)
                        pdf.set_x(effective_page_width/1.84 + pdf.l_margin)
                        pdf.cell(0,20,txt_data.loc[2,0].split(':')[1],0,0,align='L')
                else:
                    pdf.add_page()
                    pdf.set_text_color(0,75,126)
                    pdf.set_font('Arial', 'B', 30)
                    pdf.cell(40, 10,var_name_list[i])
                    pdf.ln(12)
                    divider_line_loc=static_img_loc+'divider_line.PNG'
                    pdf.image(divider_line_loc,w=300)
                    txt=location+var_name_list[i]+'_inference.txt'
                    txt_data = pd.read_csv(txt, header=None,sep='\t')
                    pdf.ln(h = 10)
                    pdf.set_font('Arial', '', 12)
                    pdf.set_text_color(0,0,0)
                    pdf.cell(0,10,txt_data.loc[0,0],0,0,align='L')
        report_nm=location+'Analysis_Report'+'.pdf'
        return(pdf.output(name=report_nm, dest='F'))
    except Exception as ex:
        return exceptionHandler('1003', 'Error in fun_generate_pdf_report code', ex)


def pdf_generation(location,analysis_vars):
    try:
        static_img_loc='static_images/'
        var_list=list(analysis_vars.Variable_Name)
        var_typ=list(analysis_vars.Variable_Type)
        report=fun_generate_pdf_report(var_list,static_img_loc,location,var_typ)
        return report
    except Exception as ex:
        return exceptionHandler('1003', 'Error in pdf_generation code', ex)