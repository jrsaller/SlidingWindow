import numpy as np
import pandas as pd
from numpy import linalg as LA
import math
import matplotlib.pyplot as plt

def dateToIndex(date):
    [M,D,Y] = date
    total = D-1
    #This corrects for the fact that January 1st is 0 days away, not January 0th.

    while M > 12:
        Y += 1
        M -= 12
    
    if isLeap(Y):
        total += [0,31,60,91,121,152,182,213,244,274,305,335,366][M-1]
    else:
        total += [0,31,59,90,120,151,181,212,243,273,304,334,365][M-1]
        
    for i in range(17,Y):
        if isLeap(i):
            total += 366
        else:
            total += 365
    return total

def isLeap(Y):
    #Every year divisible by 4 is a leap year EXCEPT if it is a century year
    #   (divisible by 100) that ISN'T divisible by 400.
    if Y < 100:
        return Y%4 == 0
    else:
        first = Y%4 == 0
        if Y%100 == 0:
            if Y%400 == 0:
                second = True
            else:
                second = False
        else:
            second = True
        return (first and second)

def indexToDate(date):
    date += 1
    #This corrects for the fact that January 1st is 0 days away, not Jan 0th
    
    daysAtMonthNorm = [0,31,59,90,120,151,181,212,243,273,304,334,365]
    daysAtMonthLeap = [0,31,60,91,121,152,182,213,244,274,305,335,366]
    if date < 0:
        print("Negative indicies not implemented.")
        raise NotImplementedError

    Y = 17
    while True:
        if isLeap(Y):
            if date > 366:
                date -= 366
                Y += 1
            else:
                break
        else:
            if date > 365:
                date -= 365
                Y += 1
            else:
                break

    if isLeap(Y):
        daysAtMonth = daysAtMonthLeap
    else:
        daysAtMonth = daysAtMonthNorm
        
    for i in range(len(daysAtMonth)):
        if date <= daysAtMonth[i]:
            date -= daysAtMonth[i-1]
            M = i
            break
    D = date
    
    return [M,D,Y]

def correctDate(A):
    #This returns a corrected date from something with the day off.
    #If you want 3 days after March 30th, pass in
    #   [4,31] - [4,32] - [4,33]    
    days = dateToIndex(A)
    date = indexToDate(days)
    return date

def yearGrowth(Y):
    #THIS IS A BAD FUNCTION AND SHOULD BE REWRITTEN OR NOT USED!!
    #Its intended purpose is to predict how much higher Y's zion visitation
    #   will be than Y-1's.
    #Returns float multiplier.
    if Y == 20:
        growth = 1.04
    elif Y == 19:
        growth = 1.1
    elif Y == 18:
        growth = 0.95
    elif Y == 17:
        growth = 0.97
    else:
        growth = 1
    return growth

def extractSpreadsheet(file,cols = False):
    #Excel file to Grid object with only cols variables.
    df = pd.read_excel(file)
    if cols:
        return exclusiveDataframeToGrid(df,cols)
    else:
        return dataframeToGrid(df)
    
def dataframeToGrid(df):
    dfl = df.values.tolist()
    return Grid(dfl)

def exclusiveDataframeToGrid(Data,cols):
    #Note: If you name every column in the spreadsheet, it seems to change
    #   everything to NaN`s
    df = pd.DataFrame(Data, columns=cols)
    dfl = df.values.tolist()
    return Grid(dfl)


def dayOfWeekMult(date):
    #Returns the multiplier for the given day of week.
    #This "multiplier" is based off of the average (Monday/Ave_of_week) value
    #   for all weeks in the spreadsheet. The values have been calculated in
    #   the spreadsheet and manually imported here.

    #This function should be rewritten with a "Find day of week" function, then
    #   finding the multiplier from that day.
    
    if type(date) == list:
        date = dateToIndex(date)

    day = date%7
    #January 1st of 2017 was a monday. That means a remainder of 1 == Tues, etc.
    #       Tuesday Wednesday Thursday Friday  Saturday Sunday   Monday
    return [0.99504,0.9447822,0.925257,0.91564,0.998275,1.134217,1.1269][day]


def dateRange(date,left,right):
    #Expands one day into a list with _left_ days to the left,
    #   and _right_ to right
    #Returns whatever method of representing the date you give it.
    if type(date) == list:
        [M,D,Y] = date
        days = []
        for i in range(D-left,D+right+1):
            days.append(correctDate([M,i,Y]))
            #Only iterate over the day. correctDate() takes care of the details.
        return days
    else:
        days = []
        for i in range(date-left,date+right+1):
            days.append(i)
        return days

#UNDOCUMENTED!
def scatter(x,y):
    data = [x,y]
    data = Grid(data)
    data.transpose()
    points = data.getData()
    df = pd.DataFrame(points,columns = ["X","Y"])
    ax1 = df.plot.scatter(x="X",y="Y")
    plt.show()

#UNDOCUMENTED!
def scatterColor(x,y,results,colors):
    data = [x,y,results]
    data = Grid(data)
    data.transpose()
    points = data.getData()
    df = pd.DataFrame(points,columns = ["X","Y","R"])
    ax1 = df.plot.scatter(x="X",y="Y",c="R",colormap = colors)
    plt.show()

def line(x,y):
    data = [x,y]
    data = Grid(data)
    data.transpose()
    points = data.getData()
    df = pd.DataFrame(points,columns = ["X","Y"])
    ax1 = df.plot.line(x="X",y="Y")
    plt.show()
    
class Grid:
    def __init__(self,data):
        self.mData = data.copy()
    def print(self):
        print(self.mData)
    def printCol(self,col):
        for i in range(self.getHeight()):
            print(self.mData[i][col])
    def getData(self):
        return self.mData
    def setData(self,data):
        self.mData = data.copy()
    def getVal(self,row,col):
        return self.mData[row][col]
    def setVal(self,row,col,val):
        self.mData[row][col] = val
    def getHeight(self):
        return len(self.mData)
    def getLength(self):
        return len(self.mData)
    def getWidth(self):
        return len(self.mData[0])

    def getVals(self,row,variables,pedantic = False):
         #Returns any variables you want from a specific date's row.
        #Variables take the form of column indicies.
        #Date can either be D/M/Y or index

        #This function silently errors if the value it tries to access is a 0
        #   because of missing data. Due to variables which CAN be 0, such as
        #   rainfall or temperature, I've elected to not have it bark at you.
        #   If you want that anyway, enable pedantic.

        if type(row) == list:
            date = dateToIndex(row)
        else:
            date = row
        if date > self.getHeight()-1:
            print("Invalid date",row)
            return False

        outs = []
        for variable in variables:
            x = self.getVal(date,variable)
            if pedantic and x == 0:
                print("Caution: value",date,variable,"is 0.")
            outs.append(x)
        return outs


#UNDOCUMENTED!
    def splitAtColVal(self,col,val):
        left = []
        right = []
        for i in range(self.getHeight()):
            if self.mData[i][col] < val:
                left.append(self.mData[i])
            else:
                right.append(self.mData[i])
        left = Grid(left)
        right = Grid(right)
        return [left,right]

    def transpose(self):
        self.mData = [[self.mData[j][i] for j in range(self.getHeight())] for i in range(self.getWidth())]
    
    def getMinimum(self,col):
        #Minimum value in column
        i = 0
        while True:
            m = self.getVal(0,col)
            if m != "?":
                break
            i += 1
            
        for i in range(1,self.getHeight()):
            if self.getVal(i,col) != "?" and m > self.getVal(i,col):
                m = self.getVal(i,col)
        return m

    def extractRowMin(self,col):
        #Returns the row that column "col"'s minimum value exists at.
        i = 0
        while True:
            m = self.getVal(0,col)
            if m != "?":
                break
            i += 1

        index = 0
        for i in range(1,self.getHeight()):
            if self.getVal(i,col) != "?" and m >= self.getVal(i,col):
                m = self.getVal(i,col)
                index = i
        return self.getData()[index]

    
    def getMaximum(self,col):
        #Maximum value in column
        i = 0
        while True:
            m = self.getVal(0,col)
            if m != "?":
                break
            i += 1
        for i in range(1,self.getHeight()):
            if self.getVal(i,col) != "?" and m < self.getVal(i,col):
                m = self.getVal(i,col)
        return m

    def extractRowMax(self,col):
        #Returns the row that column "col"'s minimum value exists at.
        i = 0
        while True:
            m = self.getVal(0,col)
            if m != "?":
                break
            i += 1

        index = 0
        for i in range(1,self.getHeight()):
            if self.getVal(i,col) != "?" and m <= self.getVal(i,col):
                m = self.getVal(i,col)
                index = i
        return self.getData()[index]
