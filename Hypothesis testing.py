

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# Hypothesis Testing
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. Only look at GDP data from the first quarter of 2000 onward.
# 
# 
# In[ ]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[2]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    import pandas as pd
    
    univ_towns = pd.read_csv('university_towns.txt',sep='\t', header = None,names=['Location'],encoding='latin-1')
    towns = []
    city_univ_towns = pd.DataFrame(columns=["State", "RegionName"])
    univ_towns['Location'] = univ_towns['Location'].apply(lambda x: x.split('(',1)[0])
    univ_towns['flag'] = univ_towns['Location'].str.contains('edit')
        
    for index, row in univ_towns.iterrows():
        if 'edit' in row['Location']:
            x = univ_towns.iloc[index] ['Location']
        towns.append(x + ' , '  +univ_towns.iloc[index] ['Location'])
      
    univ_towns['Location'] = towns
    univ_towns =  univ_towns[univ_towns['flag'] == False]
    
    city_univ_towns = pd.DataFrame(univ_towns.Location.str.split(',',1).tolist(),
                                   columns = ["State", "RegionName"])
    city_univ_towns['State'] = city_univ_towns['State'].apply(lambda x: x.split('[',1)[0])
    
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    inv_map = {v: k for k, v in states.items()}
    city_univ_towns =  city_univ_towns.replace({"State": inv_map})
    
    return city_univ_towns
    
get_list_of_university_towns()


# In[3]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    GDPs = pd.read_excel('gdplev.xls', header=219, skiprows=None, names = ["Yr/Qtr", 'GDP', 'GDP-c'], parse_cols="E:G", encoding='latin-1')
    GDPs['diff'] = GDPs['GDP-c'].diff()    
    
    for index, row in GDPs.iterrows():
        if ((GDPs.iloc[index] ['diff'] < 0) and (GDPs.iloc[index+1] ['diff'] < 0)):
            return GDPs.iloc[index] ['Yr/Qtr']
            
    return 'No recession'

get_recession_start()


# In[4]:

def get_recession_start_index():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    GDPs = pd.read_excel('gdplev.xls', header=219, skiprows=None, names = ["Yr/Qtr", 'GDP', 'GDP-c'], parse_cols="E:G", encoding='latin-1')
    GDPs['diff'] = GDPs['GDP-c'].diff()    
    
    for index, row in GDPs.iterrows():
        if ((GDPs.iloc[index] ['diff'] < 0) and (GDPs.iloc[index+1] ['diff'] < 0)):
            return index
            
    return 'No recession'

get_recession_start_index()


# In[45]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    GDPs = pd.read_excel('gdplev.xls', header=219, skiprows=None, names = ["Yr/Qtr", 'GDP', 'GDP-c'], parse_cols="E:G", encoding='latin-1')
    GDPs['diff'] = GDPs['GDP-c'].diff()    
    for index, row in GDPs.iterrows():
        if ((index > get_recession_start_index()) and (GDPs.iloc[index] ['diff'] > 0) and (GDPs.iloc[index+1] ['diff'] > 0)):
            return GDPs.iloc[index+1] ['Yr/Qtr']
    
    return "It never started"

get_recession_end()


# In[6]:

def get_recession_end_index():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    GDPs = pd.read_excel('gdplev.xls', header=219, skiprows=None, names = ["Yr/Qtr", 'GDP', 'GDP-c'], parse_cols="E:G", encoding='latin-1')
    GDPs['diff'] = GDPs['GDP-c'].diff()    
    for index, row in GDPs.iterrows():
        if ((index > get_recession_start_index()) and (GDPs.iloc[index] ['diff'] > 0) and (GDPs.iloc[index+1] ['diff'] > 0)):
            return index
    
    return "It never started"

get_recession_end_index()


# In[7]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    GDPs = pd.read_excel('gdplev.xls', header=219, skiprows=None, names = ["Yr/Qtr", 'GDP', 'GDP-c'], parse_cols="E:G", encoding='latin-1')
    GDPs['diff'] = GDPs['GDP-c'].diff()    
    GDPs_Recession = GDPs[(GDPs.index >= get_recession_start_index())] 
    GDPs_Recession = GDPs_Recession[(GDPs_Recession.index < get_recession_end_index())]
    index = GDPs_Recession['GDP-c'].idxmin()
    
    return  GDPs.iloc[index] ['Yr/Qtr'] 

get_recession_bottom()


# In[10]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    import pandas as pd
    
    home_price = pd.read_csv('City_Zhvi_AllHomes.csv',sep=',',) # header = None,names=['Location'],encoding='latin-1')
    dat_cols = home_price.ix[:,'2000-01':]
    dat_cols_qtr = dat_cols.groupby(pd.PeriodIndex(dat_cols.columns, freq='Q'), axis=1).mean()
    home_price = home_price[['RegionName','State']].join(dat_cols_qtr)
    home_price.set_index(['State','RegionName'], inplace=True)  
    return home_price

convert_housing_data_to_quarters()


# In[44]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    import pandas as pd
    from scipy import stats
    
    
    home_price = pd.read_csv('City_Zhvi_AllHomes.csv',sep=',',) # header = None,names=['Location'],encoding='latin-1')
    dat_cols = home_price.ix[:,'2000-01':]
    dat_cols_qtr = dat_cols.groupby(pd.PeriodIndex(dat_cols.columns, freq='q'), axis=1).mean()
    home_price = home_price[['RegionName','State']].join(dat_cols_qtr)
    #home_price.set_index(['State','RegionName'], inplace=True)  
    home_price.columns = home_price.columns.astype(str)
    home_price_qtrs = home_price.loc[:, get_recession_start().upper(): get_recession_bottom().upper()] 
    home_price = home_price[['RegionName','State']].join(home_price_qtrs)
    univ = get_list_of_university_towns()
    k = [x.replace(' ', '') for x in univ['RegionName'].tolist()]
    univ_home_Price = home_price[home_price['RegionName'].isin(k)]
    univ_home_Price['Diff'] = univ_home_Price[get_recession_start().upper()]- univ_home_Price[get_recession_bottom().upper()]
    non_univ_home_Price = home_price[home_price['RegionName'].isin(k)==False]
    non_univ_home_Price['Diff'] = non_univ_home_Price[get_recession_start().upper()]- non_univ_home_Price[get_recession_bottom().upper()]
    
    univ_home_Price = univ_home_Price[univ_home_Price['Diff'].notnull()]
    non_univ_home_Price = non_univ_home_Price[non_univ_home_Price['Diff'].notnull()]
    
    t = stats.ttest_ind(univ_home_Price['Diff'],non_univ_home_Price['Diff'])
   
    
    return (True,t[1] ,'university town') #univ_home_Price

run_ttest()


# In[ ]:




# In[ ]:




# In[ ]:



