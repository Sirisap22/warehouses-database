from .CollectionService import CollectionService
from enum import Enum
from datetime import datetime, timedelta
import dateutil.parser

class HistoryAction(Enum):
    def __str__(self):
        return (self.value)
    INSERT = 'insert'
    EXPORT = 'export'

class HistoryService(CollectionService):
    def __init__(self, name, repoPath, jsonSize=100, threadSize=10, CacheLength=10000):
        super().__init__(name, repoPath, jsonSize, threadSize, CacheLength)

    def addLog(self, data):
        year, month, date = data["date"].split("T")[0].split("-")
        super().addDoc(data, tags=[data["barcode"], f"Data_{date}", f"Month_{month}", f"Year_{year}", f"{data['action']}"])

    def getHistory(self, tags={None}):
        docs = super().where("id","#",True,tags=tags)
        self.quickSortByDate(0, len(docs)-1, docs)
        docs.reverse()
        return docs

    def searchBydate(self, date=None, month=None, year=None, tags=[]):
        tags += [f"Date_{date}"] if date is not None else []
        tags += [f"Month_{month}"] if month is not None else []
        tags += [f"Year_{year}"] if year is not None else []
        docs = super().where("id","#",True, tags=tags)
        self.quickSortByDate(0, len(docs)-1, docs)
        docs.reverse()
        return docs

    def searchByPeriod(self, start, end, tags=None):
        startDate = self.strToDate(start)
        endDate = self.strToDate(end)
        if startDate > endDate:
            return []

        docs = super().where("id","#",True,tags=tags if (tags is not None and tags != []) else {None})

        # quick sort
        self.quickSortByDate(0, len(docs)-1, docs)

        startIdx = self.findFirstGreaterOrEqual(docs, startDate)
        endIdx = self.findFirstLessOrEqual(docs, endDate)

        if startIdx == -1:
            return []
        if endIdx == -1 or endIdx + 1 == len(docs):
            return docs[startIdx:]
        res = docs[startIdx: endIdx+1]
        res.reverse()
        return res
    
    def findFirstGreaterOrEqual(self, arr, date):
        low = 0
        high = len(arr)-1
        ans = -1
        while low <= high:
            mid = low + (high-low)//2

            if self.strToDate(arr[mid]['date']) < date:
                low = mid + 1
            else:
                ans = mid
                high = mid - 1
        
        return ans


    def findFirstLessOrEqual(self, arr, date):
        low = 0
        high = len(arr)-1
        ans = -1
        while low <= high:
            mid = low + (high-low)//2

            if self.strToDate(arr[mid]['date']) > date:
                high = mid - 1
            else:
                ans = mid
                low = mid + 1

        return ans
        

    def strToDate(self, s):
        return dateutil.parser.parse(s)

    def partition(self, start, end, array):
        pivotIndex = start 
        pivot = array[pivotIndex]
        while start < end:

            while start < len(array) and self.strToDate(array[start]['date']) <= self.strToDate(pivot['date']):
                start += 1
            while self.strToDate(array[end]['date']) > self.strToDate(pivot['date']):
                end -= 1
            
            if(start < end):
                array[start], array[end] = array[end], array[start]

        array[end], array[pivotIndex] = array[pivotIndex], array[end]
        
        return end
      

    def quickSortByDate(self, start, end, array):
        if (start < end):
            p = self.partition(start, end, array)

            self.quickSortByDate(start, p - 1, array)
            self.quickSortByDate(p + 1, end, array)
