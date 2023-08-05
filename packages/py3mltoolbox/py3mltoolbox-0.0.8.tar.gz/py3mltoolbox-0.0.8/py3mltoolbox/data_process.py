import os
import sys
import numpy as np
import pandas as pd
import py3toolbox as tb
from sklearn.preprocessing import LabelEncoder


def df_dump(name, df_input, path=None):
  if path is None:
    path = os.getcwd()
  
  dump_file_csv  = os.path.join(path, name + ".csv")
  dump_file_html = os.path.join(path, name + ".html")
  
  tb.write_file(dump_file_html , df_input.to_html(df_input))
  df_input.to_csv(dump_file_csv)




"""
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~  label encoder - same as sklearn
 ~  return numeric number for categorical values
 ~  input: 
 ~  new_val sample : { "col_name" : value }
 ~  
 ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def fillnan (df_input, new_val={} ):
  df_output = df_input.copy
  for c in new_val.keys :
    df_input[c].fillna(new_val[c])
  return df_output

"""
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~  label encoder - same as sklearn
 ~  return numeric number for categorical values
 ~
 ~
 ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def label_encoder (df_input, cols=[]):
  df_output = df_input.copy()
  
  for c in cols :
    c_code = c + "__code"
    c_uniq_values = df[c].dropna().unique()
    label_values =  {v: i for i, v in enumerate(c_uniq_values)}
    df_output[c_code] = df_output[c].map(label_values)
    df_output[c_code] = df_output[c_code].astype('Int64')
  df_output = df_output.drop(columns=cols)
  return df_output

"""
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~  Auto detects if column is categorical or not
 ~  May not be 100% reliable, used for initial check
 ~  
 ~
 ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def auto_detect_cat (v_list):
  #v_list = df_input.values.to_list()
 
  cat_flag  = (1.*v_list.nunique()/v_list.count() < 0.05)  and  ( 
               1.*v_list.value_counts(normalize=True).head(20).sum() > 0.8 ) and (
               v_list.dtypes not in ["int64", "float64"]
               )
              
  return cat_flag

"""
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~  Get unique values and its count
 ~  return tuple
 ~  
 ~
 ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""  
def get_uniq_values_counts(v_list, to_html=False):
 result = {}
 html = ""
 v_c_dic = v_list.value_counts(dropna=False).to_dict()
 for k,v in  v_c_dic.items() :
   result.update( {str(k) : str(v) } )
 if to_html  == True:
    for k,v in result.items():
      html += str(k) + ":" + str(v) + "<BR>"
    return html
 else:
  return result
 
def gen_html_report(report_name, df_input):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  html = tb.read_file(os.path.join(os.path.dirname(dir_path) , "templates/report_template.html"))


  html = html.replace("<!--[<<HTML-TITLE-CONTENT>>]-->", report_name + " @" + tb.get_timestamp())

  # -------- HTML-SUMMARY-CONTENT ---------
  report = ""
  report += "<TABLE CLASS=sortable BORDER=1>"
  report += "<TR>" 
  report += "<TH>Item</TH>"
  report += "<TH>Value</TH>"
  report += "</TR>"
  report += "<TR>" 
  report += "<TD>Shape</TD>"
  report += "<TD>" + str(df_input.shape) + "</TD>"
  report += "</TR>"
  report += "<TR>"
  
  report += "</TABLE>" 
  html = html.replace('<!--[<<HTML-SUMMARY-CONTENT>>]-->',report)




  report_columns            = ["Name", "DataType", "Cat", "Missing%", "Unique_Count",  "Samples"]
  df_orig_report            = pd.DataFrame({}, columns = report_columns)
 
  df_orig_report["Name"]            = [c for c in df_input.columns]
  df_orig_report.index              = df_orig_report["Name"] 
  df_orig_report["DataType"]        = [df_input.dtypes[c] for c in df_input.columns]
  df_orig_report["Cat"]             = [True if auto_detect_cat(df_input[c]) == True else "" for c in df_input.columns]
  df_orig_report["Missing%"]        = (df_input.isna().mean() * 100).round(2)
  df_orig_report["Unique_Count"]    = [df_input[c].nunique() for c in df_input.columns]
  df_orig_report["Samples"]         = [df_input[c].dropna().unique()[:10] for c in df_input.columns]


  # -------- HTML-ORIGINAL-CONTENT ---------
  report = ""
  report += "<TABLE CLASS=sortable BORDER=1>"
  report += "<TR><TH>No.#</TH>"
  
  for c in df_orig_report.columns :
    report += "<TH>" + str(c) + "</TH>" 
  report += "</TR>"  
  
  i = 0
  for index, row in df_orig_report.iterrows():
    i+=1
    report += "<TR><TD>" + str(i) + "</TD>"
    for c in df_orig_report.columns:
      report += "<TD><SPAN onclick='click_expand(this);' CLASS=wrap_text>" + str(row[c]) + "</SPAN></TD>" 
    report += "</TR>"
  report += "</TABLE>" 
  html = html.replace('<!--[<<HTML-ORIGINAL-CONTENT>>]-->',report)


  return html
  
  

if __name__ == "__main__" : 
  #df_dump('test', pd.read_csv("R:/kaggle/ieee-fraud-detection/X_train.csv"), path="R:/")
  df = pd.read_csv("R:/train_data.csv")
  df_copy = label_encoder(df, cols=["ProductCD","card4","card6","P_emaildomain","R_emaildomain","M1","M2", "M3","M4","M5","M6","M7","M8","M9",
                                   "id_12","id_15","id_16","id_23","id_27","id_28","id_29","id_30","id_31","id_33","id_34","id_35","id_36","id_37","id_38","DeviceType","DeviceInfo"
                         ])

  tb.write_file("R:/report.html", gen_html_report ('test', df_copy))
