import random
import numpy as numpy
from codetiming import Timer
import scipy.optimize as optimization
import scipy
def input_number(number :int): #based on the given input, it creates a list containing integers, from 1 to the given integer number
    return list(random.sample(range(1, number+1), number))

def generate_d(n): #function to generate the dictionary, containing "the assigned no of the object : weight of the object" pairs
    l = input_number(n) #calls the input_number() with the input given to generate_d()
    dict1= {}#dictionary for quantities that can be supplied
    for key in l:
        if key not in dict1:
            dict1[key]= random.random()#creating randomly the weights of each object, a float from 0 to 1
    return dict1


def allocation(lis):#The greedy function, which from a given list, just allocates the objects in containers, considering that a container
#cannot keep more than C kg.
    #lis = sorted(l)
    C = numpy.sqrt(len(lis))#maximal weight capacity of each container
    final = []
    i = 0#the index to iterrate over the list passed to the function
    while i<len(lis):#for as long as the index is smaller than the length of list, (meaning that we are not exceeding the maximum of iterration)
        container = []
        capacity = C
        while lis[i]<=capacity:#for as long as the weight of the object doesn't exceed the capacity of the container
            capacity-=lis[i]#the capacity is updated when the object we are considering can fit into the container without exeeding its max capacity
            container.append(lis[i])#you can append the current object in this container
            i+=1#pass to the next object of the pased list
            if i == len(lis):
                break
        final.append(container)#when container is full, appended to the list of containers and we start considering another container
    return final

#When executing the greedy or the exhaustive search, what we obtain are the containers with the weights of the objects displayed.
#In order to dispaly the number of each object that is found in every container, these two functions use the dictionary returned by generate_d() while searching
#on the containers list. It creates another allocation list, with the same allocation pattern as before. In this way the user can obtain the object placement,
# in containers, as well as the weight of each object in each container.

def objects(given_list, pairs: dict):#for every container, it applies find(), then append the new container form in positioning list.
    positioning = []
    #pairs = generate_d(n_list)
    for container in given_list:
        new_container = find(container, pairs)
        positioning.append(new_container)
    return positioning

def find(L, d): #for every element in a given list, exploits all the vlaues of dictionary. If the values matches with the element,
    # appends the key associatied to this value, in a list, Returns this list of keys in the end.
    new_l = []
    for element in L:
        for key in d:
            if d[key] == element:
                new_l.append(key)
    return new_l


def total_p(random_list):#the function to yield all possible permutations of the list passed to it, required for the exhaustive search.
    if len(random_list) <=1: #in cases that the passed list is empty or contains 1 elemtn, it returns the list itself
        yield random_list
    else:
        for permutation in total_p(random_list[1:]):#else, it considers all the permutations of the other the list, excluding the first element in recursive way
            for i in range(len(random_list)):#computes and combines the permutations of specific segments of the passed list
                yield permutation[:i] + random_list[0:1] + permutation[i:]


def ex_s(lis): #the exhaustive search function, considers the allocation in containers of all the possible permutations.
    # This is done by applying allocation() in every permutation. Returns the combination that invloves the smallest no of containers
    max_containers_no = len(lis)#the maximal number of containers used, which corresponds to 1 object put in each container
    result = total_p(lis)
    best_allocation = []
    for permutation in result:
        if len(allocation(permutation))<max_containers_no:#while computing the allocation of every singel permutation, the program compared their length to the maximal one
            max_containers_no = len(allocation(permutation))#if the length of current combination is smallest, then this will be set as the new maximal number of containers used
            best_allocation= allocation(permutation)#assign the permutation to the best_permutation, if its length < maximal number of containers used
    return best_allocation# in containers are written the weights of the objects


def mi(result): #this function can be used to check the correctness of the exhaustive search. It stores the length of
    # each permutation and returns the minimum of them all, for testing and checking purposes only.
    L = []
    for permutation in result:
        L.append(len(allocation(permutation)))
    return min(L)

def testG(n: int, repetitions=1000) -> tuple: #this function's purpose is to test the running time of the Greedy function, for a given input size.
    # It will compute this time as many times as it is declared in the repetitions and then return the average time of all these trials.
    # the result is rounded to 9 digits.
    for i in range(repetitions):
        generate_input = generate_d(n)
        input = list(generate_input.values())
        with Timer(name='allocation', logger=None):
            allocation(input)
    return round(Timer.timers.mean('allocation'), 9)

def Time_setsG(input_list:list)-> list:#for testing purposes, this function takes a list of inputs sizes, and it calls the testG for each of these inputs.
    #the results of these runs, (the average running time for each input size) is stored in a list. This list is what the function returns.
    l=list()
    for input in input_list:
        result=testG(input)
        l.append(result)
    return l

def curveG(x, a, b):#testing function, which defines the proposed function which represents the greedy time complexity and returns the coefficients.
    return a * x + b
'''Why there are specific testing functions for each algorithmic approach? Because generalising the testing functions would increase the time complexity of it.'''
def testES(n: int, repetitions=10) -> tuple: #this function's purpose is to test the running time of the Exhaustive Search function, for a given input size.
    # It will compute this time as many times as it is declared in the repetitions and then return the average time of all these trials. This average number is
    # rounded up to 6 digits.
    for i in range(repetitions):
        generate_input = generate_d(n)
        input = list(generate_input.values())
        with Timer(name='exhaustive_s', logger=None):
            ex_s(input)
    return round(Timer.timers.mean('exhaustive_s'), 6)

def Time_setsES(input_list:list)-> list:#for testing purposes, this function takes a list of inputs sizes, and it calls the testES for each of these inputs.
    #the results of these runs, (the average running time for each input size) is stored in a list. This list is what the function returns.
    l=list()
    for input in input_list:
        result=testES(input)
        l.append(result)
    return l

def curveES(x, a):#testing function, which defines the proposed function which represents the exhaustive search time complexity and returns the coefficient.
    return a * x * scipy.special.factorial(x)

def print_pairs(time_list, value_list):#this function takes the input list given to Time_sets functions, as well as its result, to print pairs of
    # (input size, average running time). So it provides the coordinates to be inserted in the graph.
    for (n, t) in zip(time_list, value_list):
        print((n,t), end='')

def benchmarking(function, inputs_numbers):#this function tests either of Greedy or exhaustive search, with a given list of inputs.

    if function == 'Exhaustive Search':
        for element in inputs_numbers:
            generate_dictionary = generate_d(element)
            generate_list = list(generate_dictionary.values())
            print(objects(ex_s(generate_list), generate_dictionary), end='\n')
    if function == 'Greedy':
        for element in inputs_numbers:
            generate_dictionary = generate_d(element)
            generate_list = list(generate_dictionary.values())
            print(objects(allocation(generate_list), generate_dictionary), end='\n')

def automated_testing(input:list):#this function tests at the same time for the same list of inputs both the Greedy and the Exhaustive search
    #then it compares their result, in order to evaluate whether the Greedy provides the optimal solutions or not. The criteria for this evaluation is the lenght of
    #the list both functions return as a result. Because it represents the number of containers.
    for input_option in input:
        generate_dictionary = generate_d(input_option)
        generate_list = list(generate_dictionary.values())
        exhaustive = objects(ex_s(generate_list), generate_dictionary)
        greedy = objects(allocation(generate_list), generate_dictionary)
        if len(exhaustive)!=len(greedy):
            print('For input', input_option, 'the given results by both functions are appropriate:')
            print('Result of the exhaustive search: ', exhaustive)
            print('Result of the greedy function: ', greedy)
        else:
            print('For input', input_option, 'the given result by Greedy approach is not the optimal one:')
            print('Result of the exhaustive search: ', exhaustive)
            print('Result of the greedy function: ', greedy)

if __name__ == '__main__':
    #va = generate_d(n) #to create the dictionary
    #val_list = list(va.values()) #to create the list of weights
    #print(va)
    #greedy = allocation(val_list) #call the greedy
    #print(objects(greedy, va)) #return greedy result, which object in which container
    #exhaustive=ex_s(val_list) #call the exhaustive search
    #print(objects(exhaustive, va))  #return exhaustive result, which object in which container

    #Testing#
    #time = testES(objects, repetitions=10)
    #b = Time_setsES([2, 3, 4, 5, 6, 7, 8])
    #print(print_pairs([2, 3, 4, 5, 6, 7, 8], b))
    #print(b)


    #benchmarking('Exhaustive Search', [2, 3, 4, 5, 6, 7, 8, 10])
    #automated_testing([4, 6])
