import numpy as np
import pandas as pd
from numpy import linalg as LA
import math
import matplotlib.pyplot as plt

def dateToIndex(date):
    [M,D,Y] = date
    total = D-1

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
    #DO NOT ATTEMPT TO MODIFY MONTH OR YEAR!!
    #If you want 3 days after March 30th, pass in
    #   [4,31] - [4,32] - [4,33]    
    days = dateToIndex(A)
    date = indexToDate(days)
    return date

def yearGrowth(Y):
    #THIS IS A BAD FUNCTION AND SHOULD BE REWRITTEN!!
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
    
def dataframeToGrid(Data):
    dfl = df.value.tolist()
    return Grid(dfl)
def exclusiveDataframeToGrid(Data,cols):
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

    
def plotPCA(data,pca1,pca2):
    #Plots the two given eigenvectors onto a 2D matplotlib scatter plot.
    points = []
    for line in data.getData():
        x = 0
        for i in range(len(pca1)):
            x += pca1[i]*line[i]
        y = 0
        for i in range(len(pca2)):
            y += pca2[i]*line[i]
        points.append([x,y])
    df = pd.DataFrame(points,columns = ["PCA1","PCA2"])
    ax1 = df.plot.scatter(x='PCA1',y='PCA2')
    df.plot()
    plt.show()

def plotPCAColor(data,pca1,pca2,results):
    #This plots the data with the points colored by their corresponding
    #   values in results.
    #NOTE: results comes in a vector like [[t,h,i,s]]
    points = []
    for i in range(data.getHeight()):
        x = 0
        for j in range(len(pca1)):
            x += pca1[j]*data.getVal(i,j)
        y = 0
        for j in range(len(pca2)):
            y += pca2[j]*data.getVal(i,j)
        points.append([x,y,results[0][i]])
    df = pd.DataFrame(points,columns = ["PCA1","PCA2","Diagnosis"])
    ax1 = df.plot.scatter(x='PCA1',y='PCA2',c='Diagnosis',colormap = 'rainbow')
    plt.show()  

def numMap(val,L1,R1,L2,R2):
    #Maps a number between range 1 to range 2
    return ((val-L1)/(R1-L1))*(R2-L2) + L2

def covarianceMatrix(data):
    #Finds covariance matrix, useful for many statistical operations,
    #   namely finding eigenvalues/eigenvectors.
    #[Cov(0,0)   Cov(0,1)  ... Cov(0,n)]
    #[Cov(1,0)   Cov(1,1)        ...   ]
    #[  ...                ...         ]
    #[Cov(n,0)      ...        Cov(n,n)]
    width = data.getWidth()
    matrix = Grid([[()]*width for i in range(width)])
    for i in range(width):
        for j in range(width):
            #if matrix.getVal(i,j) == False:
            matrix.setVal(i,j,data.covariance(i,j))
            #matrix.setVal(j,i,matrix.getVal(i,j))
    return matrix

def eigen(cov,absolute = False):
    ##Calculates [Value, Vector] array
    #print(cov)
    A = np.array(cov)
    #data.print()
    val, vec = LA.eig(A)
    vectors = []
    for i in range(len(val)):
        vectors.append([val[i],list(vec[:,i])])
    ##If absolute, consider the absolute value of Value w/ negative vectors
    if absolute:
        for i in range(len(vectors)):
            if vectors[i][0] < 0:
                vectors[i][0] *= -1
                for j in range(len(vectors[i][1])):
                    vectors[i][1][j] *= -1
    ##Sort by greatest Eigenvalue
    ##  (The vectors with the greatest eigenvalue are often the most significant
    done = False
    while not done:
        done = True
        for i in range(len(vectors)-1):
            if vectors[i][0] < vectors[i+1][0]:
                vectors[i],vectors[i+1] = vectors[i+1].copy(),vectors[i].copy()
                done = False
    ##Transform eigenvector into its unit vector
    ##  (Eigenvectors don't care about magnitude, just direction.)
    for i in range(len(vectors)):
        size = 0
        for j in range(len(vectors[i][1])):
            size += vectors[i][1][j]**2
        size = math.sqrt(size)
        for j in range(len(vectors[i][1])):
            vectors[i][1][j] /= size
    return vectors

class Grid:
    def __init__(self,data):
        self.mData = data.copy()
    def sub(self,row,col,val): #Just by element!
        self.mData[row][col] -= val
    def add(self,row,col,val): #Just by element!
        self.mData[row][col] += val
    def print(self):
        print(self.mData)
    def printCol(self,col):
        for i in range(self.getHeight()):
            print(self.mData[i][col])
    def export(self,name):
        #This is for if you wanna write it to a file.
        return name + str(self.mData) + "\n"
    def getData(self):
        return self.mData
    def setData(Self,data):
        self.mData = data.copy()
    def getVal(self,row,col):
        return self.mData[row][col]
    def setVal(self,row,col,val):
        self.mData[row][col] = val
    def getHeight(self):
        return len(self.mData)
    def getWidth(self):
        return len(self.mData[0])

    def getVals(self,row,variables,pedantic = False):
         #Returns any variables you want from a specific date's row.
        #Variables take the form of column indicies.
        #Date can either be D/M/Y or index

        #This function silently errors if the value it tries to access is a 0
        #   because of missing data. Due to variables which CAN be 0, such as
        #   rainfall or temperature(F), I've elected to not have it bark at you.
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

    def include(self,ticket):
        #Reformats data to only include variables in ticket
        self.transpose()
        off = 0
        for i in range(self.getHeight()):
            if i not in ticket:
                self.mData.pop(i-off)
                off += 1
        self.transpose()

    def exclude(self,ticket):
        #Reformats data to exclude variables in ticket
        self.transpose()
        off = 0
        for i in range(self.getHeight()):
            if i in ticket:
                self.mData.pop(i-off)
                off += 1
        self.transpose()


    def smooth(self):
        #Replaces all unknowns with their column's average.
        #This is quite lazy, a better smoothing function is in order.
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                if self.mData[row][col] == "?":
                    self.mData[row][col] = self.getAverageCol(col)
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
    
    def getAverageCol(self,col):
        #Average value in column
        tot = 0
        ct = 0
        for line in self.mData:
            if line[col] != "?":
                tot += line[col]
                ct += 1
        if ct == 0:
            return 0
        return tot/ct
    
    def centerColumn(self,col):
        #Subtracts the average from every item in the column.
        #I don't recommend calling this alone, use center().
        ave = self.getAverageCol(col)
        for i in range(self.getHeight()):
            if self.getVal(i,col) != "?":
                self.sub(i,col,ave)       
    def center(self):
        #Subtracts the average from all items, centering the data about origin.
        #This is useful for statistical analysis.
        for i in range(self.getWidth()):
            self.centerColumn(i)
        
    def normalizeColumn(self,col,normalMin,normalMax,centered = True):
        #Centers column and re-maps it from normalMin to normalMax
        if centered:
            self.centerColumn(col)
        minimum = self.getMinimum(col)
        maximum = self.getMaximum(col)
        for i in range(self.getHeight()):
            if self.getVal(i,col) == "?":
                continue
            val = self.getVal(i,col)
            val = numMap(val,minimum,maximum,normalMin,normalMax)
            self.setVal(i,col,val)
    def normalize(self,normalMin,normalMax):
        #Centers and re-maps all data from normalMin to normalMax
        for i in range(self.getWidth()):
            self.normalizeColumn(i,normalMin,normalMax)

    def variance(self,col):
        #Finds statistical variance of a column
        return self.covariance(col,col)
    def covariance(self,axis1,axis2):
        #Finds statistcal relation between two columns.
        #If this value is positive, there is a positive correlation.
        # 0 = no correlation, - = anti-correlation.
        tot = 0
        ave1 = self.getAverageCol(axis1)
        ave2 = self.getAverageCol(axis2)
        for i in range(self.getHeight()):
            tot += (self.getVal(i,axis1)-ave1)*(self.getVal(i,axis2)-ave2)
        return tot/self.getHeight()

