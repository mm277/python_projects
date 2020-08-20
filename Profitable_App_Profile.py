#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profile Recommendations for the App Store and Google Play Markets 
# 
# - The project focuses on deriving actionable insights for a company that builds Android and iOS mobile apps for Google Play and the App Store.
# - The company build apps that are free to download and install and its main source of revenue comes from in-app ads. 
# - The company's revenue for any given app is mostly influenced by the number of users who use their app and engage with the ads.
# - The goal of this project is to recommend profitable app profiles to the developers by analyzing data about mobile apps available on Google Play and the App Store.
# - As of September 2018, there were approximately 2 million iOS apps available on the App Store, and 2.1 million Android apps on Google Play. Collecting data for over 4 million apps requires a significant amount of time and money, so I will try to analyze below mentioned sample datasets first to find relevant insights:
# 
#  - Android Apps Dataset  ([link](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv)) containing data about approximately 10,000 Android apps from Google Play collected in August 2018.
#  
#  - iOS Apps Dataset ([link](https://dq-content.s3.amazonaws.com/350/AppleStore.csv)) containing data about approximately 7,000 iOS apps from the App Store collected in July 2017.

# # 1. Data Exploration
# 
# Firstly, I will open and explore the android and iOS apps datasets to find out useful columns for my analysis.

# In[2]:


from csv import reader
#App Store Data
app_store_open = open('AppleStore.csv')
app_store_read = reader(app_store_open)
ios_apps = list(app_store_read)


#Google Play Data
google_play_open = open('googleplaystore.csv')
google_play_read = reader(google_play_open)
android_apps = list(google_play_read)

#function to explore the data in datasets
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

#Explore iOS data using above function
explore_data(ios_apps,0,4,True)


# In[3]:


#Explore android data using above function
explore_data(android_apps,0,4,True)


# - The columns that are important for my analysis in android dataset are are App, Price, Rating, Installs, Genres, and Category.
# - The columns that are important for my analysis in iOS dataset are track_name, price, user_rating, rating_count_tot and prime_genre.

# # 2. Data Cleaning
# 
# ### Step 1 
# Before beginning my analysis, I need to make sure the data I analyze is accurate, otherwise the results of the analysis will be wrong. I will start with the below steps:
# 
# - Detect inaccurate data, and correct or remove it.
# - Detect duplicate data, and remove the duplicates.
# 

# In[4]:


#checking duplicates
duplicates = []
unique = []
for v in android_apps:
    x = v[0]
    if x in unique:
        duplicates.append(x)
    else:
        unique.append(x)
print('Number of duplicate android apps is', len(duplicates))
#Let's see sample duplicates
print(duplicates[:11])
#Since one of the duplicate is 'ZOOM Cloud Meetings', let's go ahead and check 'Quick PDF Scanner' in main 
#dataset to deduce a criteria for removal
for z in android_apps:
    m = z[0]
    if m == 'Slack':
        print(z)
# as we can see the duplicate values differ on 4th column 'Number of Reviews'
#The critieria that can be used for removing duplicates is the number of reviews. 


# In[5]:


duplicates = []
unique = []
for v in ios_apps:
    x = v[0]
    if x in unique:
        duplicates.append(x)
    else:
        unique.append(x)
print('Number of duplicate ios apps is', len(duplicates))


# - Number of duplicate android apps is 1181.
# - Number of duplicate ios apps is 0.
# - The duplicates in android app have duplicate values differ on 4th column 'Number of Reviews'
# - The critieria that can be used for removing duplicates is the number of reviews. 
# - I will keep the unique values with the highest number of reviews since they are the latest entries in the dataset for particular apps and drop the other duplicate values

# In[6]:


#To remove duplicates I will create dictionary having app name as key and highest number of reviews as value
and_dict = {}
for g in android_apps[1:]:
    name = g[0]
    value = g[3]
    if name in and_dict and and_dict[name] < value:
        and_dict[name] = value
    elif name not in and_dict:
        and_dict[name] = value
print('Expected length of dataset after removing duplicates', len(android_apps[1:]) - 1181)
print('Actual number of unique values in datatset', len(and_dict)) 


# In[7]:


#I will remove the duplicates from my datatset using and_dict dictionary
cleaned_android_apps = []
already_added = []

for row in android_apps[1:]:
    app = row[0]
    review_num = row[3]
    if (app not in already_added) and (and_dict[app] == review_num):
        cleaned_android_apps.append(row)
        already_added.append(app)
explore_data(cleaned_android_apps,0,3,True)


# ### Step 2 
# Since the company only build apps that are free to download and install, and that is directed toward an English-speaking audience, I'll need to:
# 
# - Remove non-English apps.
# - Remove apps that aren't free.

# In[8]:


#To remove non-English Apps I need to compare the characters in the app names with 127 sinceas per the ASCII system English characters have values between 0 to 127.
#I will first create a function to compare the value of character is <= 127.
def eng_char(string):
    for c in string:
        if ord(c) > 127:
            return False
    return True
eng_char('爱奇艺PPS -《欢乐颂2》电视剧热播') 
eng_char('Instachat 😜')


# In[9]:


#I will filter the data to remove non english apps using above function
filtered_android_apps=[]
filtered_ios_apps=[]
for row in cleaned_android_apps:
    app = row[0]
    if eng_char(app):
        filtered_android_apps.append(row)
for row in ios_apps:
    app = row[1]
    if eng_char(app):
        filtered_ios_apps.append(row)
explore_data(cleaned_android_apps,0,1,True)
explore_data(filtered_android_apps,0,1,True)
explore_data(ios_apps,0,1,True)
explore_data(filtered_ios_apps,0,1,True)


# #### Result of cleaning non- English apps
# 
# - In the android app dataset we have 9118 records left out of 9660 after removing duplicates and non-English Apps.
# - In the ios app dataset we have 5708 records left out of 7198 after removing non-English Apps.

# In[10]:


#Now I will remove apps that are not free from my datasets
#The column for price in android dataset is 6 and for ios it is 4
android_apps_data = []
ios_apps_data = []
for row in filtered_android_apps:
    price = row[7]
    if price == '0':
        android_apps_data.append(row)
for m in filtered_ios_apps:
    p = m[4]
    if p == '0.0':
        ios_apps_data.append(m)


# In[11]:


explore_data(android_apps_data,0,1,True)
explore_data(ios_apps_data,0,6,True)


# ### Result of Cleaning
# - After removing non-free apps we are left with 8406 records in android dataset and 2922 in iOS dataset

# # 3. Data Analysis
# 
# The goal is to add the recommended apps on both Google play and App Store, I will explore apps that are profitable on both the markets. 

# ###  Step 1. Analysis Based on Genre
# I'll analyse prime_genre column of the App Store data set, and for the Genres and Category columns of the Google Play data set to derive insights on most common apps in these datasets.
# 
# I'll build two functions we can use to analyze the frequency tables:
# 
# - One function to generate frequency tables that show percentages
# - Another function we can use to display the percentages in a descending order

# In[12]:


#function to generate frequency table that show percentages
def freq_table(dataset, idx):
    freq_table_dict = {}
    percent_freq_table= {}
    sum = 0

    for row in dataset:
        sum += 1
        key = row[idx]
        if key not in freq_table_dict:
            freq_table_dict[key] = 1
        else:
                freq_table_dict[key] += 1
    for key in freq_table_dict:
        percent_freq_table[key] = (freq_table_dict[key]/sum)*100
    return percent_freq_table


# In[13]:


#funtion to display the percentages in a descending order
def display_table_order(dataset,idx):
    percent_freq_table = freq_table(dataset, idx)
    tab = []
    sorted_freq_table = []
    for key in percent_freq_table:
        val = (percent_freq_table[key],key)
        tab.append(val)
    sorted_freq_table = sorted(tab, reverse = True)
    for entry in sorted_freq_table:
        print(entry[1], ':', entry[0])


# In[14]:


#fequency table for prime_genre column in iOS dataset
display_table_order(ios_apps_data, 11)


# In[15]:


#fequency table for genres column in android dataset
display_table_order(android_apps_data, 9)


# In[16]:


#fequency table for category column in iOS dataset
display_table_order(android_apps_data, 1)


# ### App profile recommendation based on Genre and Category Analysis
# 
# - Apple Store: Almost 60% of free English apps on Apple Store belongs to Games genre. The other popluar genres include Entertainment, Photo & Video, Education and Social Networking. Looking at the stats the general impression is that most of the apps are designed for fun activities including games, photo and video, social networking, entertainment on Apple Store. Thus, these app profiles can be suggested based on the analysis of frequency table. 
# 
# - Google Play: The most commen genres on Google play are Tools , Entertainment, Education, Business, Productivity and Lifestyle. Since the Genres column has mixed genres as well, it makes it more confusing to come to a conclusion. The Category frequency table provides a more clear piture with precise categories, family category is the most common that accounts for 18.8% of apps and then the game category is the 2nd most common with almost 10% of free English apps.
# 
# - The app profiles that would work for both the market would be games.
# 
# - Since the frequency of certain app profiles does not guarantee that they are liked by users as well, I would futher analyse the app profiles based on installations and user ratings.
# 

# ###  Step 2. Analysis Based on Average App Installations for each Genre
# 
# I will analyse the average number of app installations per genre to dive deep into the analysis and figure out the most popular genres.
# 
# - For the iOS dataset, I will use prime_genre, sum of rating_count_tot and total number of apps in a particular genre to find the average number of installed apps per genre. 
# - For the Android dataset, I will use category, sum of installs column and total number of apps per genre to find average number of installations.

# In[17]:


#Average installations/genre for Apple Store apps
ios_data = freq_table(ios_apps_data, 11)
avg_installs = {}
for genre in ios_data:
    total_installs = 0
    len_apps = 0
    for row in ios_apps_data:
        app_genre = row[11]
        if app_genre == genre:
            installs = float(row[5])
            total_installs += installs
            len_apps += 1
    avg = total_installs/len_apps
    avg_installs[genre]=avg

#sorting the dictionary
def display_table_order_a():
    tab = []
    sorted_freq_table = []
    for key in avg_installs:
        val = (avg_installs[key],key)
        tab.append(val)
    sorted_freq_table = sorted(tab, reverse = True)
    for entry in sorted_freq_table:
        print(entry[1], ':', entry[0])
display_table_order_a()


# The most popular genres are Navigation, Reference, Social Networking, Music and Weather.
# I will further analyse the popular apps for this genres to get a clear picture if new apps are leading the giant apps in the market.

# In[18]:


#Navigation Apps
for r in ios_apps_data:
    genre = r[11]
    if genre == 'Navigation':
        print(r[1],' has ',r[5],'user ratings')


# In[19]:


# Reference Apps
for r in ios_apps_data:
    genre = r[11]
    if genre == 'Reference':
        print(r[1],' has ',r[5],'user ratings')


# In[64]:


# Social Networking Apps
for r in ios_apps_data:
    genre = r[11]
    if genre == 'Games':
        print(r[1],' has ',r[5],'user ratings')


# The apps that are most common on App store belongs to games, social networking genre while the most popular apps belongs to other genres including navigation and references.The app profile navigation and social networking can be highly competitive due to presence of giants ike Facebook, Google Maps. I can recommend References profile for new apps.

# In[21]:


##Average installations/genre for Apple Store apps
cat_freq = freq_table(android_apps_data, 1)
avg_installs = {}
for r in cat_freq:
    total = 0
    len_cat = 0
    for v in android_apps_data:
        category_app = v[1]
        if category_app == r:
            len_cat += 1
            ed_installs = v[5].replace('+','')
            ed_installs = ed_installs.replace(',','')
            ed_installs = float(ed_installs)
            total += ed_installs
    avg = total/len_cat
    avg_installs[r]=avg

#sorting the dictionary
def display_table_order_b():
    tab = []
    sorted_freq_table = []
    for key in avg_installs:
        val = (avg_installs[key],key)
        tab.append(val)
    sorted_freq_table = sorted(tab, reverse = True)
    for entry in sorted_freq_table:
        print(entry[1], ':', entry[0])
display_table_order_b()


# In[22]:


for v in android_apps_data:
    r = v[1]
    if r == 'BOOKS_AND_REFERENCE' and v[5] == '10,000,000+':
        print(v[0],v[5])


# ### App profile recommendation based on Average App Installations for each Genre
# 
# Communication is the most famous genre on Google Play. Comparing to the iOS analysis, Books and Refrences is also a famous genre with 8504745.97826087 installations. This genre is famous in both the markets. I woul recommend this app profile for new apps since they have a potential with less competition from Giant Companies.

# ###  Step 3. Analysis Based on Average User Ratings for each Genre
# 
# I will further drill down my analysis to find out most popular genres based on average user ratings. Since the company generates revenue from in-app ads, it is highly likely that the highest rated genre apps would prove to be a good investement.
# 
# - For the iOS dataset, I will use sum of user_rating and total number of apps in a particular genre to find the average of ratings for each genre. 
# - For the Android dataset, I will use sum of rating column and total number of apps per category to find average of ratings for each genre. 
# 

# In[29]:


#Average ratings/genre for Apple Store apps
ios_data = freq_table(ios_apps_data, 11)
avg_ratings = {}
for genre in ios_data:
    total_ratings = 0
    len_apps = 0
    for row in ios_apps_data:
        app_genre = row[11]
        if app_genre == genre:
            rating = float(row[8])
            total_ratings += rating
            len_apps += 1
    avg = total_ratings/len_apps
    avg_ratings[genre]=avg

#sorting the dictionary
def display_table_order_c():
    tab = []
    sorted_freq_table = []
    for key in avg_ratings:
        val = (avg_ratings[key],key)
        tab.append(val)
    sorted_freq_table = sorted(tab, reverse = True)
    for entry in sorted_freq_table:
        print(entry[1], ':', entry[0])
display_table_order_c()


# As I can see Reference is the most popular genre followed by productivity and games. I will further check if the ratings are skewed by larger giant app ratings or there is scope for lesser known apps to be popular.

# In[31]:


for r in ios_apps_data:
    genre = r[11]
    if genre == 'Reference':
        print(r[1],' has ',r[8],'user ratings')


# In[39]:


for r in ios_apps_data:
    genre = r[11]
    if genre == 'Productivity':
        print(r[1],' has ',r[8],'user ratings')


# In[40]:


for r in ios_apps_data:
    genre = r[11]
    if genre == 'Games':
        print(r[1],' has ',r[8],'user ratings')


# I can see that there is good scope for new apps in Reference genre and games genre since the competition with big giants is less and user ratings are pretty good.

# In[62]:


for v in android_apps_data:
    r = v[1]
    if r == 'BOOKS_AND_REFERENCE':
        print(v[0],v[2])


# I can see there are many NaN values in the rating column, I will replace them with 0 to get clear results

# In[63]:


#Average ratings/category for Google Play apps
cat_freq = freq_table(android_apps_data, 1)
avg_installs = {}
for r in cat_freq:
    total = 0
    len_cat = 0
    for v in android_apps_data:
        category_app = v[1]
        if category_app == r:
            len_cat += 1
            ed_installs = v[2].replace('NaN','0')
            ed_installs = float(ed_installs)
            total += ed_installs
    avg = total/len_cat
    avg_installs[r]=avg

#sorting the dictionary
def display_table_order_l():
    tab = []
    sorted_freq_table = []
    for key in avg_installs:
        val = (avg_installs[key],key)
        tab.append(val)
    sorted_freq_table = sorted(tab, reverse = True)
    for entry in sorted_freq_table:
        print(entry[1], ':', entry[0])
display_table_order_l()


# Building up on previous analysis steps, I can see that Books and Refrence category has good ratings in Google play with an average of 3.6
# 

# # App Profile Recommendation
# 
# Based on my analyis of app genres, user rating and installations in Google play and Apple Store markets, I will recommend Books and Reference genre based apps would be successful in both Google play and App store markets with good scope for in-app ads. Apps in this genre has one of the highest number of user intallations and user ratings in both the markets while the number of apps available in this genre is low with .51% in Apple Store and 2.18% in Google Play. This app profile will be profitable due to less number of competitors and big customer base.
