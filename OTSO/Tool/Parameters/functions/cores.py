import psutil
import multiprocessing as mp
import numpy as np

class Cores:
   def __init__(self, Positions, CoreNum):
        self.CoreNum = CoreNum
        self.Positions = Positions
        self.CoreNames = []

        self.CheckCoreNum()
        self.CreateCoreList()
        self.SplitPositions()



   def CheckCoreNum(self):
           if(psutil.cpu_count(logical=False) < self.CoreNum):

              print("You have entered an invalid number of cores")
              print("You have " + str(psutil.cpu_count(logical=False)) + " and have tried to use " + str(self.CoreNum) + " cores")
              print("To ensure operational integrity of your computer OTSO will run using 2 less than the max cores available, with a minumum value of 1.")

              self.CoreNum = psutil.cpu_count(logical=False) - 2
              if self.CoreNum <= 0:
                  self.CoreNum = 1

   def CreateCoreList(self):
         i = 1
         while i <= self.CoreNum:
          string = "Core " + str(i)
          self.CoreNames.append(string)
          i += 1

   def SplitPositions(self):
         self.PositionSplit = np.array_split(self.Positions, self.CoreNum)

   def getCoreList(self):
         return self.CoreNames

   def getPositions(self):
         return self.PositionSplit