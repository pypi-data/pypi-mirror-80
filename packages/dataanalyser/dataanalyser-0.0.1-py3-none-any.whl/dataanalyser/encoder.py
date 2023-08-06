import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype
from sklearn.preprocessing import OneHotEncoder,LabelEncoder

class Encoder():
    def __init__(self):
        self.thresh = 10
        self.target = None
        self.columns = None
    
    def set_params(self,df,**kwargs):
        """Method to set user-defined parameters."""
        
        if 'thresh' in kwargs:
            self.thresh = kwargs['thresh']
        if 'target' in kwargs:
            self.target = kwargs['target']
        if 'columns' in kwargs:
            self.columns= kwargs['columns']
        else:
            self.columns = df.columns.values
         
    
    def encoder(self,df,**kwargs):
        self.set_params(df,**kwargs)
        
        
        for column in self.columns:
             try:
                #checking whether column is a target that is to be avoided
                if (not self.target is None) and column in self.target:
                    continue
                #only encode categoric variables
                #if less than thresh unique values -- onehot encode
                if is_object_dtype(df[column]) and df[column].nunique()<=self.thresh:                    
                    self.oneHotEncoding(df,column)
                
                #if more than thresh unique values -- label encode
                elif is_object_dtype(df[column]):
                    self.labelEncoding(df,column)
             except:              
                print(column,'not encoded\tNULL VALUES FOUND')
                continue
                
    def oneHotEncoding(self,df,column,enc_one_hot = OneHotEncoder(sparse = False)):
        """Method to perform oneHotEncoding."""
        
        x = df[column].values
        x = x.reshape(-1,1)
        enc_one_hot.fit(x)
        x=enc_one_hot.transform(x)
                    
        df.drop(column,axis=1,inplace=True)
        temp = pd.DataFrame(x,columns=enc_one_hot.get_feature_names(input_features=[column]),index=df.index)
        for col in temp.columns.values:
            df[col]=temp[col]
        print(column,'\tOneHotEncoded to ',end=" ")
        print(enc_one_hot.get_feature_names(input_features=[column]))
    
    def labelEncoding(self,df,column,enc_label = LabelEncoder()):
        """Method to perform LabelEncoding."""
        
        enc_label.fit(df[column].values)
        df[column] = enc_label.transform(df[column].values)
        print(column,'\tLabel Encoded to ',column)
        
#data must be encoded at the end. So if we automate we have to run at end.