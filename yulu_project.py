# -*- coding: utf-8 -*-
"""yulu_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I4Pwzb3oPo-aUuRWdyK3YREEVgoI2K6M

# Yulu Case study

# About Yulu
Yulu is India’s leading micro-mobility service provider, which offers unique vehicles for the daily commute. Starting off as a mission to eliminate traffic congestion in India, Yulu provides the safest commute solution
through a user-friendly mobile app to enable shared, solo and sustainable commuting.

# Buisness Problem
Yulu seeks to identify the key variables that significantly impact the demand for shared electric cycles in India. Additionally, they aim to assess the effectiveness of these variables in describing the fluctuations in electric cycle demand. By addressing these questions, Yulu aims to gain insights that will inform strategic decisions to enhance their market position and revenue performance.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

!wget https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/428/original/bike_sharing.csv?1642089089

data = pd.read_csv('bike_sharing.csv?1642089089')

data

"""# Column Profiling:
- **datetime**: datetime
- **season**: season (1: spring, 2: summer, 3: fall, 4: winter)
- **holiday**: whether day is a holiday or not
- **workingday**: if day is neither weekend nor holiday is 1, otherwise is 0.
- **weather**:
  - 1: Clear, Few clouds, partly cloudy, partly cloudy
  - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
  - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
  - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
- **temp**: temperature in Celsius
- **atemp**: feeling temperature in Celsius
- **humidity**: humidity
- **windspeed**: wind speed
- **casual**: count of casual users
- **registered**: count of registered users
- **count**: count of total rental bikes including both casual and registered

# Basic Analysis
"""

data.info()

data.head()

data.shape

data.isnull().sum()

data.describe()

"""- There isn't any column with a null value.

# Making changes to the data by introducing new columns with categorization.

## Adding a new column to denote the season corresponding to its index.
"""

data['season_name'] = 'Unknown'
data.loc[data['season'] == 1, 'season_name'] = 'Spring'
data.loc[data['season'] == 2, 'season_name'] = 'Summer'
data.loc[data['season'] == 3, 'season_name'] = 'Fall'
data.loc[data['season'] == 4, 'season_name'] = 'Winter'

data

"""## Adding a new column to indicate whether the day is classified as a working day or a holiday."""

data['day'] = 'Holiday'
data.loc[data['workingday'] == 1, 'day'] = 'Working Day'

data

"""## Dropping unnecessary tables."""

data.drop('season',axis = 1, inplace = True)
data.drop('workingday',axis = 1, inplace = True)
data.drop('holiday',axis = 1,inplace = True)
# data.drop('Working_day',axis = 1,inplace = True)

data

"""# Univariate Analysis

## Analyzing the distribution of numerical variables.

### temp
"""

sns.boxplot(data['temp'],orient='h')

"""There are no outliers detected in the temperature column."""

sns.kdeplot(data = data,x = 'temp')

"""### atemp"""

sns.boxplot(data['atemp'],orient='h')

"""There are no outliers detected in the atemp column."""

sns.kdeplot(data = data, x = 'atemp')

"""### humidity"""

sns.boxplot(data['humidity'],orient='h')

"""There is only **one** outlier observed in the humidity column."""

sns.kdeplot(data = data, x = 'humidity')

"""### windspeed"""

sns.boxplot(data['windspeed'],orient='h')

q1,q3 = np.quantile(data['windspeed'],0.25),np.quantile(data['windspeed'],0.75)
IQR = q3 - q1
w1,w2 = q1 - (1.5 * IQR),q3 + (1.5 * IQR)
outliers = data[(data['windspeed'] < w1) | (data['windspeed'] > w2)]
len(outliers)

"""There are  **227** outlier observed in the windspeed column."""

sns.kdeplot(data = data, x = 'windspeed')

"""### registered"""

sns.boxplot(data['registered'],orient='h')

q1,q3 = np.quantile(data['registered'],0.25),np.quantile(data['registered'],0.75)
IQR = q3 - q1
w1,w2 = q1 - (1.5 * IQR),q3 + (1.5 * IQR)
outliers = data[(data['registered'] < w1) | (data['registered'] > w2)]
len(outliers)

"""There are  **423** outlier observed in the registered column."""

sns.kdeplot(data = data, x = 'registered')

"""### count"""

sns.boxplot(data['count'],orient='h')

q1,q3 = np.quantile(data['count'],0.25),np.quantile(data['count'],0.75)
IQR = q3 - q1
w1,w2 = q1 - (1.5 * IQR),q3 + (1.5 * IQR)
outliers = data[(data['count'] < w1) | (data['count'] > w2)]
len(outliers)

"""There are  **300** outlier observed in the count column."""

sns.kdeplot(data = data, x = 'count')

"""## Analyzing the distribution of categorical variables.

### season
"""

data['season_name'].value_counts()

seasons = data['season_name'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(seasons , labels = seasons.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Seasoms') #title
plt.show()

sns.countplot(data = data, x = 'season_name')

"""### weather"""

weather = data['weather'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(weather, labels=weather.index.map(str), autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Weather Categories') #title
plt.show()

sns.countplot(data = data, x = 'weather')

"""### day"""

day = data['day'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(day, labels=day.index.map(str), autopct='%1.1f%%', startangle=90)
plt.title('Distribution of type of day') #title
plt.show()

sns.countplot(data = data, x = 'day')

"""# Bivariate Analysis

## type of day
"""

palette = 'Set2'
sns.boxplot(x='day', y='count', data=data, palette=palette)
plt.xlabel('type of day')
plt.ylabel('count')
plt.title('Box Plot of Count by type of day Day')
plt.show()

"""Observations:

- Typically, there are more electric cycles rented on weekdays than on holidays.
- The higher occurrence of outliers in the rental count distribution on weekdays implies a greater variability or presence of extreme values in rentals during these days.
- The elevated median on weekdays indicates a higher demand or usage of shared electric cycles during weekdays, possibly due to commuting needs and routine travel.
- Holidays may display more consistent or predictable rental patterns, with fewer extreme deviations from the average.
- Utilizing a 2-sample t-test can help determine the impact of working days on the number of bikes rented.
"""

palette = 'Set2'
sns.barplot(x='day', y='count', data=data, palette=palette)
plt.xlabel('type of Day')
plt.ylabel('count')
plt.title('Box Plot of Count by type of day')
plt.show()

"""## season"""

palette = 'Set2'
sns.boxplot(x='season_name', y = 'count', data=data, palette=palette)
plt.xlabel('Season')
plt.ylabel('count')
plt.title('Box Plot of Count by Season')
plt.show()

"""Observations:

- The median count for Spring is the highest among all seasons.
- This implies that, on average, the demand for shared electric cycles is highest during the Fall season, followed by Winter, Summer, and then Spring.
- The ascending order of outliers also follows the sequence of Spring having the most outliers, followed by Winter, Summer, and Fall.
- Spring exhibits more extreme variations or unusually high/low rental counts compared to other seasons.
- The observed seasonal order of medians and outliers indicates distinct patterns in demand for shared electric cycles throughout the year.
- Fall appears to be a peak season for rentals, likely influenced by pleasant weather and outdoor activities.
- Winter and Summer follow with moderate demand, possibly influenced by weather conditions and seasonal factors.
- Spring shows the lowest demand, which could be attributed to transitional weather or other seasonal factors.
"""

palette = 'Set2'
sns.barplot(x='season_name', y='count', data=data, palette=palette)
plt.xlabel('Season name')
plt.ylabel('count')
plt.title('Box Plot of Count by Season Name')
plt.show()

"""Observations

- Fall shows the highest peak in rental counts.
- This suggests the presence of unique seasonal factors driving increased demand during this period.
- Potential factors may include specific events, holidays, or weather conditions characteristic of the Fall season.

## weather
"""

palette = 'Set2'
sns.boxplot(x='weather', y = 'count', data=data, palette=palette)
plt.xlabel('Weather')
plt.ylabel('count')
plt.title('Box Plot of Count by Weather')
plt.show()

"""Observations

- Median counts across different weather types follow a distinct pattern, with Type 1 having the highest median count, followed by Type 2 and then Type 3.
- This suggests that weather Type 1 conditions are associated with the highest demand for shared electric cycles, followed by Type 2 and Type 3.
- Weather Type 1 likely represents favorable or optimal conditions that encourage increased usage of micro-mobility services.
- Type 2 and Type 3 conditions may still attract moderate usage but to a lesser extent compared to Type 1.
- A median count of 0 for Weather Type 4 indicates that this weather condition is not conducive to rental activity or usage of shared electric cycles.
- Weather Type 4 represents extreme or unfavorable conditions like heavy rain, ice pellets, and thunderstorms, which deter users from utilizing micro-mobility services entirely.
"""

palette = 'Set2'
sns.barplot(x='weather', y = 'count', data=data, palette=palette)
plt.xlabel('Weather')
plt.ylabel('count')
plt.title('Box Plot of Count by Weather')
plt.show()

"""# Hypothesis Testing

## **2- Sample T-Test** to check if Working Day has an effect on the number of electric cycles rented
"""

sns.kdeplot(data = data, x="count", hue="day")
plt.show()

"""**Null Hypothesis** (H0): Working day has no effect on the number of cycles being rented.

**Alternate Hypothesis** (H1): Working day has effect on the number of cycles being rented.

**Significance level** (alpha): 0.05

We will use the 2-Sample T-Test to test the hypothess defined above

Assumptions:
- Random Sampling: We selected 30 random samples from the population data.
- Independence: The data points are independent of each other.
- Normality: Since we are testing means and our sample size is 30, according to the Central Limit Theorem (CLT), we can infer that the sample means of the data are normally distributed.
- Equal Variances: We will presume that the variances are approximately equal.
"""

s1 = np.random.choice(data[data['day'] == 'Working Day']['count'].values, 30)
s2 = np.random.choice(data[data['day'] == 'Holiday']['count'].values, 30)

t_stat, pval = ttest_ind(s1, s2, alternative="two-sided")
print("T-statistic:", t_stat)
print("P-value:", pval)

alpha = 0.05
if pval >= alpha:
    print("Fail to reject null hypothesis. Working Day does not have an effect on the number of electric cycles rented.")
else:
    print("Reject null hypothesis. Working Day has an effect on the number of electric cycles rented.")

"""### **Conclusion:**

Based on the test results, it appears that the day's status (working day or not) does not exert a statistically significant influence on the number of electric cycles rented.

## **ANNOVA** to check if No. of cycles rented is similar or different in different 1. weather 2. season

### 1. weather
"""

sns.kdeplot(data = data, x="count", hue="weather")
plt.show()

"""Based on the graph above, it is evident that the data does not follow a normal distribution and instead resembles an F distribution.

**Null Hypothesis** (H0): The number of cycles rented is consistent across different weather conditions.

**Alternative Hypothesis** (H1): The number of cycles rented varies across different weather conditions.
"""

data_1 = data[data['weather'] == 1]['count'].values
data_2 = data[data['weather'] == 2]['count'].values
data_3 = data[data['weather'] == 3]['count'].values
data_4 = data[data['weather'] == 4]['count'].values

"""Assumptions:

- Independence: The data points are independent of each other.
- Normality: We can assess the normality of the data using QQ-Plots or the Shapiro-Wilk Test, with a significance level of 0.05.
- Equal Variances: We will presume that the variances are approximately equal.
"""

fig, axs = plt.subplots(1, 4, figsize=(15, 3))
for i, data in enumerate([data_1, data_2, data_3, data_4]):
    qqplot(data, ax=axs[i])
    axs[i].set_title(f"QQ Plot for data_{i+1}")

plt.tight_layout()
plt.show()

"""The graphs provide additional evidence suggesting that the data is not normally distributed. We will confirm this by conducting the Shapiro-Wilk Test."""

# Define a dictionary to store the data and weather types
weather_data = {
    "Weather 1": data_1,
    "Weather 2": data_2,
    "Weather 3": data_3
}

# Perform Shapiro-Wilk test for each weather type
for weather, data in weather_data.items():
    stat, p_value = shapiro(data)
    print(f"Shapiro-Wilk Test for {weather}:")
    print("Test Statistic:", stat)
    print("p-value:", p_value)
    print("Data is normally distributed" if p_value > 0.05 else "Data is not normally distributed")
    print()

# Not performing for Weather 4 as it only contains 1 data point

"""This verifies that the data does not follow a normal distribution."""

def conduct_anova(data_list, significance_level=0.05):
    """
    Perform ANOVA test and display results.

    Parameters:
    - data_list (list of array-like): List of datasets to compare.
    - significance_level (float): Desired significance level (default is 0.05).
    """
    f_statistic, p_value = f_oneway(*data_list)

    print("ANOVA Results:")
    print("F-Statistic:", f_statistic)
    print("P-value:", p_value)

    if p_value < significance_level:
        print("\nReject the null hypothesis.")
        print("The number of cycles rented differs across different weather types.")
    else:
        print("\nFail to reject the null hypothesis.")
        print("The number of cycles rented is similar across different weather types.")

# Invoking the function with the data list
conduct_anova([data_1, data_2, data_3, data_4])

"""Conclusion

Weather significantly influences the number of cycles rented, as evidenced by the fact that the number of cycles rented varies across different weather conditions.

### season
"""

data = pd.read_csv("https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/428/original/bike_sharing.csv?1642089089")
sns.kdeplot(data = data, x="count", hue="season")
plt.show()

"""The data appears to deviate from a normal distribution.

**Null Hypothesis** (H0): The number of cycles rented is consistent across different seasons.

**Alternative Hypothesis** (H1): The number of cycles rented varies across different seasons.
"""

data_1 = data[data['season'] == 1]['count'].values
data_2 = data[data['season'] == 2]['count'].values
data_3 = data[data['season'] == 3]['count'].values
data_4 = data[data['season'] == 4]['count'].values

"""Assumptions:

- Independence: The data points are independent of each other.
- Normality: We can assess the normality of the data using QQ-Plots or the Shapiro-Wilk Test, with a significance level of 0.05.
- Equal Variances: We will assume that the variances of the data are equal.
"""

# test for normality

fig, axs = plt.subplots(1, 4, figsize=(16, 4))

qqplot(data_1, line='s', ax=axs[0])
axs[0].set_title('QQ Plot for data_1')

qqplot(data_2, line='s', ax=axs[1])
axs[1].set_title('QQ Plot for data_2')

qqplot(data_3, line='s', ax=axs[2])
axs[2].set_title('QQ Plot for data_3')

qqplot(data_4, line='s', ax=axs[3])
axs[3].set_title('QQ Plot for data_4')

plt.tight_layout()
plt.show()

"""The graphs provide additional indication that the data may not follow a normal distribution. To confirm this, we will conduct a Shapiro-Wilk Test."""

data_list = [data_1, data_2, data_3, data_4]
seasons = ["Season 1", "Season 2", "Season 3", "Season 4"]

for season, data in zip(seasons, data_list):
    statistic, p_value = shapiro(data)
    print(f"Shapiro-Wilk Test for {season}:")
    print("Test Statistic:", statistic)
    print("p-value:", p_value)
    print("Data is normally distributed" if p_value > 0.05 else "Data is not normally distributed")
    print()

"""The results of the Shapiro-Wilk test indicate that the data does not follow a normal distribution."""

# ANNOVA

def perform_anova(*args, significance_level=0.05):
    f_statistic, p_value = f_oneway(*args)
    print("F-Statistic:", f_statistic)
    print("P-value:", p_value)

    if p_value < significance_level:
        print("\nReject the null hypothesis.")
        print("Number of cycles rented differs across different seasons.")
    else:
        print("\nFail to reject the null hypothesis.")
        print("Number of cycles rented is similar across different seasons.")

# Invoking the function with the data
perform_anova(data_1, data_2, data_3, data_4)

"""Conclusion

The season does influence the number of cycles being rented.

## **Chi-square test** to check if Weather is dependent on the season
"""

data = pd.read_csv("https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/428/original/bike_sharing.csv?1642089089")
sns.kdeplot(data = data, x="weather", hue="season")
plt.show()

sns.countplot(data = data, x="weather", hue="season")
plt.show()

data_table = pd.crosstab(data['season'], data['weather'])
data_table

"""**Null Hypothesis** (H0): There is no relationship between weather and season.

**Alternate Hypothesis** (H1): There is a relationship between weather and season.

**Significance level** (alpha): 0.05

We will employ the chi-square test to evaluate the aforementioned hypotheses.

Assumptions:

- Random Sampling: Not required since we have data for the entire population.
- Independence: The data points are independent of each other.
- Sufficient Sample Size: The sample size is not large enough for weather type 4.
"""

def perform_chi_square_test(data, variable1, variable2, alpha=0.05):
    contingency_table = pd.crosstab(data[variable1], data[variable2])

    chi2_stat, p_val, dof, expected_values = chi2_contingency(contingency_table)

    if p_val <= alpha:
        print(f"\nSince the p-value is less than or equal to the significance level of {alpha},")
        print(f"We reject the Null Hypothesis. This suggests that {variable2} is dependent on {variable1}.")
    else:
        print(f"\nSince the p-value is greater than the significance level of {alpha},")
        print("We fail to reject the Null Hypothesis.")

# Invoking the function with the provided data and variables
perform_chi_square_test(data, 'season', 'weather')

"""### Conclusion
weather is dependent on season.

# Insights:
- During the summer and fall seasons, more bikes are rented compared to other seasons.
- Bike rentals increase on holidays.
- More bikes are rented on holidays and weekends compared to working days.
- Rentals decrease during rainy, thunderstorm, snowy, or foggy weather.
- Very few bikes are rented when humidity is less than 20.
- Rentals decrease when the temperature is less than 10.
- Rentals decrease when the windspeed is greater than 35.

# Recommendations:

1. Increase bike inventory during summer and fall seasons to meet the higher demand compared to other seasons.
2. Based on a significance level of 0.05, working days do not significantly affect bike rentals.
3. Decrease bike inventory on days with very low humidity.
4. Reduce bike inventory during very cold days or when the temperature is less than 10 degrees Celsius.
5. Decrease bike inventory during thunderstorms or when the windspeed exceeds 35 km/h.

# Note to evaluator
- colab link : https://colab.research.google.com/drive/1I4Pwzb3oPo-aUuRWdyK3YREEVgoI2K6M?usp=sharing
- Student Name = Sai Venkatesh
- Converted to pdf using https://2pdf.com/convert-ipynb-to-pdf/
"""

