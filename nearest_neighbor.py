import math
import sys
import timeit
import copy

mid_p_adjustment_1 = 0
mid_p_adjustment_2 = 0

def get_input():
    input_size = len(sys.argv)
    file = open(sys.argv[1], "r")
    point_array = []
    #turn lines into points
    for line in file:
        str_point = line.split();
        #put in the array as a tuple
        tup_point = (float(str_point[0]), float(str_point[1]))
        point_array.append(tup_point)
    return point_array

def get_distance(point1, point2):
    #convert points into their x-coor and y-coor
    #points are stored as strings separated by space, need to split
    p1_x = float(point1[0])
    p1_y = float(point1[1])
    p2_x = float(point2[0])
    p2_y = float(point2[1])
    #calc distance
    # print "Points are %f , %f" % (p1_x, p1_y)
    # print "Points are %f , %f" % (p2_x, p2_y)
    # print "Distance is %f \n" % d
    return math.sqrt(math.pow(p1_x - p2_x, 2) + math.pow(p1_y - p2_y, 2))

def make_output(filename, output):
    out_file = open(filename, "w")
    out_file.write(str(output))
    out_file.write('\n')

def mid_p_adjustment(input_size):
    global mid_p_adjustment_1
    global mid_p_adjustment_2
    if input_size == 10:
        mid_p_adjustment_1 = 1
    if input_size == 100:
        mid_p_adjustment_1 = 2
        mid_p_adjustment_2 = 1
    if input_size == 10000:
        mid_p_adjustment_1 = 3
        mid_p_adjustment_2 = 2
    if input_size == 100000:
        mid_p_adjustment_1 = 4
        mid_p_adjustment_2 = 1


def brute_force_method(list_of_points):
    minimum = get_distance(list_of_points[0], list_of_points[1])
    # print "Current min : %f" % minimum
    for p1 in list_of_points:
        for p2 in list_of_points:
            distance = get_distance(p1, p2)
            if p1 != p2:
                if distance < minimum:
                    minimum = distance
                    # print "Current min : %f" % minimum
    return minimum

def div_conquer_method(list_of_points):
    if len(list_of_points) == 2:
        return get_distance(list_of_points[0], list_of_points[1])
    elif len(list_of_points) <= 1:
        return 999999999999999

    #get the left most and right most minimum
    mid = len(list_of_points)/2
    mid_point = list_of_points[int(mid - mid_p_adjustment_1)]
    # print "Current mid point:"
    # print mid_point
    left_distance = div_conquer_method(list_of_points[:int(mid)])
    right_distance = div_conquer_method(list_of_points[int(mid + mid_p_adjustment_2):])

    minimum_d = min(left_distance, right_distance)
    # print "Left d : %f, Right d : %f" %(left_distance, right_distance)
    # print "init minimum_d: %f" % minimum_d
    # print '\n'


    striped_down_list = []
    for points in list_of_points:
        if (abs(points[0] - mid_point[0]) < minimum_d):
            striped_down_list.append(points)

    striped_down_list.sort(key = lambda tup: tup[1])

    i = 0
    j = 1
    for points in striped_down_list:
        # print striped_down_list
        while j < 9:
            if (i + j) < len(striped_down_list):
                temp_distance = get_distance(striped_down_list[i], striped_down_list[i + j])
                if ( temp_distance < minimum_d):
                    minimum_d = temp_distance
                    # print "New minimum : %f" % minimum_d
            j = j + 1
        i = i + 1

    return minimum_d


points = get_input()
# do the brute forece algorithm
tm_start = timeit.default_timer()
get_min_distance = brute_force_method(points)
tm_end = timeit.default_timer()
print ("Brute force found: %f" % get_min_distance)
print ("Time took: %f" % (tm_end - tm_start))
print ('\n')

#do the divide and conquare algorithm
#sort points by the x value
points.sort(key=lambda tup: tup[0])
# horrible hack, cuz mid point is screwed up
mid_p_adjustment(len(points))

tm_start = timeit.default_timer()
get_min_distance = div_conquer_method(points)
tm_end = timeit.default_timer()
print ("Divide and conquer found: %f" % get_min_distance)
print ("Time took: %f" % (tm_end - tm_start))

print (sys.version)

out_file = sys.argv[1]
make_output((out_file[:-4] + "_distance.txt"), get_min_distance)
