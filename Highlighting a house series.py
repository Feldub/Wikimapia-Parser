house_desc =['Пятиэтажный шестиподъездный панельный жилой дом серии 111-121.1-092.83.','Пятиэтажный шестиподъездный панельный жилой дом серии 111-121-1','Пятиэтажный пятиподъездный панельный жилой дом серии КПД-4570.']
house_type=[]

for house in house_desc:
    #Checking if the word 'серии' is in the original list and adding the result
    if 'серии' in house:
        house_split = house.split()
        house_type.append(house_split[house_split.index('серии') + 1].split('.')[0])
    #Checking if the word 'серия' is in the original list and adding the result
    elif 'серия' in house:
        house_split = house.split()
        house_type.append(house_split[house_split.index('серия') + 1].split('.')[0])
    else:
        pass

print(house_type)