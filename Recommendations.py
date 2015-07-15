from __future__ import division
import sys
import math

if len(sys.argv)<= 0:
    print "Too few arguments"
    exit()

#************************************************************************************#

def pcc(dataset,user,rest_users):
            #List of common items rated by both user and rest user
            item_similarity = {}
            for item in dataset[user]:
                    if item in dataset[rest_users]:
                            item_similarity[item] = 1

            #Number of mutually rated items
            num_similar_items = len(item_similarity)
            #If no rating in common, return 0
            if num_similar_items== 0:
                return 0

            #Calculating Pearson Correlation Coefficient
            simple_sum1 = sum([dataset[user][itm] for itm in item_similarity])
            simple_sum2 = sum([dataset[rest_users][itm] for itm in item_similarity])

            square_sum1 = sum([pow(dataset[user][itm],2) for itm in item_similarity])
            square_sum2 = sum([pow(dataset[rest_users][itm],2) for itm in item_similarity])

            product_sum = sum([dataset[user][itm] * dataset[rest_users][itm] for itm in item_similarity])

            numerator = product_sum - (simple_sum1 * simple_sum2/(num_similar_items))
            denominator = sqrt((square_sum1 - pow(simple_sum1,2)/(num_similar_items)) * (square_sum2 - pow(simple_sum2,2)/(num_similar_items)))

            if denominator == 0:
                    return 0

            #Pearson similarity score
            pss = numerator/denominator

            return pss

#************************************************************************************#

def is_biased(dataset,rest_users):
        ratings_numbers={}
        rating_probablity={}
        count,min_rating,max_rating=0,1,10

        for i in range(min_rating,max_rating+1):
            ratings_numbers[i]=0
            rating_probablity[i]=0

        #Finding the number of each rating and total number of ratings for a rest user
        for item in dataset[rest_users]:
            ratings_numbers[dataset[rest_users][item]]+=1
            count+=1

        #If rest user has done no rating, return 0 entropy
        if count==0:
            return 0

        #For users with less than 10 ratings, ignore entropies
        if count<10:
            return -1

        for j in range(min_rating,max_rating+1):
            #Finding probability of using each rating
            rating_probablity[j]+=float(ratings_numbers[j]/count)

            #Since using math.log, convert rating_probability with 0 value to 1. log(1)=0, so no net effect
            if rating_probablity[j]==0:
                rating_probablity[j]=1

        entropy=0

        #Finding total entropy
        for k in range(min_rating,max_rating+1):
            #print "rating prob: ",rating_probablity[k]
            entropy+=(-rating_probablity[k]*(math.log(rating_probablity[k])))

        #print "entropy:                 ",entropy
        return entropy


#************************************************************************************#

def find_suggestions(dataset,user):
            scores = {}
            similarity_sum = {}
            biased_users={}

            for rest_users in dataset:

                    #If both same, then continue
                    if rest_users == user:
                            continue

                    #Finding entropies for rest suers to remove biased users
                    entropy=is_biased(dataset,rest_users)

                    #Ignoring rest users with entropies less than 0.5 and collecting the IDs of biased users
                    if entropy>=0 and entropy<=0.5:
                        if entropy>0:
                            biased_users[rest_users]=entropy
                        continue

                    #Pearson Similarity scores
                    similarity = pcc(dataset,user,rest_users)

                    #Ignore for 0 similarity
                    if similarity <= 0:
                            continue

                    #Finding total similarity scores
                    for item in dataset[rest_users]:
                            #Only for items the user hasn't rated yet
                            if item not in dataset[user] or dataset[user][item] == 0:
                                    scores.setdefault(item,0)
                                    scores[item] += dataset[rest_users][item] * similarity

                                    similarity_sum.setdefault(item,0)
                                    similarity_sum[item] += similarity


            #Finding top biased users
            top_biased_users=sorted(biased_users, key=biased_users.__getitem__)
            #Top 10 biased users
            print "\nTop 15 biased users: "
            for bias in top_biased_users[0:15]:
                print bias
            
            #List of similarities
            results = [(scores/similarity_sum[item],item) for item,scores in scores.items()]

            #Sorting the list in decreasing order
            results.sort(reverse=True)

            #Return top 7 results
            return results[0:30]

#....................................................................................#


#Importing the dataset
from dataset import *

#Input
user= raw_input("Enter the ID of the person whom to recommend: ")

#Finding suggestions
suggestions=find_suggestions(dataset,user)


print "Top 10 Recommendations for user %s are: " %user
for suggestion in suggestions:
    print suggestion

