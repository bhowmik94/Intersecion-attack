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

def findIpFromLeft(list):
    with open("intersec/left.txt") as file:
        leftList = file
        ipPool = []
        for count, line in enumerate(leftList):
            
            split1 = line.split(" ")
            timeObj = split1[1].replace("[", "").replace("]", "")
            if (timeObj in list):
                ipPool.append(line)
        uniqIp = uniqueList(ipPool)[1]
        print(uniqIp)

def readRightFiles():
    webServerList = []
    timeOfAccess = []

    with open("intersec/right.txt", 'r') as file:
        rightList = file
        for count, line in enumerate(rightList):
            split1 = line.split("//")[1]
            split2 = split1.split('"')[0]
            webServerList.append(split2)
            
            time = line.split(" ")[0].replace("[", "").replace("]", "")
            currentDate = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
            onlyHour = int(currentDate.strftime("%H"))
            onlyMin = int(currentDate.strftime("%M"))
            onlySec = int(currentDate.strftime("%S"))

            if (split2 == "www.tv-movie.de"):
                if (onlyHour == 21 and onlyMin == 59 and onlySec >= 0):
                    for i in range(1, 6):
                        if (i == 1):    
                            timeOfAccess.append(time)
                        chng = time.replace(str(onlySec), str(onlySec - i))
                        timeOfAccess.append(chng)
                elif (onlyHour == 22 and onlyMin == 1):
                    for i in range(1, 6):
                        if (i == 1):    
                            timeOfAccess.append(time)
                        chng = time.replace(str(onlySec), str(onlySec - i))
                        timeOfAccess.append(chng)
                elif (onlyHour == 22 and onlyMin == 0 and onlySec <= 59):
                    for i in range(1, 6):
                        if (i == 1):    
                            timeOfAccess.append(time)
                        chng = time.replace(str(onlySec), str(onlySec - i))
                        timeOfAccess.append(chng)
        findIpFromLeft(timeOfAccess)
            

            
        totalWebServers = uniqueList(webServerList)[0]
        # print(timeOfAccess)
        mostVisitedServer = mostFreq(webServerList, totalWebServers)


    return count + 1, totalWebServers, mostVisitedServer

     
def main():
    
    # number of entries in left.txt & right.txt
    result_left = readLeftFiles()
    result_right = readRightFiles()
    
    print("Result left: ", result_left[0])
    print("Result right: ", result_right[0])

    uniqIpCount = result_left[1]
    print("Number of unique users: ", uniqIpCount)

    noOfServes = result_right[1]
    print("Number of accessed webservers: ", noOfServes)
    
    mostFreqServer = result_right[2]
    print("Most visited webserver: ", mostFreqServer)
    

    totalCandidateIP = result_left[2][0]
    candidateList = result_left[2][1]
    print("Total candidate IP: ", totalCandidateIP)
    print("Candidate IP List: ", candidateList)
    
if __name__ == '__main__':
    main()       