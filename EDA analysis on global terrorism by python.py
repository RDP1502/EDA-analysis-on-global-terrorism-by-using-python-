#!/usr/bin/env python
# coding: utf-8

# ### Task 4 : Perform ‘Exploratory Data Analysis’ on dataset ‘Global Terrorism’
# 
# 
# 
# GRIP June'24
# ![Sparks%20foundation.png](attachment:Sparks%20foundation.png)

# **By Rohan Pawar**

# In[1]:


#importing useful libraries
import numpy as np
import pandas as pd
import seaborn as sns; sns.set(color_codes=True)
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[6]:


terr_df = pd.read_csv('D:\Python Program\globalterrorismdb_0718dist.csv',  encoding ='ISO-8859-1', low_memory=False)


# In[7]:


terr_df


# ## Understanding the Data

# In[8]:


terr_df.shape


# In[9]:


terr_df.columns


# In[10]:


terr_df.dtypes


# In[11]:


terr_df.describe()


# In[12]:


terr_df.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'State',
                          'region_txt':'Region','attacktype1_txt':'Attack_Type','target1':'Target','nkill':'Killed',
                          'nwound':'Wounded','gname':'Group','targtype1_txt':'Target_Type',
                          'weaptype1_txt':'Weapon_type','latitude':'Latitude',
                          'longitude':'Longitude','target1':'Target','city':'City'},inplace=True)


# In[13]:


# percentage of missing values in our dataset
missing_values = (((terr_df.isnull().sum()).sum())/terr_df.size)*100
missing_values


# More than 50% values are Null, we need to clean the Dataset first

# In[14]:


# creating dataframe with necessary columns only
terr_df = terr_df[['Year','Month','Day','Country','State','Region','City','Latitude','Longitude','Attack_Type','Killed',
              'Wounded','Group','Target','Target_Type','Weapon_type']]
terr_df.head(10)


# In[15]:


for i in terr_df.columns:
    print(i,terr_df[i].nunique())


# In[16]:


terr_df.info()


# As we can see, 'Wounded' and 'Killed' Attributes have lots of Null values, need to fill null values

# In[17]:


terr_df['Wounded'] = terr_df['Wounded'].fillna(0).astype(int)
terr_df['Killed'] = terr_df['Killed'].fillna(0).astype(int)


# In[18]:


terr_df.info()


# **Cleaned Data**

# In[19]:


terr_df.head(10)


# # Univariate Analysis

# In[20]:


terr_df['Attack_Type'].value_counts()


# In[22]:


(terr_df['Attack_Type'].value_counts()/terr_df.shape[0])*100


# In[33]:


# 10 most attacked targets

plt.figure(figsize = (11,6))
sns.histplot(terr_df['Attack_Type'], palette='cubehelix')
plt.title('Attack Types',fontsize=15)
plt.xticks(rotation=90)
plt.show()


# **Conclusion** : 50% of the Attack happened with Bombing/Explosion 
# - 10-20% of the Attack happened with Armed Assault and Assassination rest are in between 0-6%

# ## Terrorist Targets: The Ten Countries Which Suffer Most From Terrorism

# In[34]:


terr_df.Country.value_counts()[:10]


# In[39]:


import matplotlib.pyplot as plt
import seaborn as sns


plt.figure(figsize=(12, 7))
sns.barplot(x=terr_df['Country'].value_counts()[:10].index, 
            y=terr_df['Country'].value_counts()[:10].values, 
            palette='viridis')
plt.title('Top 10 Countries Affected')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()


# According to research, Iraq is the most affected country by terrorism, then comes Pakistan and Afganistan.

# In[40]:


(terr_df['Target_Type'].value_counts().head(10)/terr_df['Target_Type'].shape[0])*100


# In[19]:


# 10 most attacked targets
plt.figure(figsize = (11,6))
sns.barplot(terr_df['Target_Type'].value_counts().head(10).index, terr_df['Target_Type'].value_counts().head(10).values, 
            palette='magma')
plt.title('Top 10 most attacked targets',fontsize=25)
plt.xlabel('Targets',fontsize=25)
plt.ylabel('Number of attacks',fontsize=25)
plt.xticks(rotation=90)
plt.show()


# **This Graph demonstrates:**
# - The most Attacked Target is 'Private Citizens & Property' which is approximately 25%
# - 10-20% is the Target which is 'Military','Police', 'Government', 'Business'   

# In[42]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
# Regions with most attacks
sns.barplot(x=terr_df['Region'].value_counts().index, 
            y=terr_df['Region'].value_counts().values, 
            palette='flare')
plt.title('Most Attacked Regions', fontsize=25)
plt.xlabel('Regions', fontsize=25)
plt.ylabel('Number of Attacks', fontsize=25)
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
# Top 10 most attacked states
sns.barplot(x=terr_df['State'].value_counts().head(15).index, 
            y=terr_df['State'].value_counts().head(15).values, 
            palette='viridis')
plt.title('Top 10 Most Attacked States', fontsize=25)
plt.xlabel('States', fontsize=25)
plt.ylabel('Number of Attacks', fontsize=25)
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


# **With these Graphs, we can conclude that :**
# - Most Attacked Region is 'Middle East and North Africa' then comes South Asia 
# - Most Attacked States is 'Baghdad'

# In[43]:


(terr_df['Weapon_type'].value_counts().head()/terr_df['Weapon_type'].shape[0])*100


# In[44]:


import matplotlib.pyplot as plt
import seaborn as sns

# Top 5 most used weapons types in terror attacks
plt.figure(figsize=(10, 7))
sns.barplot(x=terr_df['Weapon_type'].value_counts().head().index, 
            y=terr_df['Weapon_type'].value_counts().head().values, 
            palette='flare')
plt.title('Top 5 Most Used Weapon Types', fontsize=15)
plt.xlabel('Weapon Types', fontsize=15)
plt.ylabel('Number of Weapons Used', fontsize=15)
plt.show()


# - Almost 50% of Weapon used is 'Explosives' whereas 32% 'Firearms' used in the terrorism

# In[45]:


x_year = terr_df['Year'].unique()
y_count_years = terr_df['Year'].value_counts(dropna = False).sort_index()
plt.figure(figsize = (12,7))
sns.barplot(x = x_year,
           y = y_count_years,
           palette = 'dark:salmon_r')
plt.xticks(rotation = 90)
plt.xlabel('Attack Year')
plt.ylabel('Number of Attacks each year')
plt.title('Attack_of_Years')
plt.show()


# **This graphs shows**
# - 2014 appears to be witness of a huge terrorist attacks
# - 2014 onwards recorded a large increase in attacks of terrorism. 

# In[46]:


plt.figure(figsize = (12,7))
terr_df.groupby(['Year'])['Killed'].sum().plot(kind='bar',colormap='summer')
plt.title('Number of Deaths in different years',fontsize=25)
plt.xlabel('Years',fontsize=25)
plt.ylabel('Number of Deaths',fontsize=25)
plt.xticks(rotation=90)
plt.show()


# Number of deaths caused by terrorism is more between 2014 and 2018, with on an average >50K people being killed.
# High peak went to 2014 with 45K+ deaths.

# In[48]:


import matplotlib.pyplot as plt
import seaborn as sns

# Plotting KDE plot
plt.figure(figsize=(12, 7))
sns.kdeplot(data=terr_df, x='Year', hue='Region', fill=True)
plt.title('Terrorist Activities by Region in each Year', fontsize=25)
plt.xlabel('Years', fontsize=25)
plt.ylabel('Frequency of Attacks', fontsize=25)
plt.xticks(rotation=90)
plt.show()


# ## Bivariate Analysis

# In[49]:


plt.subplot(1,2,1)

terr_df.groupby(['Region'])['Wounded'].sum().sort_values(ascending = False).plot(kind='bar',colormap='rocket')
plt.title('Regions having Wounded People',fontsize=15)
plt.xlabel('Region',fontsize=15)
plt.ylabel('Number of Wounded',fontsize=15)
plt.xticks(rotation=90)

plt.subplot(1,2,2)
terr_df.groupby(['Region'])['Killed'].sum().sort_values(ascending = False).plot(kind='bar',colormap='rocket')
plt.title('Regions having Killed People',fontsize=15)
plt.xlabel('Region',fontsize=15)
plt.ylabel('Number of Killed',fontsize=15)
plt.xticks(rotation=90)
plt.gcf().set_size_inches(15, 5)


# 'Middle East & North Africa' has the most Killed people (>1.4 Lacs) and wounded people (>2 lacs)

# In[50]:


plt.subplot(1,2,2)

df1=terr_df.groupby(['Country'])['Wounded'].sum().sort_values(ascending = False).head(10).plot(kind='bar',colormap='winter')
plt.title('Country having Wounded People',fontsize=15)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Number of Wounded',fontsize=15)
plt.xticks(rotation=90)

plt.subplot(1,2,1)
terr_df.groupby(['Country'])['Killed'].sum().sort_values(ascending = False).head(10).plot(kind='bar',colormap='winter')
plt.title('Country having Killed People',fontsize=15)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Number of Killed',fontsize=15)
plt.xticks(rotation=90)
plt.gcf().set_size_inches(15, 5)


# 'Iraq' has the most Killed people (>70K) and wounded people (>1.2 lacs)
# Afganistan, pakistan and India all saw peak deaths while Iraq, which has overtaken all of these at the top of the table, suffered 37,700 more fatalities.

# In[51]:


plt.figure(figsize=(10,10))
sns.barplot(terr_df['Group'].value_counts()[1:11].values, terr_df['Group'].value_counts()[1:11].index,palette='rocket')
plt.title('Top 10 Terrorist Organization with Highest Terror Attacks',fontsize=15)
plt.xlabel('Number of Attacks',fontsize=15)
plt.ylabel('Terrorist Groups',fontsize=15)
plt.show()


# In[52]:


terr_df_tal = terr_df[terr_df.Group == 'Taliban']


# In[53]:


import matplotlib.pyplot as plt
import seaborn as sns

# Plotting the bar plot
plt.figure(figsize=(13, 7))
sns.barplot(x=terr_df_tal['Year'].value_counts().index, 
            y=terr_df_tal['Year'].value_counts().values, 
            palette='viridis')
plt.title('Terror Attack over the years by Taliban', fontsize=15)
plt.xlabel('Years', fontsize=15)
plt.ylabel('Number of Attacks', fontsize=15)
plt.xticks(rotation=90)
plt.show()


# In[54]:


plt.figure(figsize=(13,7))
terr_df_tal.groupby(['Year'])['Killed'].sum().plot(kind='bar',colormap='RdBu')
plt.title('People Killed by Taliban over the Years',fontsize=15)
plt.xlabel('Years',fontsize=15)
plt.ylabel('Number of people killed',fontsize=15)
plt.xticks(rotation=90)
plt.grid()
plt.show()


# Taliban killed more than 5000 people during 2015 after that a decreasing trend could be seen but still the numbers are very high.

# In[55]:


# creating new dataframe for the year 2014
terr_df_2014 = terr_df[terr_df.Year == 2014]


# In[57]:


import matplotlib.pyplot as plt
import seaborn as sns

# Plotting the bar plots
plt.figure(figsize=(15, 5))

# Regions that were attacked most in 2014
plt.subplot(1, 2, 1)
sns.barplot(x=terr_df_2014['Region'].value_counts().index, 
            y=terr_df_2014['Region'].value_counts().values, 
            palette='magma')
plt.title('Most Attacked Region in 2014', fontsize=15)
plt.xlabel('Regions', fontsize=15)
plt.ylabel('Number of Attacks', fontsize=15)
plt.xticks(rotation=90)

# Top 10 countries that were attacked most in 2014
plt.subplot(1, 2, 2)
sns.barplot(x=terr_df_2014['Country'].value_counts().head(10).index, 
            y=terr_df_2014['Country'].value_counts().head(10).values, 
            palette='magma')
plt.title('Top 10 Most Attacked Country in 2014', fontsize=15)
plt.xlabel('Country', fontsize=15)
plt.ylabel('Number of Attacks', fontsize=15)
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


# **With these Graphs, we can conclude that :**
# - In 2014, Most Attacked Region 'Middle East and North Africa' then comes South Asia 
# - In 2014, Most Attacked Country is 'Iraq'

# In[58]:


plt.subplot(1,2,1)
terr_df_2014.groupby(['Country'])['Killed'].sum().sort_values(ascending = False).head(10).plot(kind='bar',colormap='RdBu')
plt.title('Top 10 countries with max people killed in 2014',fontsize=15)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Number of people killed ',fontsize=15)
plt.xticks(rotation=90)

plt.subplot(1,2,2)
terr_df_2014.groupby(['Country'])['Wounded'].sum().sort_values(ascending = False).head(10).plot(kind='bar',colormap='spring')
plt.title('Top 10 countries with max people wounded in 2014',fontsize=15)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Number of people Wounded',fontsize=15)
plt.xticks(rotation=90)
plt.gcf().set_size_inches(15, 5)


# ## Conclusion
# **After performing the Exploratory Data Analysis we get the following insights from the data:**
# 
# - Private Citizens and Property were attacked most followed by Military, Police, Government and so on.
# - Middle East & North Africa was most affected among the top affected region. Most of the people in this region were either wounded or killed.
# - Iraq was the country which was most affected by terror attacks and had maximum number of killed and wounded people.
# - The State and City that was most affected was Baghdad
# - In the last decade 2014 had most number of terror attacks. That was around 16500 attacks during this year which means on average 45 attacks per day.
# - The most common attack type was Bombing/Explosion.
# - Explosives have been consistently the most popular weapon of choice for terrorists.
# - Taliban became more active since 2012 and they are responsible for the most of the terror attacks
# 
# **Recommendation**
# - Since Private Citizens and Property are being targeted consistently so stronger security and surveillance should be provided, especially in the dense populated regions.
# - More surveillance is required especially in the Middle East & North African Regions.
# - Strict border policy should be implemented to prevent the movement of explosives between the regions.

# In[ ]:




