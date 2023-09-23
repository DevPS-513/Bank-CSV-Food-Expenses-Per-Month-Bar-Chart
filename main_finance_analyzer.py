import pandas as pd
import numpy as np
import re
import glob 
import matplotlib.pyplot as plt
import calendar
from myfunctions import myfunctions as mf # Import custom functions so I can access as mf.Find... ect
import os


# Force the file to run from the same directory the file is in
current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
os.chdir(current_directory)

# Initialize keywords
fast_food_keywords = ["FRESHII","WENDYS", "MCDONALD'S", "BURGER", "SUBWAY", "TIM HORTONS", "KFC", "PIZZA", "BURRITO", "TACO BELL","SKIPTHEDISHES","DOORDASH"]
grocery_store_keywords = ["LOBLAW", "FRESHCO","LOBLAWS"]
keyword_list_dictionary={'fast food':fast_food_keywords,'grocery':grocery_store_keywords}

# Load all csv files and combine them
csv_files=glob.glob('./data_cleaned/account*.csv')
df_list=[]

for file in csv_files:
    df=pd.read_csv(file,names=['date','descr','expense','refund','total'],header=None,index_col=None)
    df_list.append(df)

combined_df=pd.concat(df_list,ignore_index=True)


# get the month as a string
combined_df['date']=pd.to_datetime(combined_df['date'])
combined_df['month']=combined_df['date'].dt.month
combined_df['month']=combined_df['month'].map(lambda x: calendar.month_name[x])

# Define a new column to categorize the purchase
combined_df['type']='uncategorized'
combined_df[['type','used-keyword']]=combined_df['descr'].apply(lambda x: pd.Series(mf.Find_Match_From_Keyword_List(x,keyword_list_dictionary,"uncategorized")))

# Print to the console
print(combined_df[(combined_df['type']=='fast food')|(combined_df['type']=='grocery')])

# Get the list of keywords used for each type
used_fast_food_keywords=np.unique(combined_df[combined_df['type']=='fast food']['used-keyword'])
used_grocery_keywords=np.unique(combined_df[combined_df['type']=='grocery']['used-keyword'])

# Get the sum per month for each category
df1=combined_df[(combined_df['type']=='fast food')].copy()
df1=df1.groupby('month')
fast_food_series=df1['expense'].sum()

df1=combined_df[(combined_df['type']=='grocery')].copy()
df1=df1.groupby('month')
grocery_series=df1['expense'].sum()
month_series=grocery_series.index.values

# Solve for the average spent over all months
combined_list=fast_food_series+grocery_series
avg_value=np.mean(combined_list)

# Plot the results
plt.figure(0)
plt.bar(month_series,fast_food_series,color='blue',alpha=.6,label='fast food /mo')
plt.bar(month_series,grocery_series,color='green',alpha=.6,label='grocery /mo',bottom=fast_food_series)
# Put text boxes in the middle of each bar
for i,month in enumerate(month_series):
    value=int(np.round(fast_food_series[i],0))
    plt.text(month,value/2,'\$'+str(value),va='center',ha='center',
             bbox={'facecolor': 'lightgrey', 'edgecolor': 'black'})
    value=value+int(np.round(grocery_series[i]/2,0))
    plt.text(month,value,'\$'+str(value),va='center',ha='center',
            bbox={'facecolor': 'lightgrey', 'edgecolor': 'black'})
    
# print the list of keywords used
str1=r'$\bf{Fast\ Food\ Keywords}$:'+'\n'
for keyword in used_fast_food_keywords:
    str1=str1+keyword+"\n"

str1=str1+r'$\bf{Grocery\ Keywords}$:'+'\n'
for keyword in grocery_store_keywords:
    str1=str1+keyword+"\n"

plt.subplots_adjust(right=.7)

plt.text(1.02,.5,str1,transform=plt.gca().transAxes,va='center')
plt.plot([month_series[0],month_series[-1]],[avg_value,avg_value],label=f"Measured Value:{avg_value:.1f}",linestyle=":",marker="x")
plt.plot([month_series[0],month_series[-1]],[388,388],label=f"Target Value:{388.0}",linestyle=":",marker="^")
plt.xlabel('Month')
plt.ylabel('Dollars $')
plt.legend()
plt.savefig('./monthly_bar_chart.png')


# Now lets calculate how much per year we could save if we spent the recommended amount
years=np.arange(2023,2033,1)
amount=(np.abs(avg_value-388)*12)*(years-2023) # amount saved per year

plt.figure(2)
plt.plot(years,amount,label='Total Saved in 10 years: ${:,}'.format(np.round(amount[-1])))
plt.bar(years,amount)
plt.legend()
plt.title("Total Estimated Savings @ $388.0/mo")
plt.xlabel('Year')
plt.ylabel('Total Saved $')
plt.savefig('./output_savings_over_10_years.png')
plt.show()
print('..done')