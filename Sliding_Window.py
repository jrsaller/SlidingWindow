#import pandas
import DataTools as tools
import math
import matplotlib.pyplot as plt

DATAFILE = "Zion(2017-19)V_4.xlsx"

#Setup the dataset as an easily-accessible matrix
def setup(dataset):
    data = tools.extractSpreadsheet(DATAFILE,dataset)
    return data

#Calculate the average of the given list
def avg(lst):
    return sum(lst)/len(lst)

def predictDayUsingWeather(data,month,day,year,p):
    TYPW = tools.dateRange(tools.dateToIndex([month,day-1,year]),6,0)
    ThisYearsWindow = []
    #populate This Year's window with data from our spreadsheet
    for index in TYPW:
        ThisYearsWindow.append((data.getVal(index,0),data.getVal(index,1)))
    q = []
    for i in range(len(TYPW)):
        q.append((tools.indexToDate(TYPW[i]),ThisYearsWindow[i][0],ThisYearsWindow[i][1]))
    if p:
        print("\n======LAST WEEK WINDOW========")
        for item in q:
            print(str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2]))
        print("==============================")
    
    
    #Last Years Window (Index Form)
    LYWI = tools.dateRange(tools.dateToIndex([month,day,year-1]),7,6)
    #Last Year Mega Window
    LY = []
    for index in LYWI:
        LY.append((data.getVal(index,0),data.getVal(index,1)))
    if p:    
        print("\n======LAST YEAR BIG WINDOW======")
        for item in range(len(LYWI)):
            print(str(tools.indexToDate(LYWI[item])) + "\t" + str(LY[item][0]) + "\t" + str(LY[item][1]))
        print("=================================")
    #Use the first window as the baseline window
    LastYearWeather = []
    for item in LY:
        LastYearWeather.append(item[1]) 
    #print(LastYearWeather)
    lowestAvg = avg(LastYearWeather)
    lowWindow = LY[0:7]
    if p:
        print(lowWindow)
    #get the average weather of this year's window
    ThisYearWeather = []
    for item in ThisYearsWindow:
        ThisYearWeather.append(item[1]) 
    TYA = avg(ThisYearWeather)
    #loop over Last Years Mega Window, generate smaller windows to compare with this year
    for i in range(1,8):
        #get the window in a list
        window = LY[i:i+7]
        TempLastYearWeather = []
        #calculate the average of the window
        for item in window:
            TempLastYearWeather.append(item[1]) 
        windowAverage = avg(TempLastYearWeather)
        #if the average of this window is closer to this years average, change so this window is the new closest window
        if p:
            print(TYA)
            print(windowAverage)
            print(lowestAvg)
            print("=================")
        if abs(windowAverage-TYA) < abs(lowestAvg-TYA):
            if p:
                print("WINDOW HAS CHANGED")
            lowestAvg = windowAverage
            lowWindow = LY[i:i+7]
    if p:
        print("\n=========SELECTED LOW WINDOW=========")
        for item in lowWindow:
            print(item)
        print("=====================================")
    #calculate the day to day variance of This Years Window
    TYW = []
    for item in ThisYearsWindow:
       TYW.append(item[1])
    #print(TYW)
    LYW = []
    for item in lowWindow:
        LYW.append(item[1])
    #print(LYW)
    varianceTY = []
    for i in range(len(TYW)-1):
        varianceTY.append(TYW[i+1] - TYW[i])
    if p:
        print("\n=========THIS YEARS VARIANCE=========")
        for item in varianceTY:
            print(item)
        print("=====================================")
    #calculate the day to day variance of Last Year's Window
    varianceLY = []
    for j in range(len(LYW)-1):
        varianceLY.append(LYW[j+1] - LYW[j])
    if p:
        print("\n=========LAST YEARS WINDOW VARIANCE=========")
        for item in varianceLY:
            print(item)
        print("=============================================")
    #Calculate the average variance for last year's window and this years window
    VLY = avg(varianceLY)
    VLW = avg(varianceTY)
    #find the average of this year's variance average nd last year's variance average
    newVariance = (VLY + VLW) / 2
    if p:
        print("\n===============AVERAGE VARIANCE==============")
        print("Last Year's Average Variance:",str(VLY))
        print("Last Week's Average Variance: ",str(VLW))
        print("New Variance: ",str(newVariance))
        print("Result:",TYW[-1],"+",newVariance,"=",TYW[-1]+newVariance)
        print("=============================================")
    if VLY > 800:
        print(month,day,year)
    
    
    #take the day before the one we are predicting, add the newly calculated variance, and return that number
    return TYW[-1] + newVariance


#Sliding Window Algorithm Workhorse
def predictDay(data,month,day,year,p):
    #get last year's data
    #This Years Previous Week (Index Form)
    TYPW = tools.dateRange(tools.dateToIndex([month,day-1,year]),6,0)
    
    ThisYearsWindow = []
    #populate This Year's window with data from our spreadsheet
    for index in TYPW:
        ThisYearsWindow.append(data.getVal(index,0))
    q = []
    for i in range(len(TYPW)):
        q.append((tools.indexToDate(TYPW[i]),ThisYearsWindow[i]))
    if p:
        print("\n======LAST WEEK WINDOW========")
        for item in q:
            print(str(item[0]) + "\t" + str(item[1]))
        print("==============================")
    
    
    #Last Years Window (Index Form)
    LYWI = tools.dateRange(tools.dateToIndex([month,day,year-1]),7,6)
    #Last Year Mega Window
    LY = []
    for index in LYWI:
        LY.append(data.getVal(index,0))
    if p:    
        print("\n======LAST YEAR BIG WINDOW======")
        for item in range(len(LYWI)):
            print(str(tools.indexToDate(LYWI[item])) + "\t" + str(LY[item]))
        print("=================================")
    #Use the first window as the baseline window
    lowWindow = LY[0:7]
    LD = 0
    for i in range(len(lowWindow)):
        LD += (lowWindow[i] - ThisYearsWindow[i]) ** 2
    LD /= 7
    #get the average population of this year's window
    #TYA = avg(ThisYearsWindow)
    #loop over Last Years Mega Window, generate smaller windows to compare with this year
    for i in range(1,8):
        #get the window in a list
        window = LY[i:i+7]
        #calculate the average of the window
        #windowAverage = avg(window)
        tempdist =0
        for j in range(len(window)):
            tempdist += (window[j]-ThisYearsWindow[j]) ** 2
        tempdist /= 7
        if tempdist < LD:
            lowWindow = window
            LD = tempdist
        #if the average of this window is closer to this years average, change so this window is the new closest window
        #if abs(windowAverage-TYA) < abs(lowestAvg-TYA):
        #    lowestAvg = windowAverage
        #    lowWindow = LY[i:i+7]
#   RETURN LOWWINDOW            
    if p:
        print("\n=========SELECTED LOW WINDOW=========")
        for item in lowWindow:
            print(item)
        print("=====================================")
   #calculate the day to day variance of This Years Window
    varianceTY = []
    for i in range(len(ThisYearsWindow)-1):
        varianceTY.append(ThisYearsWindow[i+1] - ThisYearsWindow[i])
    if p:
        print("\n=========THIS YEARS VARIANCE=========")
        for item in varianceTY:
            print(item)
        print("=====================================")
    #calculate the day to day variance of Last Year's Window
    varianceLY = []
    for j in range(len(lowWindow)-1):
        varianceLY.append(lowWindow[j+1] - lowWindow[j])
    if p:
        print("\n=========LAST YEARS WINDOW VARIANCE=========")
        for item in varianceLY:
            print(item)
        print("=============================================")
    #Calculate the average variance for last year's window and this years window
    VLY = avg(varianceLY)
    VLW = avg(varianceTY)
    #find the average of this year's variance average nd last year's variance average
    newVariance = (VLY + VLW) / 2
    if p:
        print("\n===============AVERAGE VARIANCE==============")
        print("Last Year's Average Variance:",str(VLY))
        print("Last Week's Average Variance: ",str(VLW))
        print("New Variance: ",str(newVariance))
        print("Result:",ThisYearsWindow[-1],"+",newVariance,"=",ThisYearsWindow[-1]+newVariance)
        print("=============================================")
    if VLY > 800:
        print(month,day,year)
    
    
    #take the day before the one we are predicting, add the newly calculated variance, and return that number
    return ThisYearsWindow[-1] + newVariance

#Ask the user which specific day to predict for
def askUser(data,a):
   date = input("What day do you want to predict? (mmddyy) : ")
   if a ==1:
       answer = predictDay(data,int(date[0:2]),int(date[2:4]),int(date[4:]),True)
   elif a == 2:
       answer = predictDayUsingWeather(data,int(date[0:2]),int(date[2:4]),int(date[4:]),True)
   print("You should see " + str(answer) + " People on that day")

#Plot the list, using the provided xlabel for the x-axis and ylabel for the y-axis
def plotData(lst,xlabel,ylabel):
    plt.plot(lst)
    plt.xlabel(xlabel)
    plt.show()

    
holidays = [[1,15,18],[2,19,18],[5,28,18],[7,4,18],[7,24,18],[9,3,18],[11,12,18],[11,22,18]]
   
def calcOverallError(data): 
    count=0
   #Calculating the percent error for the entire year of data
    percentLst = []
    highPercentDictionary = {}
    #Loop starting Jan 1 2018 
    for i in range(365,1011):
        #Get the correct day in a list form [M, D, Y]
        day = tools.indexToDate(i)
        answer=predictDay(data,day[0],day[1],day[2],False)
        if data.getVal(i,0) == 0:
            percent = 0.0
        else:
            percent = abs(answer-data.getVal(i,0))/data.getVal(i,0)
        percent *= 100
        if percent >= 10:
            #print(day)
            count+=1
#        if day in holidays:
#            print("=======================")
#            print(day)
#            print("++++++++++++\nDAY BEFORE")
#            db = tools.indexToDate(i-1)
#            print(db)
#            print("Prediction:",predictDay(data,db[0],db[1],db[2],False))
#            print("Actual:",data.getVal(i-1,0))
#            print("++++++++++++++")
#            print("Prediction:",answer)
#            print("Actual:",data.getVal(i,0))
#            print("Percent:",percent)
#            if answer > data.getVal(i,0):
#                print("Too High")
#            else:
#                print("Too Low")
#            print("==============================")
#        
        
        if percent > 40 or percent < 0.0:
            highPercentDictionary[tools.dateToIndex(day)] = percent
            #print(day,"\t",percent)
        if not math.isnan(percent):
            percentLst.append(percent)
        else:
            print(day)
    #print(tools.indexToDate(i))
    #percentLst2 = percentLst[:]
    #print(percentLst)
    print("DAYS OVER 10 PERCENT:",count)
    print(len(highPercentDictionary))
    print("TOTAL AVERAGE ERROR: " + str(avg(percentLst)))
    print("MAX ERROR:",max(percentLst))
    print("MIN ERROR",min(percentLst))
    print()
    
    #percentLst.sort()
    newPercentList = []
   
    for item in percentLst:
        if item >= 0 and item < 400:
            newPercentList.append(item)
    #newPercentList.sort()
    #secondNewPercentList = newPercentList[:]
    #print(newPercentList)
    print("CORRECTED MAX ERROR:",max(newPercentList))
    print("CORRECTED MIN ERROR:",min(newPercentList))
    print("CORRECTED AVERAGE ERROR:" , avg(newPercentList))
    
    plotData(newPercentList,"Days Since Jan 1, 2018","Percent Error")
    
    newPercentList.sort()
    #print(newPercentList)
    maxPercentList=newPercentList[len(newPercentList)-20:]
    print("Highest Percent error list:")
    print(maxPercentList)
    percentDictionary = {}
    for e in maxPercentList:
        for key in highPercentDictionary:
            if highPercentDictionary[key] == e:
                x=key
                break
        #x = percentLst.index(e)
        print(x)
        percentDictionary[x] = e
        print(tools.indexToDate(x),e)
    print("==========================")
    dayDictionary = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,}
    high = 0
    low = 0
    for key in percentDictionary:
        day = tools.indexToDate(key)
        #print(day)
        percentError = percentDictionary[key]
        DOW = data.getVal(key,1)
        actual = data.getVal(key,0)
        prediction = predictDay(data,day[0],day[1],day[2],False)
        print(percentError)
        print(DOW)
        dayDictionary[DOW] += 1
        print(str(day) + "\t\tACT: " + str(actual) + "\t\tCALC: " + str(prediction))
        if prediction > actual:
            print("+++++++ TOO HIGH +++++++++")
            high+=1
        else:
            print("--------- TOO LOW ---------")
            low+=1
    print(dayDictionary)
    print("HIGH:",high)
    print("LOW:",low)
   
    
def calcOverallErrorWeather(data):
    count=0
   #Calculating the percent error for the entire year of data
    percentLst = []
    #highPercentDictionary = {}
    #Loop starting Jan 1 2018 
    for i in range(365,1011):
        #Get the correct day in a list form [M, D, Y]
        day = tools.indexToDate(i)
        answer=predictDayUsingWeather(data,day[0],day[1],day[2],False)
        #print(answer)
        if data.getVal(i,1) == 0:
            percent = 0.0
        else:
            percent = abs(answer-data.getVal(i,1))/data.getVal(i,1)
        percent *= 100
        if percent >= 10:
            #print(day)
            count+=1
#        if day in holidays:
#            print("=======================")
#            print(day)
#            print("++++++++++++\nDAY BEFORE")
#            db = tools.indexToDate(i-1)
#            print(db)
#            print("Prediction:",predictDay(data,db[0],db[1],db[2],False))
#            print("Actual:",data.getVal(i-1,0))
#            print("++++++++++++++")
#            print("Prediction:",answer)
#            print("Actual:",data.getVal(i,0))
#            print("Percent:",percent)
#            if answer > data.getVal(i,0):
#                print("Too High")
#            else:
#                print("Too Low")
#            print("==============================")
#        
        
        #if percent > 40 or percent < 0.0:
        #    highPercentDictionary[tools.dateToIndex(day)] = percent
            #print(day,"\t",percent)
        if not math.isnan(percent):
            percentLst.append(percent)
#        else:
#            print(day)
    #print(tools.indexToDate(i))
    #percentLst2 = percentLst[:]
    #print(percentLst)
    #print("DAYS OVER 10 PERCENT:",count)
    #print(len(highPercentDictionary))
    print("TOTAL AVERAGE ERROR: " + str(avg(percentLst)))
    print("MAX ERROR:",max(percentLst))
    print("MIN ERROR",min(percentLst))
    print()
    
    #percentLst.sort()
    newPercentList = []
   
    for item in percentLst:
        if item >= 0 and item < 400:
            newPercentList.append(item)
    #newPercentList.sort()
    #secondNewPercentList = newPercentList[:]
    #print(newPercentList)
    print("CORRECTED MAX ERROR:",max(newPercentList))
    print("CORRECTED MIN ERROR:",min(newPercentList))
    print("CORRECTED AVERAGE ERROR:" , avg(newPercentList))
    
    plotData(newPercentList,"Days Since Jan 1, 2018","Percent Error")
    
    newPercentList.sort()
    #print(newPercentList)
    maxPercentList=newPercentList[len(newPercentList)-20:]
    print("Highest Percent error list:")
    print(maxPercentList)
    #percentDictionary = {}
    #for e in maxPercentList:
    #    for key in highPercentDictionary:
    #        if highPercentDictionary[key] == e:
    #            x=key
    #            break
    #    x = percentLst.index(e)
    #    print(x)
    #    percentDictionary[x] = e
    #    print(tools.indexToDate(x),e)
    print("==========================")
    #dayDictionary = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,}
    #high = 0
    #low = 0
    #for key in percentDictionary:
    #    day = tools.indexToDate(key)
        #print(day)
    #    percentError = percentDictionary[key]
        #DOW = data.getVal(key,1)
        #actual = data.getVal(key,1)
        #prediction = predictDayUsingWeather(data,day[0],day[1],day[2],False)
        #print(percentError)
        #print(DOW)
        #dayDictionary[DOW] += 1
    #    print(str(day) + "\t\tACT: " + str(actual) + "\t\tCALC: " + str(prediction))
    #    if prediction > actual:
    #        print("+++++++ TOO HIGH +++++++++")
    #        high+=1
    #    else:
    #        print("--------- TOO LOW ---------")
    #        low+=1
    #print(dayDictionary)
    #print("HIGH:",high)
    #print("LOW:",low)
   
    
    
def calcOverallErrorModel3(data1,data2):
    count=0
   #Calculating the percent error for the entire year of data
    percentLst = []
    #highPercentDictionary = {}
    #Loop starting Jan 1 2018
    data = data2
    for i in range(365,1011):
        #Get the correct day in a list form [M, D, Y]
        day = tools.indexToDate(i)
        answer1=predictDayUsingWeather(data2,day[0],day[1],day[2],False)
        answer2=predictDay(data1,day[0],day[1],day[2],False)
        answer=(answer1+answer2)/2.0
        #print(answer)
        if data.getVal(i,1) == 0:
            percent = 0.0
        else:
            percent = abs(answer-data.getVal(i,1))/data.getVal(i,1)
        percent *= 100
        if percent >= 10:
            #print(day)
            count+=1
#        if day in holidays:
#            print("=======================")
#            print(day)
#            print("++++++++++++\nDAY BEFORE")
#            db = tools.indexToDate(i-1)
#            print(db)
#            print("Prediction:",predictDay(data,db[0],db[1],db[2],False))
#            print("Actual:",data.getVal(i-1,0))
#            print("++++++++++++++")
#            print("Prediction:",answer)
#            print("Actual:",data.getVal(i,0))
#            print("Percent:",percent)
#            if answer > data.getVal(i,0):
#                print("Too High")
#            else:
#                print("Too Low")
#            print("==============================")
#        
        
        #if percent > 40 or percent < 0.0:
        #    highPercentDictionary[tools.dateToIndex(day)] = percent
            #print(day,"\t",percent)
        if not math.isnan(percent):
            percentLst.append(percent)
#        else:
#            print(day)
    #print(tools.indexToDate(i))
    #percentLst2 = percentLst[:]
    #print(percentLst)
    #print("DAYS OVER 10 PERCENT:",count)
    #print(len(highPercentDictionary))
    print("TOTAL AVERAGE ERROR: " + str(avg(percentLst)))
    print("MAX ERROR:",max(percentLst))
    print("MIN ERROR",min(percentLst))
    print()
    
    #percentLst.sort()
    newPercentList = []
   
    for item in percentLst:
        if item >= 0 and item < 400:
            newPercentList.append(item)
    #newPercentList.sort()
    #secondNewPercentList = newPercentList[:]
    #print(newPercentList)
    print("CORRECTED MAX ERROR:",max(newPercentList))
    print("CORRECTED MIN ERROR:",min(newPercentList))
    print("CORRECTED AVERAGE ERROR:" , avg(newPercentList))
    
    plotData(newPercentList,"Days Since Jan 1, 2018","Percent Error")
    
    newPercentList.sort()
    #print(newPercentList)
    maxPercentList=newPercentList[len(newPercentList)-20:]
    print("Highest Percent error list:")
    print(maxPercentList)
    #percentDictionary = {}
    #for e in maxPercentList:
    #    for key in highPercentDictionary:
    #        if highPercentDictionary[key] == e:
    #            x=key
    #            break
    #    x = percentLst.index(e)
    #    print(x)
    #    percentDictionary[x] = e
    #    print(tools.indexToDate(x),e)
    print("==========================")
    #dayDictionary = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0,}
    #high = 0
    #low = 0
    #for key in percentDictionary:
    #    day = tools.indexToDate(key)
        #print(day)
    #    percentError = percentDictionary[key]
        #DOW = data.getVal(key,1)
        #actual = data.getVal(key,1)
        #prediction = predictDayUsingWeather(data,day[0],day[1],day[2],False)
        #print(percentError)
        #print(DOW)
        #dayDictionary[DOW] += 1
    #    print(str(day) + "\t\tACT: " + str(actual) + "\t\tCALC: " + str(prediction))
    #    if prediction > actual:
    #        print("+++++++ TOO HIGH +++++++++")
    #        high+=1
    #    else:
    #        print("--------- TOO LOW ---------")
    #        low+=1
    #print(dayDictionary)
    #print("HIGH:",high)
    #print("LOW:",low)
    
def main():
    #data = setup(["Adjusted", "Day"])
    #data = setup(["Canyon Total Visitation", "Day"])
    calc = input("Calculate overall, or ask user? (ask or calc)")
    print("1.) Original Model (Population only)")
    print("2.) Weather model")
    print("3.) Combined 1 AND 2")
    a = int(input("What model would you like to use?"))
    
    if calc in "ask":
        if a == 1:
            data = setup(["Adjusted","Day"])
        elif a == 2:
            data = setup(["Max Temp","Adjusted","Day"])
        askUser(data,a)
    else:
        
        if a == 1:
            data = setup(["Adjusted","Day"])
            calcOverallError(data)
        elif a == 2:
            data = setup(["Max Temp","Adjusted","Day"])
            calcOverallErrorWeather(data)
        elif a==3:
            data1 = setup(["Adjusted","Day"])
            data2 = setup(["Max Temp","Adjusted","Day"])
            calcOverallErrorModel3(data1,data2)
      
main()