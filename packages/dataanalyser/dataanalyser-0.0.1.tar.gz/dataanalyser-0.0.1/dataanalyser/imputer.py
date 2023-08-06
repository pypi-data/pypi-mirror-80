import pandas as pd
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype
from sklearn.linear_model import LinearRegression

class Imputer(object):
    def __init__(self,*arg,**kwargs):
        """parameters used by imputing methods."""
        
        self.num_method = 'median'
        self.cat_method = 'mode'
        self.columns = None
        
    def set_params(self,df,**kwargs):
        """updating the paramters."""
        
        if 'num_method' in kwargs:
            self.num_method = kwargs['num_method']
        if 'cat_method' in kwargs:
            self.cat_method = kwargs['cat_method']
        if 'columns' in kwargs:
            self.columns= kwargs['columns']
        else:
            self.columns = df.columns.values
            

            
    def impute(self,df,**kwargs):
        """Calls relevant methods to impute numeric and categoric variables."""
        
        print('All columns having null values will be imputed. To impute specific columns pass columns = [] when calling the method')
        self.set_params(df,**kwargs)
        print('Columns to be imputed')
        print(self.columns)
        print('Method for imputing numeric variables: median,mean,interpolate')
        print('Method for imputing categoric variables: mode,missing(replace nan by "missing")')
        print('Other options: bfill,ffill')
        
        #user input
        opt = input('Impute(y or n c to change method: )')
        if opt=='n':
            return
        if opt == 'c':
            self.num_method = input('Method for imputing numerical values: ')
            self.cat_method = input('Method for imputing categoric values: ')
            
        #imputing
        columns_imputed=[]
        
        for column in self.columns:
            try:
                if is_numeric_dtype(df[column]):
                    self.impute_num(df,column)
                elif is_object_dtype(df[column]):
                    self.impute_cat(df,column)
                columns_imputed.append(column)
            except:
                print('Problem in processing ',column)
                continue
        print('Imputed Columns: ',columns_imputed)
                
    def impute_num(self,df,column):
        """Imputes Numeric Variables."""
        
        if(self.num_method=='mean'):
            df[column]=df[column].fillna(df[column].mean())
        elif(self.num_method=='median'):
            df[column]=df[column].fillna(df[column].median())
        elif self.num_method=='bfill':
            df[column]=df[column].fillna(method='bfill')
        elif self.num_method=='ffill':
            df[column]=df[column].fillna(method='ffill')
        elif self.num_method=='interpolate':
            df[column]=df[column].interpolate()
        #elif self.num_method == 'knn':
        #    from sklearn.impute import KNNImputer
        #    imputer = KNNImputer()
        #    df[column]=df[column] = pd.Series(imputer.fit_transform(df[column].values.reshape(-1,1)).reshape(-1,))
            
        
    def impute_cat(self,df,column):
        """Imputes Categoric Variables."""
        
        if self.cat_method=='mode':
            df[column]=df[column].fillna(df[column].mode()[0])
        elif self.cat_method=='bfill':
            df[column]=df[column].fillna(method='bfill')
        elif self.cat_method=='ffill':
            df[column]=df[column].fillna(method='ffill')
        elif self.cat_method == 'missing':
            df[column] = df[column].fillna('missing')

#If it is time series, bfill and ffill should be suggested
#Warning: before imputing ask the user.
"""        
    def impute_regression(self,df,**kwargs):
        from sklearn.linear_model import LinearRegression
        params = None
        target = None
        if 'params' in kwargs and 'target' in kwargs:
            params = kwargs['params']
            target = kwargs['target']
        #TO DO: Label encode categorical variables here
        try:
            for feature in target:
                model = LinearRegression()
                model.fit(X=df.loc[df[feature].notnull(),params],y=df.loc[df[feature].notnull(),feature])
            
                df.loc[df[feature].isnull(),feature]= model.predict(df[params])[df[feature].isnull()]
                print(feature,' imputed using Linear Regression')
        except:
            print('NULL Values found in Features used for predicting')
            try:
                print(df[params].isna().sum())
            except:
                print('Invalid Columns Present')
"""
#Linear Regression and KNN