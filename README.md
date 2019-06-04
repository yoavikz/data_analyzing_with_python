# data_analyzing_with_python_adgorithms
data analyzing with python - from 2016


Here are my comments and explanations for my code. I tried to avoid “repeating myself” in the code, and write a dynamic code with short functions. 
In my code I decided to print all functions outputs to console so you can go through it, instead of writing to files as I would do in my workplace. This is because I tried not to spend too much time and give this task 3-4 hours as I was instructed. Ideally, I would write a more dynamic code and write the results to files. 
I wrote the function “best_performing_ad_per_period(reader)” to find the ad with best CTR of the whole time period given (question number 1). The function inputs a CSVreader object as input, and outputs the ad with best CTR score. The “best_performing_ad_per_period(reader)” function iterates all ads and compares each ad’s CTR to the best CTR so far.  When running this function on the given data, it returns:
“best_performing_ad_per_period(reader)”
{'bodyText': 'balls, balls balls!', 'adGroupId': '1489318', 'campaign': '#Albert_**[8327983]**_Current_campaign', 'headLine': 'Buy sporting goods', 'cost': '24.65', 'date': '2016-10-23', 'impressions': '2930', 'clicks': '2930'}
“best_performing_ad_per_period(reader)” can be improved so that if multiple ads have a CTR of 1, it will return all of them as a list of ads.
The function “is_ad_relevant(ad)”  is another function which is used by “best_performing_ad_per_period(reader)” and by other functions as well . This function will return True only if the ad is relevant, which means the ad is an “Albert” campaign ad, and does not have ‘- -‘ or ‘0’ as values of clicks and impressions. (To avoid casting error when converting str to int, or division by zero error).
The  function “best_performing_ad_each_day(reader)” was written to get the ad with highest CTR for each day in the range of days given (question number 2). The function inputs a reader object and outputs a dictionary with all days of given period as keys, and each day’s best performing ad as a value. 
When running this function on given data it returns (I only attached the first few elements of the dictionary):
('2016-10-19', {'bodyText': 'balls, balls balls!', 'adGroupId': '7582227', 'campaign': '#Albert_**[8327983]**_Current_campaign', 'headLine': 'Goods buy sports', 'cost': '10.14', 'date': '2016-10-19', 'impressions': '28', 'clicks': '28'})
('2016-10-18', {'bodyText': "don't do sports, its not fun", 'adGroupId': '1276217', 'campaign': '#Albert_**[2935974]**_Current_campaign', 'headLine': 'Sporting The Goods', 'cost': '10.27', 'date': '2016-10-18', 'impressions': '54', 'clicks': '54'})
('2016-10-30', {'bodyText': 'forget everything you know about sports', 'adGroupId': '7924778', 'campaign': '#Albert_**[2935974]**_Current_campaign', 'headLine': 'Sporting Goods - The place for you!', 'cost': '15.594999999999999', 'date': '2016-10-30', 'impressions': '2329', 'clicks': '1119'})

The function “get_groupIds_stats(reader)” returns a dictionary which has a groupID as a key, and its value is details about this groupID – “num_ads” = number of ads for the groupID, “sum_ctr” = a sum of all ads’ CTRs and “campaign” as the name of campaign this group belongs to. When running this function on our data we get (only first element of many):
{'1866565': {'num_ads': 201, 'campaign': '#Albert_**[8327983]**_Current_campaign', 'sum_ctr': 114.2460109167866}, {……….},{……..…}}
The function “get_campaign_stats(reader)”  uses the last described function, “get_groupIds_stats(reader)” to get information of sum of CTR and number of ads for each Albert campaign. When running this function on our data we get the following output:
{'#Albert_**[8327983]**_Current_campaign': {'num_ads': 27348, 'sum_ctr': 14585.327996003147}, '#Albert_**[4488288]**_Current_campaign': {'num_ads': 3886, 'sum_ctr': 2074.372261462827}, '#Albert_**[2935974]**_Current_campaign': {'num_ads': 9351, 'sum_ctr': 4955.2579505693275}}
The two last described functions, will be useful for us when we will use their output dictionaries as inputs to the function “get_best_group(stats)” . This function will output the best performing campaign or groupID, depending on the input (solution for question 3).  It returns the CTR of best performing group / campaign, and the id (if group) or name (if campaign). 
When running this function on groupIDs stats we get the following output:
get_best_group(get_groupIds_stats(reader))
('CTR=', 0.6138474787249513, 'Name/ID=', '8025166')	

When running this function on campaigns stats we get the following output:
get_best_group(get_campaign_stats(reader) 
('CTR=', 0.533806552100573, 'Name/ID=', '#Albert_**[4488288]**_Current_campaign')
For question number 4, I was asked to check each ad group, and state if it is in the lower quartile of its campaign in terms of impressions. I first wrote the function “ad_group_sum_impressions(reader)”. This function outputs a dictionary with group_id as key. The value is another dictionary with sum of impressions for each group_id and name of campaign which the ad group belongs to.
When running the code on the given data we get the following output (only first element of many):
{'1866565': {'sum_imp': 738985, 'campaign': '#Albert_**[8327983]**_Current_campaign'}, {….}}
The next function I wrote to solve this question is “camp_group_imp_sums(reader)”. This function uses the return value from “ad_group_sum_impressions(reader)”  to create a dictionary with campaign as key, and value of all campaigns ad_groups and their sums of impressions. It actually returns the same data as “ad_group_sum_impressions(reader)” , but here the key is the campaign which will help us to 
continue and solve this question.
“camp_group_imp_sums(reader)” returns the following data (only first element of 3 campaigns):
{'#Albert_**[8327983]**_Current_campaign': [['1866565', 738985], ['8569794', 580326], ['1774209', 796391], […],[…]]}
Here the value of each key (each campaign) is a 2d list. Each inner list has [0] group_id , [1] sum of impressions for this group id. I made this in the format of 2d list to make it easier to sort and work with in the next stages.
The next function “get_lowest_quartile_per_camp(reader)” uses the dictionary returned from last described function, “camp_group_imp_sums(reader)”. It sorts the 2d list by sum of impressions, and returns only the ¼ first elements in the sorted list. Which means this function returns a dictionary with campaign as key, and each campaign first ¼ ordered group_ids. 
When running on our data, the function returns (only first elements):
{'#Albert_**[8327983]**_Current_campaign': ['3513344', '4485830', '5475294', '9292440', '7645694', '4975245', '5051924', '1489318',…,…,]}
Which means that for campaign '#Albert_**[8327983]**_Current_campaign' the worst group id by terms of impressions is '3513344', then '4485830' is a just a bit better and so on.
Another function I wrote for this question is “is_group_in_camp_low_quartile(camp_low_quartile_imp_dict,group_id)”. This function inputs a dictionary with campaign as key and list of ids (the return from “camp_group_imp_sums(reader)”.  It is a very simple function and it returns True if the group_id is in the dictionary values, else it returns False. 
The last function I wrote is “check_all_group_ids(reader)”. It actually uses all above functions, and iterates each ad group id to check if it appears in lowest quartile. The function looks like this:
def check_all_group_ids(reader):
    ads = (ad_group_sum_impressions(reader))
    in_file.seek(0)
    low_quartile = get_lowest_quartile_per_camp(reader)
    for id in ads:
        print(id, is_group_in_camp_low_quartile(low_quartile, str(id)))

It prints the following to the screen (only few representative lines):
('1866565', False)
('8569794', False)
('7811335', True)
('9273730', False)
('5960024', True)
('6228142', False)
False means- This ad group is not in its campaign lowest quartile in terms of impressions.
True means- This ad group is in its campaign lowest quartile in terms of impressions.


Optimization
In order to optimize the performance of campaigns, I would try to do some research of the data in the following way : First advertise all ads randomly. Which means – do not try to direct a certain campaign or ad group to specific times / zones / population / gender and so on. Then collect as much relevant data as you can (This is a tough stage because here you have to decide which data is ‘relevant’).  Then learn the patterns of the ads, the ad groups and campaigns. Some ads may have a very low CTR, but on certain conditions (for example advertised on winters, on mobile, at night and for women) have a very high CTR. This is said in order to try not only to compare by CTR, but to also try and get a CTR value for each ad (or group) on each possible condition which may include many variables. You may want to use machine learning tools to help you in this stage. Some ads/groups/campaigns may have relatively high CTR under all conditions and others may have lower CTRs in general, but I think that the most challenging and profitable thing to do is to find those campaigns who have an average CTR, but on specific conditions may have very high CTR. I think that basically,  this is what Albert is trying to do.
Exploration
Such a set of data can be very challenging and interesting to work with. You can analyze it in many ways and always come up with new ideas. I tried to sort the ads in the file according to number of impressions and number of clicks, and also added a field of CTR. Some ideas which came to my mind, are in terms of the text and header of each ad:
Presence of “!” in the header or in the body text.
Presence of positive words: “good”, “sale”
Presence of negative words: “don’t”, “forget”
Repeating words : “balls, balls, balls”
Presence of word “you”
Given more time for this task, I would write functions and try to analyze how does the presence of the above texts in the ad effect its performance.
From what I see in the data and in the code results (especially when looking on best performing ad of each day in the period), I believe that ads with negative words (such as “don’t do sports”) and with repeating words (“balls balls balls”) tend to have more success. Of course these are all just my hypothesis and assumptions and in order to check them you must first  describe your hypothesis clearly and then write code to prove / deny it.


