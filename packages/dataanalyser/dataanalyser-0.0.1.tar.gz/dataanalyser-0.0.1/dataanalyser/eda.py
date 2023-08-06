#Loading necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import normaltest
from .explorer import Explorer
from .preprocess import Preprocess

#target for supervised analysis
target = None

class Preprocessing(object):
	"""Class for Preprocessing"""

	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)
		
	def automate(self):
		"""Automates the preprocessing steps."""
		self.exp_obj.print_shape()
		self.exp_obj.preprocess()
		self.columns_info()
		display(self.data_info())
		self.describe_data()
		self.exp_obj.drop_duplicates()
		self.exp_obj.drop_rows()
		self.exp_obj.drop_cols()
		self.is_supervised()

	def is_supervised(self):
		"""Sets the target variable."""
		global target
		print('\t\t**Target Information**\n')
		type_of_analysis = input("Supervised or Unsupervised Analysis:(s for supervised,u for unsupervised: ")
		while type_of_analysis == 's':
			column = input('Enter Target Variable: ')
			if column in self.df.columns.values:
				target = column
				break
			else:
				print('Target varible not found in list of columns')

	def columns_info(self):
		"""Gives data types of the columns."""
		print('\t\t**Columns Information**')
		data_dict = self.exp_obj.column_types()
		for key in data_dict:
			print(key,':\t',len(data_dict[key]))
		for key in data_dict:
			print(key,':\t',data_dict[key])

	def data_info(self):
		"""Displays information about data such as null count etc."""
		print('\t\t**Data Information**')
		try:
			df = self.df
			df_info = pd.DataFrame(df.isna().sum(),columns = ['Null_count'])
			df_info['Non_Null_count'] = df_info.index.map(df.notna().sum())
			df_info['N_unique'] = df_info.index.map(df.nunique())
			df_info['D_types'] = df_info.index.map(df.dtypes)
			#df_info['Blank_count'] = df_info.index.map((df=='').sum())
			return df_info
		except:
			return 'Data Info failed: \nProblem with Column names -- Check for duplicate column names'

	def describe_data(self):
		"""Describes Dataset Properties."""
		print('\t\t**Dataset**')
		display(self.df.head())
		print('\t\t**Description of Numeric Variables**')
		display(self.df.describe())
		print('\t\t**Description of Categoric Variables**')
		display(self.df.describe(include=['object','datetime']))

class Visual(object):
	"""Class for Visual Analysis"""

	def __init__(self,data):
		global target
		self.df = data
		self.target = target
		self.exp_obj = Explorer(self.df)

	
	def automate(self):
		"""Automates the visual analysis process."""
		self.pairplot()
		self.correlation_plot()
		self.histogram()
		if self.target is not None:
			print('\t\t**Plots with Target Variable**')
			if Preprocess().get_col_type(self.df,self.target) == 'numeric':
				self.corr_numeric()
				self.boxplot_numeric()
				self.scatterplot()
			if Preprocess().get_col_type(self.df,self.target) == 'categoric':
				self.boxplot_category()
				self.contingency_table()

	def correlation_plot(self):
		"""Correlation between all numeric variables"""
		print('\t\t**Correlation Ceofficient**')
		plot = sns.heatmap(self.df.corr())
		plt.show()

	def pairplot(self):
		"""Pairplot of numeric varialbles with each other"""
		try: 
			print('\t\t**Pairplot**')
			numeric_vars = self.exp_obj.column_types()['numeric']
			g = sns.PairGrid(self.df[numeric_vars].sample(100,replace=True))
			g.map_diag(plt.hist)
			g.map_offdiag(plt.scatter)
			plt.figure()
			plt.show()
		except:
			pass

	def scatterplot(self):
		"""Scatter plots of all numeric variables."""
		numeric_vars = self.exp_obj.column_types()['numeric']
		for var in numeric_vars:
			if var==self.target:
				continue
			my = sns.relplot(x=var,y=self.target,data=self.df)
			plt.show()

	def histogram(self):
		"""Frequency distribution of all variables"""
		print('\t\t**Distribution of all columns**')
		plot = self.df.hist(figsize=(30,30))
		fig = plot[0][0].get_figure()
		plt.show()

	def boxplot_category(self):
		"""Boxplot of categoric target with al numeric variables"""
		numeric_vars = self.exp_obj.column_types()['numeric']
		for col in numeric_vars:
			my = sns.catplot(x=self.target,y=col,kind='box',data=self.df)
			plt.show()

	def boxplot_numeric(self):
		"""Boxplot of numeric target with different categoric variables"""
		categoric_vars = self.exp_obj.column_types()['categoric']
		for col in categoric_vars:
			my = sns.catplot(x=col,y=self.target,kind='box',data=self.df)
			plt.show()

	def corr_numeric(self):
		"""Correlation table for numeric variables."""
		display(pd.DataFrame(self.df.corrwith(self.df[self.target]),columns=['correlation-coefficient']))

	def contingency_table(self):
		"""If target is categoric then contigency table for categoric variables"""
		pass

class Outlier(object):
	"""Class for Outlier Detection."""
	def __init__(self,data):
		self.df = data
		self.exp_obj = Explorer(self.df)

	def automate(self):
		"""Automates the Outlier Analysis"""
		self.exp_obj.outlier_detection()
		self.outlier_categoric()

	def detect_outliers(self,**kwargs):
		"""Detects outliers for numeric variables."""
		self.exp_obj.outlier_detection(**kwargs)

	def outlier_categoric(self):
		"""Detects outliers for categoric variables."""
		pass

class Imputation(object):
	"""Class for Imputation."""

	def __init__(self,data):
		self.df=data
		self.exp_obj = Explorer(self.df)
	
	def impute(self,**kwargs):
		"""Imputes both numeric and categoric variables"""
		self.exp_obj.impute(**kwargs)

	def automate(self):
		"""Automates the imputation process."""
		self.exp_obj.impute()


class Testing(object):
	"""Statistical Testing Class"""

	def __init__(self,data):
		global target
		self.df = data
		self.target = target
		self.exp_obj = Explorer(self.df)

	def automate(self):
		"""Automates the process of statistical testing."""
		self.normality()
		if self.target is not None and Preprocess().get_col_type(self.df,self.target) == 'numeric':
			self.anova()

	def normality(self):
		"""Tests whether numeric variables follow a normal distribution or not."""
		print('\t\t**Normality Testing**\n')
		numeric_vars = self.exp_obj.column_types()['numeric']
		statistic = []
		pvalue = []
		for var in numeric_vars:
			if(self.df[var].isna().sum()!=0):
				print(var,' :null values_found')
				statistic.append(0)
				pvalue.append(0)
				continue
			v,p = normaltest(self.df[var])
			statistic.append(v)
			pvalue.append(p)
		result = pd.DataFrame({'statistic':statistic,'p-value':pvalue},index=numeric_vars)
		display(result)

	def anova(self):
		"""ANOVA Testing for categoric variables with a numeric target."""
		self.exp_obj.anova(target=self.target)
#chi-squared test of independence for category vs category
#anova test for category vs numeric
"""
When I create a html file - remember I am going to autogenerate a html file
I will have one file that will be inside the report directory I create. every time I write ssomething I write there.
"""