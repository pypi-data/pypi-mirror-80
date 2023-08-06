To install the package 'dataanalyser'
1. Enter this folder through terminal
2. pip install -r requirements.txt
3. pip install .--user

To use the package 'dataanalyser'
	from dataanalyser.eda import Preprocessing,Visual,Outlier,Imputation,Testing
	import pandas as pd
	dataframe = pd.read_csv('filename')
	Preprocessing(dataframe).automate()
	Visual(dataframe).automate()
	Outlier(dataframe).automate()
	Imputation(dataframe).automate()
	Testing(dataframe).automate()
