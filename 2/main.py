import random

# def sort(arr):
#     n = len(arr)
#     for i in range(n):
#         for j in range(0, n-i-1):
#             if arr[j] > arr[j+1]:
#                 arr[j], arr[j+1] = arr [j+1], arr[j]
#     return arr

# arr = [654, 41, 213,1,676,3243]
#arr = [random.randint(0,1000) for _ in range(20)]
#arr1 = [random.randint(1,1000) for _ in range(20)]
#print(arr)
#print(arr1)


# def bubble_sort(arr):
#     n=len(arr)
#     for i in range(n):
#         for j in range(0, n-i-1):
#             if arr[j]>arr[j+1]:
#                 t = arr[j]
#                 arr[j] = arr[j+1]
#                 arr[j+1] = t
#     print(arr)

# bubble_sort(arr)

#1 цикл запускается n раз
#2 цикл запускается n-i-1 раз
#Big-O: O(n^2)

# def selection_sort(arr):
#     n = len(arr)
#     for i in range(n):
#         min_index = i
#         for j in range(i+1,n):
#             if arr[j] < arr[min_index]:
#                 min_index = j
#         t = arr[i]
#         arr[i] = arr[min_index]
#         arr[min_index] = t
#     print(arr)
#     return arr

# a = selection_sort(arr)
#b = selection_sort(arr1)

#1 цикл запускается n раз
#2 цикл запускается n-i-1 раз
#Big-O: O(n^2)

# def bingo(arr):
    
#     max = len(arr)-1
#     value = arr[max]
#     for i in range(max-1,-1,-1):
#         if value<arr[i]:
#             value = arr[i]
    
#     while max and arr[max]==value:
#         max -= 1
    
#     while max:
#         newValue = value
#         value = arr[max]
        
#         for i in range(max-1,-1,-1):
#             if arr[i]==newValue:
#                 arr[i],arr[max] = arr[max], arr[i]
#                 max-=1
#             elif arr[i]>value:
#                 value = arr[i]
#         while max and arr[max]==value:
#             max-=1
#     print(arr)

# bingo(arr)

# def pancake(arr):
    
#     if len(arr)>1:
        
#         for i in range(len(arr),1,-1):
#             maxindex = i - 1
#             for s in range(i):
#                 if arr[s]>=arr[maxindex]:
#                     maxindex = s
#             if maxindex +1!=i:
#                 if maxindex !=0:
#                     arr[:maxindex+1] = reversed(arr[:maxindex+1])
#             arr[:i] = reversed(arr[:i])
#     print(arr)

# pancake(arr)

#n+(n-1)+(n-2)+...+2
#(n(n+1))/2 - 1
#n^2/2 + n/2 - 1>O(n^2+3n)

# def ctrlv(arr):
#     for i in range(1,len(arr)):
#         for j in range(i, 0, -1):
#             if arr[j-1]>arr[j]:
#                 t = arr[j]
#                 arr[j] = arr[j-1]
#                 arr[j-1] = t
#             else:
#                 break
#     print(arr)

# ctrlv(arr)

# def bin_search(arr,k_ind):
#     k = arr[k_ind]
#     left = 0
#     right = k_ind - 1
#     while left<=right:
#         mid = (left+right)//2
#         if arr[mid]>k:
#             right = mid-1
#         else:
#             left = mid+1
#     return left
    
# def insertion_binary(arr):
#     for i in range(1,len(arr)):
#         k = arr[i]
#         pos = bin_search(arr,i)
#         for j in range(i, pos, -1):
#             arr[j] = arr[j-1]
#         arr[pos] = k
#     print(arr)
    
# insertion_binary(arr)

def make_array(n):
    if n ==1:
        return [random.randint(1, 1000)]
    return make_array(n-1) + [random.randint(1, 1000)]

# def merge(a, b):
#     i = 0
#     j = 0
#     res = []
    
#     while i < len(a) and j < len(b):
#         if a[i] < b[j]:
#             res.append(a[i])
#             i += 1
#         else:
#             res.append(b[j])
#             j += 1
#     res += a[i:]+b[j:]
#     #print(res)
#     return res

# # merge(a, b)

# def split_and_merge(arr):
#     mid = len(arr)//2
#     a = arr[:mid]
#     b = arr[mid:]
    
#     if len(a)>1:
#         a = split_and_merge(a)
#     if len(b)>1:
#         b = split_and_merge(b)
#     return merge(a,b)

arr = make_array(15)
print(arr)

# print(split_and_merge(arr))

def quick_sort(data):
    if len(data) > 1:
        x = data[random.randint(0, len(data) - 1)]
        low = [u for u in data if u < x]
        eq = [u for u in data if u == x]
        hi = [u for u in data if u > x]
        data = quick_sort(low) + eq + quick_sort(hi)
    print(data)
    return data

print(quick_sort(arr))