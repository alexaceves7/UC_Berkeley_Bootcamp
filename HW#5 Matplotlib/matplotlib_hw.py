 %matplotlib notebook
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# File to Load (Remember to change these)
city_data_to_load = "data/city_data.csv"
ride_data_to_load = "data/ride_data.csv"

# Read the City and Ride Data
city_data = pd.read_csv(city_data_to_load)
ride_data = pd.read_csv(ride_data_to_load)
# Combine the data into a single dataset
all_data = pd.merge(ride_data, city_data, on="city", how="left")
# Display the data table for preview
all_data.head()

#--------------------------------------------------------------------------------------
#Bubble Plot of Ride Sharing Data
#--------------------------------------------------------------------------------------

# Obtain the x and y coordinates for each of the three city types

urban_data = []
sub_data =[]
rural_data = []
urban_final = pd.DataFrame()
sub_final = pd.DataFrame()
rural_final = pd.DataFrame()

#separates the area types
urban_data = all_data.loc[all_data['type'] == "Urban"]
sub_data = all_data.loc[all_data['type'] == "Suburban"]
rural_data = all_data.loc[all_data['type'] == "Rural"]

#creates a cleaner dataframe
urban_cleaned=urban_data[["city", "fare", "driver_count", "ride_id"]]
sub_cleaned=sub_data[["city", "fare", "driver_count", "ride_id"]]
rural_cleaned=rural_data[["city", "fare", "driver_count", "ride_id"]]

#creates final urban DF with values needed for scatter plot
urban_final['average fare'] = urban_cleaned.groupby("city")["fare"].mean()
urban_final['total driver'] = urban_cleaned.groupby("city")["driver_count"].sum()
urban_final['total rides'] = urban_cleaned.groupby("city")["ride_id"].count()

x_urban = urban_final["total rides"]
s_urban = urban_final["total driver"]
y_urban = urban_final["average fare"]

#creates final suburban DF with values needed for scatter plot
sub_final['average fare'] = sub_cleaned.groupby("city")["fare"].mean()
sub_final['total driver'] = sub_cleaned.groupby("city")["driver_count"].sum()
sub_final['total rides'] = sub_cleaned.groupby("city")["ride_id"].count()

x_sub = sub_final["total rides"]
s_sub = sub_final["total driver"]
y_sub = sub_final["average fare"]

#creates final rural DF with values needed for scatter plot
rural_final['average fare'] = rural_cleaned.groupby("city")["fare"].mean()
rural_final['total driver'] = rural_cleaned.groupby("city")["driver_count"].sum()
rural_final['total rides'] = rural_cleaned.groupby("city")["ride_id"].count()

x_rural = rural_final["total rides"]
s_rural = rural_final["total driver"]
y_rural = rural_final["average fare"]

# Build the scatter plots for each city types
plt.scatter(x = x_urban, y = y_urban, marker='o', facecolors ="lightcoral", edgecolors="black", s=s_urban*.4, alpha=.90, label="Urban")
plt.scatter(x = x_sub, y = y_sub, marker='o', facecolors ="lightskyblue", edgecolors="black", s=s_sub*.4, alpha=.90, label="Suburban")
plt.scatter(x = x_rural, y= y_rural, marker='o', facecolors ="gold", edgecolors="black", s=s_rural*.4, alpha=.90, label= "Rural")

# Incorporate the other graph properties
plt.grid()
plt.title("Pyber Ride Sharing data (2016)")
plt.xlabel("Total Number of Rides (Per City)")
plt.ylabel("Average Fare ($)")
#legend and circle size
legend = plt.legend(loc = "upper right")
legend.legendHandles[0]._sizes = [30]
legend.legendHandles[1]._sizes = [30]
legend.legendHandles[2]._sizes = [30]
#outside text
text_out1 = "Note:"
text_out2 =  "Circle size correlates with driver count per city"
plt.text(41, 30,text_out1)# bbox_inches="tight")
plt.text(41, 28,text_out2)# bbox_inches="tight")



# Save Figure
plt.savefig("./pyber_ride_sharing_data.png", bbox_inches="tight")

# Show plot

plt.show("./pyber_ride_sharing_data.png")

#-----------------------------------------------------------------------
#total fares by city type
#-----------------------------------------------------------------------

# sets up values needed for pie chart
labels = ["Rural", "Suburban", "Urban"]
fare_sizes = []
colors = ["gold","lightskyblue","lightcoral",]
explode = (0, 0, .1)

#total per city type
total_fare_urban = urban_cleaned['fare'].sum()
total_fare_sub = sub_cleaned['fare'].sum()
total_fare_rural = rural_cleaned['fare'].sum()

total_fare = all_data["fare"].sum()

#appends sizes
fare_sizes.append(total_fare_rural/total_fare)
fare_sizes.append(total_fare_sub/total_fare)
fare_sizes.append(total_fare_urban/total_fare)


# Build Pie Chart

plt.pie(fare_sizes, explode = explode, labels = labels, colors = colors, autopct ="%1.1f%%", shadow = True, startangle = 140)
plt.title("% of Total Fares by City Type")
# Save Figure
plt.savefig("./percent_total_fares_by_city_pie.png")

# Show Figure
plt.show("./percent_total_fares_by_city_pie.png")


#------------------------------------------------------------------------------------------
#total rides by city type
#------------------------------------------------------------------------------------------

# Calculate Ride Percents

ride_sizes = []


ride_sizes.append(len(rural_data)/len(all_data))
ride_sizes.append(len(sub_data)/len(all_data))
ride_sizes.append(len(urban_data)/len(all_data))


# Build Pie Chart
plt.pie(ride_sizes, explode = explode, labels = labels, colors = colors, autopct ="%1.1f%%", shadow = True, startangle = 140)
plt.title("% of Total Rides by City Type")
# Save Figure
plt.savefig("./percent_total_rides_by_city_pie.png")

# Show Figure
plt.show("./percent_total_rides_by_city_pie.png")

#--------------------------------------------------------------------------------------------------
#total drivers by city type
#--------------------------------------------------------------------------------------------------

# Calculate Driver Percents

drive_sizes = [city_data.groupby(["type"]).sum()["driver_count"] / city_data["driver_count"].sum()]



# Build Pie Charts
plt.pie(drive_sizes[0], explode = explode, labels = labels, colors = colors, autopct ="%1.1f%%", shadow = True, startangle = 170)
plt.title("% of Total Drivers by City Type")
# Save Figure
plt.savefig("./percent_total_drivers_by_city_pie.png")

# Show Figure
plt.show("./percent_total_drivers_by_city_pie.png")