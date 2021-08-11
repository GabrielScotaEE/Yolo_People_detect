from itertools import chain

from torch._C import Size

# for id, pt in center_points.items():
#     print (id)
#     print (pt)



# test = center_points.get(0)
# if test is None:
#     print ('Boa!')
# else:
#     print ('No tiene!')


# rev_dict = {}
# for key, value in center_points.items():
#     rev_dict.setdefault(value, set()).add(key)
  
  
# output = set(chain.from_iterable(
#          values for key, values in rev_dict.items()
#          if len(values) > 1))
  
# # printing result
# print("resultant key", str(output))


# print(list(output))

center_points = {}
cx = (347 + 510) // 2
cy = (337 + 442) // 2
# center_points[0] = (cx, cy)
center_points[1] = (20, 30)
center_points[5] = (25, 17)
center_points[7]= (50, 40)
center_points[10]= (50, 40)
center_points[11] = (20, 30)
center_points[15] = (20, 30)


print('\n{}\n'.format(center_points))

print('{}\n'.format(center_points.items()))

flipped = {}
  
for key, value in center_points.items():
    
    if value not in flipped:
        flipped[value] = [key]
    else:
        flipped[value].append(key)
  
# printing result
print("final_dictionary", str(flipped))
cleaner_list = []

for repeated in flipped.values():
    if len(repeated)>1:
        
        repeated.pop(-1)
        
        for sep in repeated:
            cleaner_list.append(sep)
        
        
print(cleaner_list)            
for clean in cleaner_list:
    print (clean)