list1= [[['Peter'], "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"],[['ten'], ['11'], "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"] ]

list2= [[['Peter'], "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"],[['ten'], ['11'],['fourty'], "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"] ]

from collections import Counter
list1 = [[1,2,3],[4,5,6],[7,8,9]]
list2 = [[1,3, 2],[4,5,6],[7,9,8]]
print(list1[0])
print(set(list1[0])==set(list2[0]))
