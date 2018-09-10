# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

#-------------------------------------------------------------
total_players = purchase_data["SN"].nunique()
total_players
#-------------------------------------------------------------

#purchasing analsys total
unique_items = purchase_data["Item ID"].nunique()
avg_price= '${:,.2f}'.format(purchase_data["Price"].mean())
total_purchases = purchase_data['Item ID'].count()
total_rev= '${:,.2f}'.format(purchase_data["Price"].sum())
summary = {'Number of Unique Items':[unique_items], 'Average Price': [avg_price], 'Number of Purchases': [total_purchases], 'Total Revenue': [total_rev]}
summary_table = pd.DataFrame(data=summary)
summary_table

#------------------------------------------------------------
#Gender Demographics
cleaned_gender = purchase_data[["SN","Gender"]]

group_sn = pd.DataFrame(cleaned_gender.groupby(['SN']).sum())

group_sn = group_sn.replace({'MaleMale': 'Male', 'MaleMaleMale':'Male', 'FemaleFemale':'Female', 'Other / Non-Disclosed': 'Other', 'FemaleFemaleFemale':'Female', 'Other / Non-DisclosedOther / Non-Disclosed':'Other','MaleMaleMaleMale':'Male','MaleMaleMaleMaleMale':'Male'})

group_sn["Gender"].value_counts()

male = group_sn.loc[group_sn["Gender"] == "Male"]
female = group_sn.loc[group_sn["Gender"] == "Female"]
other = group_sn.loc[group_sn["Gender"] == "Other"]

male_count = len(male)
female_count = len(female)
other_count = len(other)

male_percent = '{0:,.2f}%'.format((male_count/len(group_sn))*100)
female_percent = '{0:,.2f}%'.format((female_count/len(group_sn))*100)
other_percent = '{0:,.2f}%'.format((other_count/len(group_sn))*100)

gender_summary = {'':['Male','Female','Other/Non-Disclosed'],'Total Count':[male_count, female_count, other_count], 'Percentage of Players':[male_percent, female_percent, other_percent]}



gender_summary_df = pd.DataFrame(data=gender_summary)
final_gender_df = gender_summary_df.set_index('')
final_gender_df
#-----------------------------------------------------------------------------------------------

#Purchasing Analysis (Gender)
cleaned_purchase = purchase_data[["Gender", "Price"]]

cleaned_purchase = cleaned_purchase.replace({'MaleMale': 'Male', 'MaleMaleMale':'Male', 'FemaleFemale':'Female', 'Other / Non-Disclosed': 'Other', 'FemaleFemaleFemale':'Female', 'Other / Non-DisclosedOther / Non-Disclosed':'Other','MaleMaleMaleMale':'Male','MaleMaleMaleMaleMale':'Male'})
cleaned_purchase
group_purchase = pd.DataFrame(cleaned_purchase.groupby(['Gender']).mean())

male_purchase = cleaned_purchase.loc[cleaned_purchase["Gender"] == "Male"]
female_purchase = cleaned_purchase.loc[cleaned_purchase["Gender"] == "Female"]
other_purchase = cleaned_purchase.loc[cleaned_purchase["Gender"] == "Other"]


group_purchase["Purchase Count"] = [female_purchase['Price'].count(), male_purchase['Price'].count(), other_purchase['Price'].count()]
group_purchase["Average Purchase Price"] = ['${:,.2f}'.format(female_purchase['Price'].mean()), '${:,.2f}'.format(male_purchase['Price'].mean()), '${:,.2f}'.format(other_purchase['Price'].mean())]
group_purchase["Total Purchase Value"] = ['${:,.2f}'.format(female_purchase['Price'].sum()), '${:,.2f}'.format(male_purchase['Price'].sum()), '${:,.2f}'.format(other_purchase['Price'].sum())]
group_purchase["Avg Total Purchase per Person"] = ['${:,.2f}'.format(female_purchase['Price'].sum()/female_count), '${:,.2f}'.format(male_purchase['Price'].sum()/male_count), '${:,.2f}'.format(other_purchase['Price'].sum()/other_count)]
del group_purchase["Price"]
group_purchase

#-------------------------------------------------------------------------------------------------
#Age Demographics
cleaned_age = purchase_data[["SN","Age", "Price"]]
group_age = pd.DataFrame(cleaned_age.groupby(['SN']).mean())
group_age

bins = [0, 9, 14, 19, 24, 29, 34, 39, 1000]
bin_names = ['<10', '10-14', '15-19', '20-24','25-29','30-34','35-39','40+']

age_bin = group_age.groupby(pd.cut(group_age["Age"], bins, labels=bin_names)).size()

age_df = pd.DataFrame({"Total Count":age_bin})
age_df['Percentage of Players'] = round((age_df["Total Count"]/len(group_sn))*100, 2)

age_df

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------
#I know there is an easier way to figure this part out, I figured it out as I went through the HW so at the end my code is better
#But I have work tomorrow and don't have time to come back and fix this, sorry for the crazy code
#-------------------------------------------------------------------------------------------------------------------------------------

#Purchasing analysis (age)
purchase_data["Age Bin"] = pd.cut(purchase_data["Age"], bins, labels=bin_names) #adds bins

cleaned_purchase_data = purchase_data[["SN","Age Bin"]] #creates easier to read table
group_age_purchase = pd.DataFrame(cleaned_purchase_data.groupby(["SN"]).sum())#creates new DF with groupby



#I did something wrong above so now I have to go in and replace the wrong value
#I learned how to do it correctly at the end of the HW but I don't have time to replace this
group_age_purchase = group_age_purchase.replace({'20-2420-24': '20-24', 
                                             '20-2420-2420-24':'20-24', 
                                             '30-3430-34':'30-34', 
                                             '25-2925-29': '25-29', 
                                             '15-1915-19':'15-19',
                                             '25-2925-2925-29':'25-29', 
                                             '<10<10': '<10',
                                             '35-3935-39':'35-39',
                                             '15-1915-1915-19': "15-19",
                                             '40+40+':'40+',
                                             '<10<10<10':'<10',
                                             '10-1410-14':'10-14',
                                             '20-2420-2420-2420-24':'20-24',
                                             '25-2925-2925-2925-2925-29':'25-29',
                                             '30-3430-3430-34':'30-34',
                                             '10-1410-1410-14':'10-14',
                                             '35-3935-3935-39':'35-39'})

#Again - there is an easier way to this
#I stored in individual variables per bin label the bin data - this helps with total purchase per person 
less10 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "<10"]
bw10and14 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "10-14"]
bw15and19 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "15-19"]
bw20and24 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "20-24"]
bw25and29 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "25-29"]
bw30and34 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "30-34"]
bw35and39 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "35-39"]
over40 = group_age_purchase.loc[group_age_purchase["Age Bin"] == "40+"]
#storing info for each individual bin in a variable, this helps with average purchase price and total purchase price
#I know there is an easier way
less10_purchase = purchase_data.loc[purchase_data["Age Bin"] == "<10"]
bw10and14_purchase = purchase_data.loc[purchase_data["Age Bin"] == "10-14"]
bw15and19_purchase = purchase_data.loc[purchase_data["Age Bin"] == "15-19"]
bw20and24_purchase = purchase_data.loc[purchase_data["Age Bin"] == "20-24"]
bw25and29_purchase = purchase_data.loc[purchase_data["Age Bin"] == "25-29"]
bw30and34_purchase = purchase_data.loc[purchase_data["Age Bin"] == "30-34"]
bw35and39_purchase = purchase_data.loc[purchase_data["Age Bin"] == "35-39"]
over40_purchase = purchase_data.loc[purchase_data["Age Bin"] == "40+"]


age_purchase_group = purchase_data.groupby(pd.cut(purchase_data["Age"], bins, labels=bin_names)).size()
age_purchase_df = pd.DataFrame({"Purchase Count":age_purchase_group})


#add the average purchase price column
age_purchase_df["Average Purchase Price"] = ['${:,.2f}'.format(less10_purchase['Price'].mean()),
                                             '${:,.2f}'.format(bw10and14_purchase['Price'].mean()),
                                             '${:,.2f}'.format(bw15and19_purchase['Price'].mean()),
                                             '${:,.2f}'.format(bw20and24_purchase['Price'].mean()), 
                                             '${:,.2f}'.format(bw25and29_purchase['Price'].mean()), 
                                             '${:,.2f}'.format(bw30and34_purchase['Price'].mean()), 
                                             '${:,.2f}'.format(bw35and39_purchase['Price'].mean()), 
                                             '${:,.2f}'.format(over40_purchase['Price'].mean())]
#add the total purchase value column
age_purchase_df["Total Purchase Value"] = ['${:,.2f}'.format(less10_purchase['Price'].sum()),
                                             '${:,.2f}'.format(bw10and14_purchase['Price'].sum()),
                                             '${:,.2f}'.format(bw15and19_purchase['Price'].sum()),
                                             '${:,.2f}'.format(bw20and24_purchase['Price'].sum()), 
                                             '${:,.2f}'.format(bw25and29_purchase['Price'].sum()), 
                                             '${:,.2f}'.format(bw30and34_purchase['Price'].sum()), 
                                             '${:,.2f}'.format(bw35and39_purchase['Price'].sum()), 
                                             '${:,.2f}'.format(over40_purchase['Price'].sum())]
#add the avg total purchase per person column
age_purchase_df["Avg Total Purchase Per Person"] = ['${:,.2f}'.format(less10_purchase['Price'].sum()/len(less10)),
                                             '${:,.2f}'.format(bw10and14_purchase['Price'].sum()/len(bw10and14)),
                                             '${:,.2f}'.format(bw15and19_purchase['Price'].sum()/len(bw15and19)),
                                             '${:,.2f}'.format(bw20and24_purchase['Price'].sum()/len(bw20and24)), 
                                             '${:,.2f}'.format(bw25and29_purchase['Price'].sum()/len(bw25and29)), 
                                             '${:,.2f}'.format(bw30and34_purchase['Price'].sum()/len(bw30and34)), 
                                             '${:,.2f}'.format(bw35and39_purchase['Price'].sum()/len(bw35and39)), 
                                             '${:,.2f}'.format(over40_purchase['Price'].sum()/len(over40))]

age_purchase_df

#------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
#As you can see in this section, I figured out how to do it using groupby, and adding to a DataFrame
#---------------------------------------------------------------------------------------------------------------------

clean_spender = purchase_data[["SN", "Price"]]#creates easier to read table

clean_spender = purchase_data.groupby("SN")#groups by SN

spender_df = pd.DataFrame(clean_spender["Purchase ID"].count())#creates new DF


spender_df["Average Purchase Price"] = clean_spender["Price"].mean() #adds average price
spender_df["Average Purchase Price"] = spender_df["Average Purchase Price"].map("${:.2f}".format)#formats average price
spender_df["Total Purchase Value"] = clean_spender["Price"].sum()#adds total value

final_spender_df=spender_df.rename(columns={"Purchase ID":"Purchase Count"})#renames column

sorted_spender = final_spender_df.sort_values(by='Total Purchase Value', ascending=False)#sorts
sorted_spender["Total Purchase Value"] = sorted_spender["Total Purchase Value"].map("${0:.2f}".format)#formats
sorted_spender.head()#preview

#--------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
#And lastly, my code got a lot better
#---------------------------------------------------------------------------------------------------------------------

item_df = purchase_data[["Item ID","Item Name","Price"]]#creates easier to read table

grouped_item = item_df.groupby(["Item ID","Item Name"])#grouping by item id and item name

grouped_item_df = pd.DataFrame(grouped_item["Price"].count())#creates new DF with grouped table

final_item_df = grouped_item_df.rename(columns={"Price":"Purchase Count"})#changes column name


final_item_df["Item Price"] = grouped_item["Price"].mean()#adds average price
final_item_df["Item Price"] = final_item_df["Item Price"].map("${:.2f}".format)#adds formatting for average price
final_item_df["Total Purchase Value"] = grouped_item["Price"].sum()#adds total value

sorted_value = final_item_df.sort_values(by='Total Purchase Value', ascending=False) #saves sorting for next task

final_item_df["Total Purchase Value"] = final_item_df["Total Purchase Value"].map("${:.2f}".format) #adds formatting

sorted_count = final_item_df.sort_values(by='Purchase Count', ascending=False)#sorts

sorted_count.head()#preview

#----------------------------------------------------------------------------------------------------------------------
#Most Profitable Items
sorted_value["Total Purchase Value"] = sorted_value["Total Purchase Value"].map("${:.2f}".format) #adds the formatting to the DF column
sorted_value.head()#previews the new sorted DF



