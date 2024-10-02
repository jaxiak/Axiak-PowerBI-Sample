import pandas as pd

df1 = pd.read_csv('input/RegionLabels.csv')

df1['Country'] = df1['Country'].str.strip()

df2 = pd.read_csv('countries of the world.csv')


df2['Country'] = df2['Country'].str.strip()
df2['Region'] = df2['Region'].str.strip()

for col in ['Pop. Density (per sq. mi.)',
       'Coastline (coast/area ratio)', 'Net migration',
       'Infant mortality (per 1000 births)', 'Literacy (%)',
       'Phones (per 1000)', 'Arable (%)', 'Crops (%)', 'Other (%)', 'Climate',
       'Birthrate', 'Deathrate', 'Agriculture', 'Industry', 'Service']:
    df2[col] = df2[col].str.replace(',', '.').astype('float64')



df2['TransactionRegion'] = df2['Country'].map(df1.set_index('Country')['Region'])

df2['GDP'] = df2['Population'] * df2['GDP ($ per capita)']

df3 = df2[~pd.isna(df2['TransactionRegion'])] 
pd.options.mode.chained_assignment = None        #This SettingWithCopyWarning will not go away even when we correctly set values to the view rather than the copy.


ratio_columns = {'Population':['Net migration', 'Infant mortality (per 1000 births)', 'Literacy (%)', 'Phones (per 1000)',  'Birthrate', 'Deathrate'],
                 'GDP' :  ['Agriculture', 'Industry', 'Service'],
                 'Area (sq. mi.)' : ['Coastline (coast/area ratio)', 'Arable (%)', 'Crops (%)', 'Other (%)']}

totals_df = df3.groupby('TransactionRegion')[list(ratio_columns.keys())].sum()

def propna_sum(series, threshold = 0.05):  #propogates NaN if more than the threshold amount of values is NaN
    import numpy as np
    if series.isna().sum() / len(series) > threshold:
        return np.nan
    return series.sum()

agg_funct_dict = {}

for total_col in ratio_columns:
    df3['Region' + total_col] = df3['TransactionRegion'].map(totals_df[total_col])
    agg_funct_dict[total_col] = propna_sum
    for ratio_col in ratio_columns[total_col]:
       df3.loc[df3.index, 'Adjusted' + ratio_col] = df3[ratio_col] * df3[total_col] / df3['Region' + total_col]
       agg_funct_dict['Adjusted' + ratio_col] = propna_sum

agg_funct_dict['Region'] = lambda x: pd.Series.mode(x)[0]


for col in df2.columns:
       if (('Adjusted' + col) not in agg_funct_dict) and (col not in agg_funct_dict) and (col not in ['Country', 'Pop. Density (per sq. mi.)', 'GDP ($ per capita)', 'TransactionRegion']):
            agg_funct_dict[col] = 'mean'
       #      print(col)



regions_df =  df3.groupby('TransactionRegion').aggregate(agg_funct_dict, skipna = False)

column_renamer = {}
for total_col in ratio_columns:
       for ratio_col in ratio_columns[total_col]:
              column_renamer['Adjusted' + ratio_col] = ratio_col

regions_df = regions_df.rename(columns = column_renamer)
regions_df['Country'] = regions_df.index
regions_df['TransactionRegion'] = regions_df.index
regions_df['Pop. Density (per sq. mi.)'] = regions_df['Population'] / regions_df['Area (sq. mi.)']
regions_df['GDP ($ per capita)'] = regions_df['GDP'] / regions_df['Population']

regions_df = regions_df[df2.columns]

df4 = pd.concat([df2, regions_df], axis = 0)
# print(df1)
# print(df2)
# print(df3)
# print(totals_df)
# print(regions_df)
# print(regions_df[['Population', 'Literacy (%)']])
# print(df4)
# for total_col in ratio_columns:
#      for region in regions_df.index:
#        print(df3[df3['TransactionRegion'] == region][[ 'TransactionRegion','Country', total_col] + ratio_columns[total_col]])
#        print(df4[df4['TransactionRegion'] == region][[ 'TransactionRegion', 'Country',total_col] + ratio_columns[total_col]])
#        breakpoint()

df1.to_csv('output/RegionLables.csv')
df4.to_csv('output/Countries.csv', index = False)