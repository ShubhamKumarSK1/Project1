import pandas as pd
import math
from fastapi import FastAPI
from pydantic import BaseModel          #required imports                     
app=FastAPI()                           #making an Fast API object

dataframe=pd.read_excel('capbudg.xls')
data=dataframe.to_dict(orient='index')
raw_data=pd.DataFrame(data)             #converting the data in readable form

Initial_investment=raw_data.iloc[[0,2], 1:9]
Cashflow_details=raw_data.iloc[[4,6], 1:6]
Discount_rate=raw_data.iloc[[8,10], 1:9]
Working_capital=raw_data.iloc[[0,2], 10:14]
Growth_rates=raw_data.iloc[0:11, [15,17,18,19]]
Initial_Investment2=raw_data.iloc[0:1 ,22:30]
Salvage_value=raw_data.iloc[0:11 ,31:34]
year=raw_data.iloc[0:11, 20:33]
Operating_Cashflows=raw_data.iloc[0:11, 35:50]
Investment_measures=raw_data.iloc[1:2 ,51:55]
Book_Value=raw_data.iloc[0:11 , 57:61]  #making the proper slots of differet table
table=[Initial_investment,Cashflow_details,Discount_rate,Working_capital,Growth_rates,Initial_Investment2,Salvage_value,Operating_Cashflows,Investment_measures,Book_Value]

list_tab=[]
for i in range(0,len(table)-1):
    list_tab.append(table[i].iloc[0, 0])
list_tab.append(table[9].iloc[4, 0])
dic1={"tables":list_tab}        #making list of names of tables storing it in a dictionary

@app.get("/list_tables")        #
def list_tables():
    return dic1                 #Printing the dictionary

@app.get("/get_table_details")
def get_table_details(table_name):
    list1=[]
    for i in range(0,len(list_tab)):
        if list_tab[i]==table_name:
            print(table[i])
            for j in range(1,len(table[i].columns)): 
                list1.append(table[i].iloc[0,j])
            break    
    dic2={"table_name":table_name,"row_names":list1}
    return dic2             #printing the dictionary having data of table name and the rows

@app.get("/row_sum")
def get_table_details(table_name,row_name):
    sum=0
    for i in range(0,len(list_tab)):
        if list_tab[i]==table_name:
            for j in range(1,len(table[i].columns)): 
                if table[i].iloc[0,j]==row_name:
                    for k in range(1,len(table[i])):
                        if isinstance(table[i].iloc[k,j], (int, float)) and not math.isnan(table[i].iloc[k,j]):
                            sum+=table[i].iloc[k,j]
    dic3={"table_name":table_name,"row_name":row_name,"sum":sum}
    return dic3    #printing the dictionary having data of table name, the row name and sum of its datapoints