#This is just a very quick hacked out script to scrape UK sectoral balances
#from the ONS website and produce some sectoral balance charts. I will aim
#to work this up in to something more formal when I can, but I wanted to get
#a proof of concept out there now...
#I code python in Visual Studio code, and have used their cell mode for running
#interactively with an integrated Jupyter notebook

#%%
import urllib.request 
import pandas as pd
import matplotlib.pyplot as plt
#%%
#Get file from the ONS website
ons_econ_home = 'https://www.ons.gov.uk/file?uri=/economy/nationalaccounts'
ons_sector_accounts = ons_econ_home + '/uksectoraccounts/datasets/unitedkingdomeconomicaccountsuktotaleconomy/current/'
year = '2018'
quarter = 'q4'
sb_url = ons_sector_accounts + 'ukea' + year + quarter + 'reftable2uksector.xls'
print(sb_url)

#Need the opener otherwise we get a 403 access denied error
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

url=''
local=''
(filename, header) = urllib.request.urlretrieve(sb_url)
print(filename)
print(header)

#%%
#Use pandas to get data into spreadsheet
dfs = pd.read_excel(filename, sheet_name='1.6.B9')
print(dfs)
#%%
def plot_aggregate_balances(dfs, start_row, end_row):
    '''Plot aggregate balance given input pandas datasheet
    requires knowing row and column indices, will aim to automate
    these by looking for keywords'''
    
    period_labels = dfs.iloc[start_row:end_row,0]
    corp_non_fin = dfs.iloc[start_row:end_row,3]
    corp_fin = dfs.iloc[start_row:end_row,4]
    households = dfs.iloc[start_row:end_row,12]
    rest_of_world = dfs.iloc[start_row:end_row,13]

    gov_all = dfs.iloc[start_row:end_row,8]
    private_all = corp_non_fin+corp_fin+households+rest_of_world
    x = range(0, len(period_labels))

    plt.figure() #Create a new window
    plt.plot(x, gov_all, 'b-', label='Government all')
    plt.plot(x, private_all, 'r-', label='Private sector all')
    plt.xticks(x, period_labels, rotation=90)
    plt.legend()
    plt.show()
#%%
#Show annual data
plot_aggregate_balances(dfs, 7, 39)

#Show seasonally adjusted quarterly data (available post 2011)
plot_aggregate_balances(dfs, 270, 302)
