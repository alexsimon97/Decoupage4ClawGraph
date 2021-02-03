import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter


DISPLAY_CONST = 0.2

'''
Asks the user to enter the number of intervals and then for each interval enter the beginning and the end of it
An interval is a list of two values : its beginning and its end
collection is the collection of all the intervals, it is a list of intervals

def enter_values():
	collection = []
	nbInterval = int(input("Number of intervals : "))
	for i in range(nbInterval):
		interval = []
		print("Interval "+ str(i+1) + " :")
		begin = int(input("Beginning of the interval : "))
		end = int(input("End of the interval : "))
		interval.append(begin)
		interval.append(end)
		collection.append(interval)
	return collection
'''	

def read_values(endpoints):
	collection = []
	print(endpoints)
	for i in range(1,len(endpoints)//2+1):
		interval = []
		begin = endpoints.index(i)
		end = endpoints.index(i,begin+1)
		interval.append(begin)
		interval.append(end)
		collection.append(interval)
	return collection

'''
Plots the intervals in collection
'''
def plot(collection):

	fig, ax = plt.subplots()
	for i in range(len(collection)):
		interval = collection[i]
		intervalNumber = i+1
		begin = interval[0]
		end = interval[1]
		ax.hlines(y=intervalNumber, xmin=begin, xmax=end, linewidth=2, color='r')
		ax.text((end+begin)/2,intervalNumber+len(collection)/100,str(intervalNumber))
		if(len(interval)>2):
			begin = interval[2]
			end = interval[3]
			ax.hlines(y=intervalNumber, xmin=begin, xmax=end, linewidth=2, color='r')
			ax.text((end+begin)/2,intervalNumber+len(collection)/100,str(intervalNumber))

	plt.show(block=False)

	
'''
Cuts an interval from cutBegin to cutEnd
The cut interval is now a list a 4 values, its beginning, the beginning of the cut, the end of the cut and its end
'''
def cut_interval(interval,cutBegin,cutEnd):
	
	intervalEnd = interval[1]
	interval[1] = cutBegin
	interval.append(cutEnd)
	interval.append(intervalEnd)
	#print(interval)
	
	
'''
Checks if there is a three-claw
If True, then it also returns the first 2 disjoint intervals intersecting the considered interval and a list of intervals causing a three-claw
'''
def has_three_claw(interval,collection):
	
	#We first keep the intervals whose end is in the considered interval
	candidates = []
	for i in range(len(collection)):
		potentialInterval = collection[i]
		if(potentialInterval[1] >= interval[0] and potentialInterval[1] < interval[1]):
			candidates.append(potentialInterval)
	if not candidates:
		#print("Problem first interval")
		return False,[],[],[]
	
	#We then choose the interval whose end is minimal
	first_interval = candidates[0]
	for i in range(len(candidates)):
		if(candidates[i][1] < first_interval[1]):
			first_interval = candidates[i]
	#print(first_interval)
	
	#Secondly, we keep the intervals beginning after the end first_interval but ending before the end of the considered interval
	candidates = []
	for i in range(len(collection)):
		potentialInterval = collection[i]
		if(potentialInterval[0] > first_interval[1] and potentialInterval[1] < interval[1]):
			candidates.append(potentialInterval)
	if not candidates:
		#print("Problem second interval")
		return False,[],[],[]
		
	#We then choose the interval whose end is minimal
	second_interval = candidates[0]
	for i in range(len(candidates)):
		if(candidates[i][1] < second_interval[1]):
			second_interval = candidates[i]
	
	#print(second_interval)
	#Finally, we check if there are some interval beginning after the end of second_interval but that still intersects the considered interval
	candidates = []
	for i in range(len(collection)):
		potentialInterval = collection[i]
		if(potentialInterval[0] > second_interval[1] and potentialInterval[0] <= interval[1]):
			candidates.append(potentialInterval)
	
	if not candidates:
		#print("No 3-claw")
		return False,[],[],[]
	
	
		
	return True, first_interval,second_interval,candidates
	
'''
Checks if there is a four-claw
If True, it then also returns 5 intervals intersecting the considered interval such that:
first_interval and second_interval and breaker is the first triple of disjoint intervals 
breaker_interval thus causes the considered interval to break
third_interval is the interval that causes the considered interval to resume (may be equal to breaker_interval)
fourth_interval is the interval whose beginning is maximal
first, second, third and fourth intervals are four disjoint intervals
'''
def has_four_claw(interval,collection):
	
	check_three_claw, first_interval, second_interval, candidates = has_three_claw(interval,collection)
	if(check_three_claw==False):
		return False,[],[],[],[],[]
	
	#candidates is a list of all intervalls beginning after second_interval that still intersect the considered interval.
	#breaker_interval is therefore the one that begins the first among them
	breaker_interval = candidates[0]
	for i in range(len(candidates)):
		if(candidates[i][0] < breaker_interval[0]):
			breaker_interval = candidates[i]
	
	#fourth_interval is therefore the one that begins the last among the candidates
	fourth_interval = candidates[0]
	for i in range(len(candidates)):
		if(candidates[i][0] > fourth_interval[0]):
			fourth_interval = candidates[i]
	
	#print(fourth_interval)
	#We look for an interval that begins after the end of second_interval but ends before the beginning of fourth_interval 
	candidates = []
	for i in range(len(collection)):
		potentialInterval = collection[i]
		if(potentialInterval[1] < fourth_interval[0] and potentialInterval[0] > second_interval[1]):
			candidates.append(potentialInterval)
			
	#if none exists then there was a 3-claw
	if not candidates:
		print("There is a 3-claw but not a 4-claw")
		return False,[],[],[],[],[]
		
	#else, we choose the one whose end is minimal as it will force the considered interval to resume
	third_interval = candidates[0]
	for i in range(len(candidates)):
		if(candidates[i][1] < third_interval[1]):
			third_interval = candidates[i]
			
			
	#We check if there is an interval between the third and the fourth: in this case there is a 5-claw
	for i in range(len(collection)):
		potentialInterval = collection[i]
		if(potentialInterval[1] < fourth_interval[0] and potentialInterval[0] > third_interval[1]):
			print("5-claw")
			return False,[],[],[],[],[]
		
		
	
	return True, first_interval, second_interval, breaker_interval, third_interval , fourth_interval
#def decide_cut(collection):


'''
Cuts the intervals right before the beginning breaker_interval and resumes them right before the end of third_interval
'''
def cut_first_time(collection):
	memory = []
	for interval in collection:
		check, first_interval, second_interval, breaker_interval, third_interval , fourth_interval = has_four_claw(interval,collection)
		
		if(check==True):
			l = []
			#l.append(check)
			l.append(interval)
			l.append(breaker_interval[0])
			l.append(third_interval[1])
			memory.append(l)
		#	cut_interval(interval,breaker_interval[0]-DISPLAY_CONST, third_interval[1]-DISPLAY_CONST)
	
	for l in memory:
		#if(l[0] == True):
		cut_interval(l[0],l[1]-DISPLAY_CONST,l[2]-DISPLAY_CONST)
		


'''
Create allIntervals : a list of all intervals after cutting
'''
def collect_all_intervals(collection):
	allIntervals = []
	for interval in collection:
		leftInterval = [interval[0],interval[1]]
		allIntervals.append(leftInterval)
		if(len(interval)>2):
			rightInterval = [interval[2],interval[3]]
			allIntervals.append(rightInterval)
	return allIntervals
	
'''
Checks if there is a fake-claw : a three-claw after cutting
If True, it returns the three disjoint intervals responsible of the fake-claw
'''	
def has_fake_claw(allIntervals):
	for interval in allIntervals:
		check_three_claw, first_interval, second_interval, third_interval = has_three_claw(interval,allIntervals)
		if(check_three_claw):
			return True, first_interval, second_interval, third_interval
	return False, [], [], []
		
'''
Rectifies the cut so the fake-claw disappears
It first looks for the corresponding interval in collection (the theory states it can only be the right part of the interval) and extends it to the left
'''
def rectify_cut(collection,first_interval,second_interval):
	for interval in collection:
		if(len(interval)>2):
			
			if(interval[2]==second_interval[0] and interval[3]==second_interval[1]):
				#print(interval[2])
				#print(interval[3])
				interval[2] = first_interval[1]
		
	


'''
Cuts the intervals and checks for all the fake-claws
If there are some, rectifies it and checks again
If there are still some, the algorithm is wrong
'''
def can_be_cut(collection):
	

	cut_first_time(collection)
	allIntervals = collect_all_intervals(collection)
	check, first_interval, second_interval, third_interval = has_fake_claw(allIntervals)
	#print(first_interval)
	#print(second_interval)
	#print(third_interval)
	i=0
	#Once an interval is rectified it cannot cause problem anymore, so we cannot rectify more times than the number of intervals in total
	while(check and i<len(collection)):
		#print("Problem")
		rectify_cut(collection,first_interval, second_interval)
		allIntervals = collect_all_intervals(collection)
		check, first_interval, second_interval, third_interval = has_fake_claw(allIntervals)
		
		i = i+1
		
	
	if(check):
			print("Real Problem")
			print(first_interval)
			print(second_interval)
			print(third_interval)
			
			return False
			
		#else:
			#print("Solved")

	return True
	

def output_equivalent_interval_graph(collection):
	allIntervals = collect_all_intervals(collection)
	
	l = []
	for i in range(len(allIntervals)): #IMPORTANT : WE CANNOT MERGE THE TWO FOR LOOPS AND WE NEED THE SORT TO BE IN PLACE
		u = [i+1,allIntervals[i][0]]
		l.append(u)
		
	for i in range(len(allIntervals)):
		v = [i+1,allIntervals[i][1]]
		l.append(v)
	l.sort(key=lambda x: x[1])
	lineToWrite = ""
	for i in range(len(l)-1):
		lineToWrite += str(l[i][0]) + " "
	lineToWrite += str(l[len(l)-1][0]) + "\n"
	return lineToWrite
	
	
		

	
def main():
	#collection  = enter_values()
	file = open(sys.argv[1], "r")
	fileToWriteIn = open("filesWithAllIntervalGraphs/IntervalGraphs12VerticesCUT.txt", "w")
	for line in file:
		endpoints = line.split()
		endpoints = [ int(x) for x in endpoints ]
		collection = read_values(endpoints)
		#plot(collection)
		#print(collection)
		if(can_be_cut(collection)==False):
			plot(collection)
			plt.show()
			break
		fileToWriteIn.write(output_equivalent_interval_graph(collection))
	#plot(collection)
	#plt.show()

if __name__ == "__main__":
	main()
   



    
    




