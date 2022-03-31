import random
import numpy as numpy
from codetiming import Timer
import scipy.optimize as optimization

'''The function creates a registry of the clients, to whom we can sell a specific quantity of product, for a given price. An integer is the only parameter
of the create_registry() function, and it is used to create a list of integers which symbolises the quantity of the batches that each client can buy. 
The list of these quantities is obtained by exploiting generators and a variable i taking values from 0 to n. By the difference n-i, are obtained all the 
integers from 0 to n. The resulting list, named quantities, will be in descending order, since we start from i = 0, and n-0=n, using [::-1] we invert it.
The next step performed by the function, is creating an empty dictionary, called registry{}, which contains ('units of product : price offered') pairs.
To generate the price offered by a given buyer for a quantity of product, random.randint function of random module is applied, in a range that the
price of the batches quantity is not smaller than 4 times the quantity, neither bigger than 6 times the quantity. The price value is immediately assigned
to the corresponding quantity in the registry. Registry is then returned in the end of the execution of the function.  '''
def create_registry(n):
    quantities = [n-i for i in range(0, n+1)][::-1]
    registry = {}
    for quantity in quantities:
        registry[quantity] = random.randint(quantity*4, quantity*6)
    return registry

'''This is the central function of the whole program, which provides a Dynamic Programming based result. The function takes as input the number of the 
batches planned to be sold and the registry we obtained in the create_registry() function, and its aim is to return a list which inside itself contains the list
the selling plan and an integer recording the maximal revenue we can profit. 
Creation of optimal_solutions is the next step. This dictionary is supposed to store the best plan to sell any quantity of product in the format 
'quantity of product : [(quantity, price offered), revenue]'. The plan for selling 0 product is already part of this dictionary for a ceratain reason:
every time we compute the plan for a quantity of product n, we base the solution in the plan of selling n-1 product. So overall, the whole problem, since it is 
solved using a Dynamic Programming approach, it will divide the problem being considered in small subporblems whose solutions are known and then used to compute 
the result of the main problem. Important local variables of the function are Max_revenue which stores the highest revenue we can obtain by selling
n batches and final_plan list which stores the final plan of selling n batches.
For any number of batches, we want to compute the Max_revenue as well as the plan, while we already know the best plan for n-i batches. For facilitating
the orientation of the reader the variable that keeps track of the number of batches which have been already sold in
optimized way, is named optimized. This is the difference of the number of total batches quantity we have to sell, and the unsold_batches.
For the number of optimized batches, we can search on the optimal_solutions dictionary, by using optimized as a key, to return the maximal
revenue which can be obtained by their best selling plan. The plan to sell n batches, the variable named current_value, keeps track of the maximal revenue of 
every possible plan. It consists on the sum of the money obtained by selling plan of 'optimized' batches, with the price we can sell the unsold_batches, 
found associated to the key = unsold_batches, on the registry given as a parameter to the selling_plan() function. 
If the current_value is bigger than the Max_revenue, we update the Max_revenue value, assigning to it the value of current_value. At the same time, to the
 best_plan, which in the begining of the for loop is an empty list, is appended as a tuple the number of the unsold_batches and the price we can sell them, found
as a value in teh registry. Setting the condition in teh following line, does not allow the function to append on teh solution list the plan to sell 0 batches, 
which has no purpose on the result, rather than computational importance. If the plan of unsold_batches does not involve selling (0 batches, zero money units), then 
the plan is added from the optimal_solutions, to the best plan. In the end of the scope, the final_plan is set to be the best_plan. 
Every time that the second for loop is executed, the best plan is empty,  if the current_value > Max_revenue, the Max_vlaue gets updated, best_plan
gets filled and the final_plan assigned another list. In the end of the execution of this second loop, the optimal_solution dictionary will have a new key:value pair
'batches number:[final_plan, Max_revenue] format. So for every number of batches from 0 to n, we store theit best selling plan in the optimal_solutions dictionary, 
so they can be easily accessed when needed for computation. 
The function will return the value of this dictionary associated to the number of batches to be sold 'n', so the best selling plan for this quantity.'''
def selling_plan(n, registry):
    optimal_solutions = {0:[(0, registry[0]), registry[0]]}
    for batches in range(1, n+1):
        Max_revenue = 0
        final_plan = []
        for unsold_batches in range(1, batches+1):
            best_plan = []
            optimized = batches-unsold_batches
            current_value = optimal_solutions[optimized][1] + registry[unsold_batches]
            if current_value > Max_revenue:
                Max_revenue = current_value
                best_plan.append((unsold_batches, registry[unsold_batches]))
                if optimal_solutions[optimized][0] != (0, 0):
                    best_plan +=optimal_solutions[optimized][0]
                final_plan = best_plan
        optimal_solutions[batches] = [final_plan, Max_revenue]
    return optimal_solutions[n]

'''The function takes a list as a parameter and returns a dictionary, occurences_tracker, counting the occurence of every element of the list. The dictionary contains 'element:occurence'
pairs. The function considers every element of the list, if it is not in the dictionary already, it puts it as a key and assigns to it the value 1. Otherwise,
it if is already a key of hte dictionary, it will increase the values associated to it 1.
The importance of this function is that it will help in the fancy and correct display of the selling plan. For every element (qunatity, price offered), it will cound
its occurence and create key:value pairs. The value will tell us how many stocks of this quantity are sold.'''
def count_occurences(given_list):
    occurences_tracker = {}
    for element in given_list:
        if element not in occurences_tracker:
            occurences_tracker[element] = 1
        else:
            occurences_tracker[element]+=1
    return occurences_tracker


'''This function needed for the final representation of the plan. As an input takes the list of selling plan, the quantity to be sold and the occurences_tracker 
dictionary. Rather than just printing the sentences to be displayed, the function considers the occurrence of every (quantity, price offered) and based
on that and the quantity (i.e quantity singluar 1 or plural), it prints the grammatically correct sentence. Moreover, the selling plan is indexed [1], so it
returns which is the final revenue for the quantity to be sold.'''
def present_plan(plan : list, n, occurences_tracker):
    print('The selling plan in order to maximise the revenue for selling ',n, 'units of products, is: ')
    for occurences in occurences_tracker:
        if occurences_tracker[occurences]!=1:
            if occurences[0]==1:
                print(occurences_tracker[occurences], 'stocks of', occurences[0], 'batch each, to be sold for', occurences[1], 'units of money.' )
            else:
                print(occurences_tracker[occurences], 'stocks of', occurences[0], 'batches, to be sold for',
                      occurences[1], 'units of money.')
        else:
            if occurences[0] == 1:
                print(occurences_tracker[occurences], 'stock of', occurences[0], 'batch each, to be sold for', occurences[1],
                  'units of money each.')
            else:
                print(occurences_tracker[occurences], 'stock of', occurences[0], 'batches, to be sold for',
                      occurences[1], 'units of money.')
    print('The revenue: ', plan[1])

'''The function to test the selling_plan() function on a given values 1000 times and to return the average running time of all the tryouts exploiting codetiming module.
As the input of the selling_plan(), it is created a registry by create_registry() function based on the number of input the code is being tested.'''
def testDP(n: int, repetitions=1000) -> tuple:
    for i in range(repetitions):
        input = create_registry(n)
        with Timer(name='selling_plan', logger=None):
            selling_plan(n, input)
    return round(Timer.timers.mean('selling_plan'), 9)

'''For testing purposes, this function takes a list of inputs sizes, and it calls the testDP() for each of these inputs.The results of these runs, 
(the average running time for each input size) is stored in a list which is then returned by the function.'''
def Time_setsDP(input_list:list)-> list:
    l=list()
    for input in input_list:
        result=testDP(input)
        l.append(result)
    return l

'''This function takes the input list given to Time_setsDP functions, as well as its result, to print pairs of (input size, average running time), 
providing so the coordinates to be inserted in the graph.'''
def print_pairs(value_list, time_list):
    for (n, t) in zip(value_list, time_list):
        print((n,t), end='')

'''Testing function, which considers the timing_list and value_list to define the coenficients of the proposed function representing 
the Dynamic Programming based function, selling_plan().'''
def polynomial(x, a, b):
    return a * numpy.power(x, 2)+b

if __name__ == '__main__':
    #n = 10
    #D= (create_registry(n))
    #plan = selling_plan(n, D)
    #print(plan)
    #occurences_tacker = count_occurences(plan[0])
    #present_plan(plan, n, occurences_tacker)
    #print(create_registry(n))
    #print(count_occurences(plan[0]))
