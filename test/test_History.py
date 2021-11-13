def findFirstGreaterOrEqual(arr, target):
        low = 0
        high = len(arr)-1
        ans = -1
        while low <= high:
            mid = low + (high-low)//2

            if arr[mid] < target:
                low = mid + 1
            else:
                ans = mid
                high = mid - 1

        return ans

def findFirstLessOrEqual(arr, target):
        low = 0
        high = len(arr)-1
        ans = -1
        while low <= high:
            mid = low + (high-low)//2

            if arr[mid] > target:
                high = mid - 1
            else:
                ans = mid
                low = mid + 1

        return ans
arr = sorted([3, 8, 1, 4, 5, 6])
print(arr[findFirstGreaterOrEqual(arr, 5)])
print(arr[findFirstLessOrEqual(arr, 5)])