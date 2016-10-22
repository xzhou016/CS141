import math
import copy
import re
import sys
import timeit

class Point :
    def __init__(self, x_val, y_val):
        self.x = x_val
        self.y = y_val

    def __repr__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

def Read_Points_From_Command_Line_File():
    points = []
    number_of_args = len(sys.argv)
    file = open(sys.argv[1],"r")

    for line in file:
        line.strip()
        x_y = line.split(" ")
        points.append(Point(float(x_y[0]),float(x_y[1])))

    return points

def Write_to_File(filename, s):
    output = open(filename ,'w')
    output.write(str(s))
    output.write('\n')

#distance formula
def Distance_Form(pnt1 , pnt2):
	dist = math.sqrt(math.pow(pnt1.x - pnt2.x, 2) + math.pow(pnt1.y - pnt2.y,2))
	return dist

#brute force method function
def Brute_Force(pnts_list):
	min = Distance_Form(pnts_list[0],pnts_list[1])
	#for loop to find shortest dist
	for p1 in pnts_list:
		for p2 in pnts_list:
			temp = Distance_Form(p1,p2)
			if p1 != p2:
				if temp < min:
					min = temp
			else:
				continue

	return min

def Div_Conq(pnts_list):

	#base case
	if(len(pnts_list) <= 1):
		return 100000.0
	elif(len(pnts_list) == 2):
		return Distance_Form(pnts_list[0] , pnts_list[1])

	#calculate min in left and right side
	L = pnts_list[:len(pnts_list)/2]
	R = pnts_list[len(pnts_list)/2:]
	l_min = Div_Conq(L)
	r_min = Div_Conq(R)
	min_val = min(l_min,r_min)

    # print "Left d : %f, Right d : %f" %(l_min, r_min)
    # print "init minimum_d: %f" % min_val
    # print '\n'

	center_val = pnts_list[len(pnts_list)/2].x

	M = copy.deepcopy(pnts_list)
	i = 0
	#construct center list
	for curr in pnts_list:
		if(center_val - min_val > curr.x  ) :
			del M[i]
			i=i-1
		elif(center_val + min_val < curr.x) :
			del M[i]
			i=i-1
		i = i+1

	#sort by y
	M = sorted(M, key = lambda point: point.y)

	#final comparision
	k = 0
	for pnt in M:
		j  = 1
		while  j < 8:
			if(k + j >= len(M)):
				break;
			temp = Distance_Form(M[k],M[k + j])
			if(temp < min_val):
				min_val = temp
			j = j + 1
		k = k + 1

	return min_val



list = Read_Points_From_Command_Line_File()

# start = timeit.default_timer()
# nearest  = Brute_Force(list)
# print "Brute Force: %f" % nearest
# stop = timeit.default_timer()
# print stop - start

#found online, used to sort by x value
list = sorted(list, key = lambda point: point.x)

start = timeit.default_timer()
nearest = Div_Conq(list)
print "Divide and Conquere: %f" % nearest
stop = timeit.default_timer()
print stop - start

fname = sys.argv[1]
fname = fname[:-4]

Write_to_File(fname + "_distance.txt", nearest)
