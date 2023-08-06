import pandas as pd
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype
import re
from dateutil.parser import parse
import numpy as np

class Preprocess(object):
    def __init__ (self):
        pass
#''?',np.na,pd.NA, naa,nan,-
#'1' - 1
#'2' - 
#'?'
#'3'
#int - 50 , str = 40
#most frequent values -- least frequent values -- Need to think about it
#Overall Dataset overview
#5-point Summary
#null values in categoric variables make it treated as float()
    def preprocess(self, df,columns = None ,regex = '[^\w\s\.]'):
        final_columns=None
        if columns is None:
            final_columns = df.columns.values
        else:
            final_columns = columns
        for column in final_columns:
            #First change the type to a int or float
            #try:
            self.change_type(df,columns = [column])
            #except:
                #print('Problem with ',column)
                #continue
                #value = str(rows[column])
                #x = re.search(regex,value)
                #if not x is None:
                    #rows[column] = np.nan
            #If the column is of string type.
            if is_object_dtype(df[column]):
                for ini in (df[column].index):
                    value = df.loc[ini,column]
                    if pd.isna(value) or len(value)>3:
                        continue
                    x = re.search(regex,value)
                    if not x is None:
                        df.loc[ini,column] = np.nan
                try:
                    df[column] = pd.to_numeric(df[column])
                except:
                    continue
    
    def find_max_type(self,df ,column):
        number_int = 0
        number_float = 0
        number_string = 0
        num_datetime=0
        for entry in df[column]:
            try:
                isinstance(int(entry),int)
                number_int+=1
            except :
                try:
                    isinstance(float(entry),float)
                    number_float+=1
                except :
                    try:
                        parse(str(entry))
                        num_datetime+=1
                    except :
                        number_string+=1


        return {'int':number_int,'float':number_float,'str':number_string,'datetime':num_datetime}
    
    def change_type(self,df,columns=None):
        if columns is None:
            final_columns = df.columns.values
        else:
            final_columns = columns
        for column in final_columns:
            
            if is_numeric_dtype(df[column]) or is_datetime64_any_dtype(df[column]):
                continue
                
            dic = self.find_max_type(df,column)
            maxi = max(dic,key=dic.get)
            #going by the majority is not always a great decision
            #prefer strings more than ints
            #replace maxi by something else
            #get max and second max -- most of the times - better to leave as string - if only 10% string I convert to numeric
            #what will you do for datetime - same concept - if 10% string convert to datetime - otherwise keep as string
            
            #Finding the second maximum
            second_maxi = 0
            index = None
            for key in dic:
                if key==maxi:
                    continue
                if dic[key]>=second_maxi:
                    index =  key
                    second_maxi = dic[key]


            if float(second_maxi)/df.shape[0]<=0.2:
                if maxi == 'int' or maxi== 'float':
                    df[column] = pd.to_numeric(df[column],errors='coerce')
                    print(column,' converted from str to ',maxi)
                elif maxi == 'datetime':
                    df[column]=pd.to_datetime(df[column],errors = 'coerce')
                    print(column,' converted from str to datetime')
    
    
    def get_col_type(self,df,column):
        """Returns the type of column - numeric or categoric.
        
        Identifies the column in the dataframe as either a
        numeric or categoric or datetime variable. Treats
        column having integer values but less than <10>
        distinct values as categoric.
        
        Args:
            column: a str refering to the column whose type
                is to be identified.
        Returns:
            A string 'numeric' or 'categoric'
        """
        
        try:
            if is_numeric_dtype(df[column]) and df[column].nunique()>=10:
                return 'numeric'
            elif is_numeric_dtype(df[column]) and df[column].nunique()<=10:
                return 'categoric'
            elif is_datetime64_any_dtype(df[column]):
                return 'datetime'
            elif is_object_dtype(df[column]):
                return 'categoric'
            else:
                return 'problem_in_detecting_dtype'
                
        except KeyError:
            print('Error in column name')
            return
        
    def num_col_types(self,df):
        dtype_dict = {}
        dtype_dict['numeric']=[]
        dtype_dict['categoric']=[]
        dtype_dict['datetime'] = []
        dtype_dict['problem_in_detecting_dtype']=[]
        for column in df.columns.values:
            dtype_dict[self.get_col_type(df,column)].append(column)

        return dtype_dict