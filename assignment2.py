import enum
from itertools import count
from posixpath import split
import numpy as np
import datetime



def uniqueList(list):
    x = np.array(list)
    return len(np.unique(x)), np.unique(x)

# create a hashtable for all webservers -> no of occurances.
# find the max occurance from the mapping
def mostFreq(list, uniqlist):
    freq = {}

    for i in list:
        if (i in freq):
            freq[i] += 1
        else:
            freq[i] = 1
    maxOccur = max(freq, key=freq.get)

    return maxOccur

def readLeftFiles():
    ipList = []
    accessTimeMax = []

    with open("intersec/left.txt") as file:
        leftList = file.readlines()

        for count, line in enumerate(leftList):
            
            # Check for unique IP addresses 
            split1 = line.split(" ")
            currentIp = split1[0]
            ipList.append(currentIp)

            # break the datetime object from left.txt
            timeObj = split1[1].replace("[", "").replace("]", "")
            currentDate = datetime.datetime.strptime(timeObj, '%Y-%m-%dT%H:%M:%S%z')
            weekDay = int(currentDate.strftime("%w"))
            onlyHour = int(currentDate.strftime("%H"))
            onlyMin = int(currentDate.strftime("%M"))
            onlySec = int(currentDate.strftime("%S"))

            # Monday to Friday 8:15 pm (taking 30 sec interval on both sides)
            if (weekDay < 5 and onlyHour == 20):
                if (onlyMin == 14 and onlySec > 30):
                    accessTimeMax.append(currentIp)
                elif (onlyMin == 15 and onlySec < 30):
                    accessTimeMax.append(currentIp)

        uniqIpCounter = uniqueList(ipList)[0]
        ipListForMax = uniqueList(accessTimeMax)  

    return count + 1, uniqIpCounter, ipListForMax

def readRightFiles():
    webServerList = []

    with open("intersec/right.txt", 'r') as file:
        rightList = file
        for count, line in enumerate(rightList):
            split1 = line.split("//")[1]
            split2 = split1.split('"')[0]
            webServerList.append(split2)
            
        totalWebServers = uniqueList(webServerList)[0]
    
        mostVisitedServer = mostFreq(webServerList, totalWebServers)


    return count + 1, totalWebServers, mostVisitedServer

     
def main():
    
    # number of entries in left.txt & right.txt
    result_left = readLeftFiles()[0]
    result_right = readRightFiles()[0]
    
    print("Result left: ", result_left)
    print("Result right: ", result_right)

    uniqIpCount = readLeftFiles()[1]
    print("Number of unique users: ", uniqIpCount)

    noOfServes = readRightFiles()[1]
    print("Number of accessed webservers: ", noOfServes)
    
    mostFreqServer = readRightFiles()[2]
    print("Most visited webserver: ", mostFreqServer)
    

    totalCandidateIP = readLeftFiles()[2][0]
    candidateList = readLeftFiles()[2][1]
    print("Total candidate IP: ", totalCandidateIP)
    print("Candidate IP List: ", candidateList)
    
if __name__ == '__main__':
    main()       