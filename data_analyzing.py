# Function to check if a certain ad suits the kind of \
# ads we would like to work with in the future
def is_ad_relevant(ad):
    if ("Albert" in ad['campaign']):
        if ((not '--' in ad["clicks"]) and (ad["impressions"] != '0')):
            return True
    return False

#Function to solve question number 1
def best_performing_ad_per_period(reader):
    best_ctr_value = 0
    for ad in reader:
        if (is_ad_relevant(ad)):
            temp_ctr = int(ad["clicks"]) / int(ad["impressions"])
            if (temp_ctr > best_ctr_value):
                best_ctr_value = temp_ctr
                best_ad = ad
    return best_ad

#Function to solve question number 2
def best_performing_ad_each_day(reader):
    days_best_ad = {}
    for ad in reader:
        if (is_ad_relevant(ad)):
            if (not ad["date"] in days_best_ad):
                days_best_ad[ad["date"]] = ad
            else:
                temp_ctr = int(ad["clicks"]) / int(ad["impressions"])
                if (temp_ctr > int(days_best_ad[ad["date"]]["clicks"]) / int(days_best_ad[ad["date"]]["impressions"])):
                    days_best_ad[ad["date"]] = ad
    return days_best_ad

#Function for question 3
def get_groupIds_stats(reader):
    group_stats = {}
    for ad in reader:
        if (is_ad_relevant(ad)):
            if (not ad['adGroupId'] in group_stats):
                group_stats[ad["adGroupId"]]={}
                group_stats[ad["adGroupId"]]["num_ads"] = 1
                group_stats[ad["adGroupId"]]["sum_ctr"] =float(ad["clicks"]) / float(ad["impressions"])
                group_stats[ad["adGroupId"]]["campaign"] = ad["campaign"]
            else:
                group_stats[ad["adGroupId"]]["num_ads"] += 1
                group_stats[ad["adGroupId"]]["sum_ctr"] += float(ad["clicks"]) / float(ad["impressions"])
    return group_stats

def get_campaign_stats(reader):
    campaign_stats={}
    group_stats = get_groupIds_stats(reader)
    for id in group_stats:
        if (not group_stats[id]["campaign"] in campaign_stats):
            campaign_stats[group_stats[id]["campaign"]]={}
            campaign_stats[group_stats[id]["campaign"]]["sum_ctr"]=group_stats[id]["sum_ctr"]
            campaign_stats[group_stats[id]["campaign"]]["num_ads"] = group_stats[id]["num_ads"]
        else:
            campaign_stats[group_stats[id]["campaign"]]["sum_ctr"] += group_stats[id]["sum_ctr"]
            campaign_stats[group_stats[id]["campaign"]]["num_ads"] += group_stats[id]["num_ads"]
    return  campaign_stats

#This function is good for question 3 - to get best campaign or group ids stats
def get_best_group(stats):
    max_avg=0
    max_id = None
    for id in stats:
        tmp_ctr = float(stats[id]["sum_ctr"]) / float(stats[id]["num_ads"])
        if tmp_ctr > max_avg:
            max_avg= tmp_ctr
            max_id=id
    return ("CTR=",float(stats[max_id]["sum_ctr"]/stats[max_id]["num_ads"]),"Name/ID=",max_id)

#For question 4
def ad_group_sum_impressions(reader):
    ad_group_vs_sum_imp={}
    for ad in reader:
        if "Albert" in ad["campaign"]:
            if not (ad["adGroupId"] in ad_group_vs_sum_imp):
                ad_group_vs_sum_imp[ad["adGroupId"]]={}
                ad_group_vs_sum_imp[ad["adGroupId"]]["sum_imp"] = int(ad["impressions"])
                ad_group_vs_sum_imp[ad["adGroupId"]]["campaign"] = ad["campaign"]
            else:
                ad_group_vs_sum_imp[ad["adGroupId"]]["sum_imp"] += int(ad["impressions"])
    return ad_group_vs_sum_imp


def camp_group_imp_sums(reader):
    camp_sum_dict={}
    group_sum_imp = ad_group_sum_impressions(reader)
    for id in group_sum_imp:
        if not group_sum_imp[id]["campaign"] in camp_sum_dict:
            camp_sum_dict[group_sum_imp[id]["campaign"]]=[]
            tmp_list = [id, group_sum_imp[id]["sum_imp"]]
            camp_sum_dict[group_sum_imp[id]["campaign"]].append(tmp_list)
        else:
            tmp_list=[id,group_sum_imp[id]["sum_imp"]]
            camp_sum_dict[group_sum_imp[id]["campaign"]].append(tmp_list)
    #every camp has a 2d list when each inner list is [0] group id , [1] the group id sum of imps
    #here we sort the 2d list by the sum of imps
    return camp_sum_dict

def get_lowest_quartile_per_camp(reader):
    from operator import itemgetter
    camp_sum_dict=camp_group_imp_sums(reader)
    for camp in camp_sum_dict:
        camp_sum_dict[camp] = sorted(camp_sum_dict[camp], key=itemgetter(1))
    for camp in camp_sum_dict:
        ids_list=[]
        camp_sum_dict[camp] = camp_sum_dict[camp][:len(camp_sum_dict[camp])/4]
        for lst in camp_sum_dict[camp]:
            ids_list.append(lst[0])
        camp_sum_dict[camp]=ids_list
    return camp_sum_dict

def is_group_in_camp_low_quartile(camp_low_quartile_imp_dict,group_id):
    for camp in camp_low_quartile_imp_dict:
        if group_id in camp_low_quartile_imp_dict[camp]:
            return True
    return False

def check_all_group_ids(reader):
    ads = (ad_group_sum_impressions(reader))
    in_file.seek(0)
    low_quartile = get_lowest_quartile_per_camp(reader)
    for id in ads:
        print(id, is_group_in_camp_low_quartile(low_quartile, str(id)))


import csv
num_pre_headers = 3
in_filename = "albert_dev_test.csv"
with open(in_filename, 'r') as in_file:
    # skipping pre-headers. could be more elegant and dynamic, for this
    # home task I decided to keep it simple
    for i in range(num_pre_headers):
        in_file.next()
    reader = csv.DictReader(in_file)
    reader.fieldnames = [i for i in reader.fieldnames]
    fieldnames = reader.fieldnames
    # Using fieldnames makes the code more readable, and will force all \
    # programmers to use same syntax when refering to fields in the files
    print ("Adgorithms home task - Yoav Zaltsman")
    print("This is the best performing ad for the entire period actually it has a ctr=1")
    print("ideally in such cases we would return a list of all ads with CTR of 1")
	
    print(best_performing_ad_per_period(reader))
    in_file.seek(0)

    print('\n\n')
    print("Best performing ad for each day in the period given")
    best_each_day=(best_performing_ad_each_day(reader))
    for key in best_each_day:
        print(key, best_each_day[key])
    in_file.seek(0)

    print('\n\ngroupIds_stats')
    print get_groupIds_stats(reader)
    in_file.seek(0)

    print('\n\nget campaign stats')
    print get_campaign_stats(reader)
    in_file.seek(0)

    print('\n\nget best group - for ad groups')
    print(get_best_group(get_groupIds_stats(reader)))
    in_file.seek(0)

    print('\n\nget best group- for campaigns!')
    print(get_best_group(get_campaign_stats(reader)))
    in_file.seek(0)

    print('\n\n ad group sum impressions')
    print ad_group_sum_impressions(reader)
    in_file.seek(0)

    print('\n\ncamp group impressions sums')
    print camp_group_imp_sums(reader)
    in_file.seek(0)

    print('\n\nlowest quartaile for each campaign')
    dic=get_lowest_quartile_per_camp(reader)
    in_file.seek(0)

    print('\n\nchecking all group ids - if they are in their campaign lowest quartile by impressions')
    check_all_group_ids(reader)
    in_file.seek(0)

print("run finished")
