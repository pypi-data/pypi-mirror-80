from .duplicates import Duplicates
from .encoder import Encoder
from .imputer import Imputer
from .nullhandler import HandleNull
from .outlier import OutlierDetector
from .plotter import Plotter
from .preprocess import Preprocess
from .statanalysis import StatAnalysis

import pandas as pd
import time
from functools import wraps
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype

class Explorer(object):
    
    def _print_decorator(function):
        @wraps(function)   
        def wrapper(self,*arg,**kwarg):
            dic = function(self,*arg,**kwarg)
            for key,value in dic.items():
                print(key,':',value)
            self.print_shape()
            print()
            print('******************************')
        return wrapper
    
    def __init__(self,df):
        self.df=df

    @_print_decorator
    def tester(self,a=4,*arg,**kwarg):
        print('Hello World',a)
        return {3:4}
    
    def data(self):
        """Returns the data."""
        return self.df    
    
    def shape(self):
        """Returns the shape of the data."""
        return self.data().shape
    
    def print_shape(self):
        """Prints the shape of the dataframe."""
        print('Number of rows: ',self.num_rows(),'\t','Number of columns: ',self.num_cols())
    
    def num_rows(self):
        """Returns the number of rows in the dataframe."""
        return self.data().shape[0]
    
    def num_cols(self):
        """Returns the number of columns int the dataframe."""
        return self.data().shape[1]
    
    def column_types(self,Pro = Preprocess()):
        """Print the Data types of each column in the dataframe."""
        print('Note: Numeric_variables having less than 10 distinct values are regarded as categoric')
        return Pro.num_col_types(self.data())

    def null_values(self):
        """Returns the count of null values in each column. """
        return (self.data().isna().sum())
    
    def columns(self):
        return self.data().columns.values

    @_print_decorator
    def preprocess(self,Processor = Preprocess(),**kwargs):

        print('\t\t**Preprocessing**\n')    

        Processor.preprocess(self.data(),**kwargs)
        
        return {}
        
    
    @_print_decorator
    def drop_duplicates(self,DuplicateHandler = Duplicates()):
        """Removes duplicate rows and columns
        
        Removes duplicate rows. Duplicate columns with same name are removed.
        
        Args:
        
        DuplicateHandler: optional, a class object that has a drop_duplicates
            method
        
        """
        print('\t\t**Dropping Duplicates**\n')    

        initial_num_rows = self.num_rows()
        initial_num_cols = self.num_cols()
        
        
        #DuplicateHandler can be replaced by any suc
        DuplicateHandler.drop_duplicates(self.data())
        
        
        final_num_rows = self.num_rows()
        final_num_cols = self.num_cols()
        
        return {'Rows removed':initial_num_rows-final_num_rows,'Columns removed':initial_num_cols-final_num_cols}
    
    @_print_decorator
    def drop_rows(self,NullHandler = HandleNull(),**kwargs):
        """Drops rows having drop_percent fraction of null values.
        
        Args:
        
        NullHandler: optional, a class object that has a 'HandleNull' method
        
        **kwargs(optional)
            drop_percent: default 0.3,float,between 0 and 1. Rows having 
                more than drop_percent amount of null values will be
                dropped.
            

        
        """
        print('\t\t**Dropping rows**\n')

        initial_num_rows = self.num_rows()

        NullHandler.drop_rows(self.data(),**kwargs)
        
        final_num_rows = self.num_rows()
        
        return {'Rows removed':initial_num_rows-final_num_rows}
    
    @_print_decorator
    def drop_cols(self,NullHandler = HandleNull(),**kwargs):
        """Drops columns having drop_percent fraction of null values.
        
        Args:
        
        NullHandler: optional, a class object that has a 'HandleNull' method
        
        **kwargs(optional)
            drop_percent: default 0.8,float,between 0 and 1. Columns having 
                more than drop_percent amount of null values will be
                dropped.

        
        """
        print('\t\t**Dropping Columns**\n')

        initial_num_cols = self.num_cols()
        
        NullHandler.drop_cols(self.data())
    
        final_num_cols = self.num_cols()

        return {'Columns removed':initial_num_cols-final_num_cols}
    
    
    @_print_decorator
    def impute(self,NullHandler=Imputer(),**kwargs):
        """Imputes columns.
        
        Imputes column based on default methods.
        
        Args:
        
        NullHandler(optinal): a class object have 'impute' method.
        
        **kwargs(optional)
            columns:default None, a list of str, Columns to impute.
                Default None means impute all columns in the
                dataframe
            num_method:default 'median', a str, Method to use to impute
                columns having numeric values. Possible options,
                'mean','bfill','ffill','interpolate','knn','median'
            cat_method: default 'mode', a str , Method to use to impute
                columns having categoric values. Possible options,
                'mode','bfill','ffill'
        """
        print('\t\t**Imputing Columns**\n')

        NullHandler.impute(self.data(),**kwargs)
        
        return {}
    
    @_print_decorator
    def random_impute(self,NullHandler = Imputer(),**kwargs):
        """Imputes null values randomly.
        
        Imputes null values randomly from the observed values in the
        column.
        
        Args:
            columns: default None, a list of str, Columns to impute.
                Default None means impute all columns in the 
                dataframe.
                
        """

        NullHandler.random_impute(self.data(),**kwargs)
        
        return {}
    
    @_print_decorator
    def impute_regression(self,NullHandler = Imputer(),**kwargs):
        """Imputes null values using regression.
        
        Imputes null values by doing regression on the observed values.
        
        Args:
            params: a list of str, columns to use as features for prediction
                Note: The columns to be used as predictor variables should
                not have any null values.
        """
        NullHandler.impute_regression(self.data(),**kwargs)
        
        return {}
    
    
    @_print_decorator
    def encoder(self,Enc=Encoder(),**kwargs):
        """Encodes the data.
        
        Encodes data using primary methods like LabelEncode
        
        Args:
            Column: a list of str, list of columns to encode
            thresh: above which LabelEncoded, below which OneHotEncoded
            
        """
        print('\t\t**Encoding Variables**\n')

        initial_num_cols = self.num_cols()
        
        Enc.encoder(self.data(),**kwargs)
        
        final_num_cols = self.num_cols()
        
        return {'Columns removed':initial_num_cols-final_num_cols}
    
    @_print_decorator
    def outlier_detection(self,Out = OutlierDetector(),**kwargs):
        """Detects outliers in the columns.
        
        Detects outliers using a variety of methods. Some are zscore,iqr,
        pca, dbscan
        
        Args:
            columns : a list of str, a list of columns to detect outliers
            methods: 'iqr','zscore','pca','dbscan'
        """
        print('\t\t**Outlier Detection**\n')

        Out.outlier_detection(self.data(),**kwargs)
        
        return {}
    
    @_print_decorator
    def outlier_pca(self,Out = OutlierDetector(),**kwargs):
        """Outlier detection using pca.
        
        Shows you can detect outliers using pca.
        NOTE: It is important 'columns' should not have any null values.
        
        Args:
            cols: columns to do pca on.
        """
        Out.outlier_pca(self.data(),**kwargs)
        
        return {}
    def plot(self,Plott = Plotter(),**kwargs):
        if 'x' not in kwargs and 'y' not in kwargs:
            print('Column name needed')
            return
        Plott.plot(self.data(),kwargs['x'],kwargs['y'])    
    def boxplot(self,Plott = Plotter(),**kwargs):
        if 'columns' not in kwargs:
            print('Column name needed')
            return
        Plott.boxplot(self.data(),kwargs['columns'])
        
    def barplot(self,Plott = Plotter(),**kwargs):
        if 'columns' not in kwargs:
            print('Column name needed')
            return
        Plott.barplot(self.data(),kwargs['columns'])
        
    def histogram(self,Plott = Plotter(),**kwargs):
        if 'columns' not in kwargs:
            print('Column name needed')
            return
        Plott.histogram(self.data(),kwargs['columns'])
        
    def scatterplot(self,Plott = Plotter(),**kwargs):
        if 'x' not in kwargs or 'y' not in kwargs:
            print('Need both column for x-axis and y-axis for scatter plot')
            return
        Plott.scatterplot(self.data(),kwargs['x'],kwargs['y'])
        
    def countplot(self,Plott = Plotter(),**kwargs):
        if 'x' not in kwargs or 'y' not in kwargs:
            print('Need both column for x-axis and y-axis for scatter plot')
            return
        Plott.countplot(self.data(),kwargs['x'],kwargs['y'])
        
    def lmplot(self,Plott = Plotter(),**kwargs):
        if 'x' not in kwargs or 'y' not in kwargs:
            print('Need both column for x-axis and y-axis for scatter plot')
            return
        Plott.lmplot(self.data(),kwargs['x'],kwargs['y'])

    def correlation(self,Stat = StatAnalysis(),**kwargs):
        print('\t\t**Correlation Ceofficient**')
        Stat.correlation(self.data())
        
    def anova(self,Stat=StatAnalysis(),target=None,**kwargs):
        print('\t\t**Anova Analysis**\n')
        if target is None:
            print('No target variable found to do anova')
            return
        if not is_numeric_dtype(self.data()[target]):
            print('Target variable has to be numeric')
            return
        Stat.anova(self.data(),target,**kwargs)
        
    def crosstab(self,Plott=Plotter(),**kwargs):
        if 'x' not in kwargs or 'y' not in kwargs:
            print('Need both column for x-axis and y-axis for crosstabulation')
            return
        print(pd.crosstab(self.data()[kwargs['x']],self.data()[kwargs['y']]))
        
#All the necessary checks I am doing here

    def calculate_woe_iv(self,dataset,feature,target):
        lst = []
        #replace isna by missing
        #if target is not binary return

        dataset[feature]=dataset[feature].apply(lambda ft : 'missing' if pd.isna(ft) else ft)
        for i in range(dataset[feature].nunique()):
            val = dataset[feature].unique()[i]
            lst.append({
                'Value':val,
                'All': dataset[dataset[feature]==val].count()[feature],
                'Good': dataset[(dataset[feature]==val) & (dataset[target]==dataset[target].unique()[1])].count()[feature],
                'Bad': dataset[(dataset[feature]==val) & (dataset[target]==dataset[target].unique()[0])].count()[feature]
            })
        dset = pd.DataFrame(lst)
        dset['Distr_Good'] = (dset['Good'])/dset['Good'].sum()
        dset['Distr_Bad'] = (dset['Bad'])/dset['Bad'].sum()
        dset['WoE'] = np.log(dset['Distr_Good']/dset['Distr_Bad'])
        dset = dset.replace({'WoE':{np.inf:0,-np.inf:0}})
        dset['IV'] = (dset['Distr_Good']-dset['Distr_Bad'])*dset['WoE']
        iv = dset['IV'].sum()
        dset.sort_values(by='WoE')
        dataset[feature]=dataset[feature].apply(lambda ft : pd.NA if ft=='missing' else ft)
    
        return dset,iv
    
    def woe(self,columns = None,target = None):
        df = self.data()
        if target is None:
            print('No target variable mentioned ')
            return
        final_columns = None
        if columns is None:
            final_columns = df.columns.values
        else:
            final_columns = columns
        for column in final_columns:
            if (column==target) or (not is_object_dtype(df[column])):
                continue
            else:
                print('WoE and IV for column: {}'.format(column))
                dfee,iv = self.calculate_woe_iv(df,column,target)
                print(dfee)
                print('IV Score: {:.2f}'.format(iv))
                print('\n')


    def pairplot(self,Plott=Plotter()):
        columns_to_plot = self.column_types()['numeric']
        print('Colums Used for pairplot',columns_to_plot)
        Plott.pairplot(self.data(),columns_to_plot)

    def describe(self):
        """Summary of columns in dataframe."""
        return self.data().describe()
    
    def automate(self):
        """Automate the EDA Process.
        
        Interacts with the user in performing Exploratory Data Analysis.
        """
        print('Automating Exploratory Data Analysis')
        print('The following steps will be automated')
        print('\t1. Drop Duplicates, drop rows, drop columns')
        print('\t2. Outlier Detection')
        print('\t3. Data Imputation')
        print('\t4. Statistical Analysis')
        print('Default Order: 1 2 3 4 ')
        print('If you want to change order, then input the numbers in reqd order ex: 3 1 2 4 1.\nNote that you can perform\
the same step again')
        order = [1,2,3,4]
        orde  = input('Order(Enter if no change): ')
        if len(orde)!=0:
            order = list(map(int,orde.split()))
        print()
        for ordd in order:
            if ordd==1:
                print('\n\t\t**Drop rows, drop columns**\n')
                self.drop_rows()
                self.drop_cols()
            elif ordd==2:
                print('\n\t\t**Outlier Detection**\n')
                self.outlier_detection()
            elif ordd==3:
                print('\n\t\t**Data Imputation**\n')
                print('Null value count(columnwise)')
                print(self.null_values())
                self.impute()
            elif ordd==4:
                print('\n\t\t**Statistical Analysis**\n')
                self.correlation()

