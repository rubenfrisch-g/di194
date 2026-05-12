# import datetime

# def minutes_lived(birthdate_str):
    
#     birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d")
    
#     now = datetime.datetime.now()
    
#     time_difference = now - birthdate
    
#     minutes = int(time_difference.total_seconds() / 60)
    
#     print(f"You have lived approximately {minutes} minutes.")

# from collections import Counter  
# list = [1,2,3,4,1,2,6,7,3,8,1,2,2]  
# answer=Counter()
# answer = Counter(list)  
# print(answer[2])  

# from collections import deque  
# #initialization
# list = ["a","b","c"]  
# deq = deque(list)  
# print(deq)  

# #insertion
# deq.append("z")  
# deq.appendleft("g")  
# print(deq)
# #removal
# deq.pop()  
# deq.popleft()  
# print(deq)

import collections

dictionary1 = { 'a' : 1, 'b' : 2 }  
dictionary2 = { 'c' : 3, 'b' : 4 }  
chain_Map = collections.ChainMap(dictionary1, dictionary2)  
print(chain_Map.maps)  