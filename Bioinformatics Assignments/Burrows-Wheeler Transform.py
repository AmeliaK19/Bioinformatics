#WORKED BY: Amelia Kurti
import numpy as np
import random
import itertools

'''The function to generate a random string, a DNA fragment of a given length'''
def getGenome(inp:str, length=1000):
    genome = ''.join(random.choice(inp) for i in range (length))
    return genome

'''The function needed for the rotation of the string. Takes a string as a parameter and returns it transformed, the last character now is in the first position'''
def rotations(string):
    i = len(string)-1
    return string[i] + string[:i]

'''The function which calculates all the possible rotation of a given string, by expoliting the rotations() function. All the possible rotations are
added to a list, whose elements in the end are alphabetically ordered.'''
def get_rotations(string):
    rotations_list = []
    i = 0
    while i< len(string): #once a string is rotated, the rotation will be given as a parameter to the get_rotations() function.
        rotation = rotations(string)

        rotations_list.append(rotation)
        string = rotation# So each rotations, serves as a string itself
        i+=1
    return sorted(rotations_list)

'''for a given string, returns a list whose elements are the characters of the string'''
def to_list(string):
    L= [a for a in string]
    return L


'''FUnction to create the matrix from the list of rotations.'''
def create_matrix(string):
    rotations_list = get_rotations(string)
    matrix = []
    for rotation in rotations_list:#each rotation given as a string to to_list(), transformed by it into a list, then appended to the matrix
        l_rotation = to_list(rotation)
        matrix.append(l_rotation)
    return np.array(matrix) #in case of visualization need, it is brought to the right form by numpy

'''The function to substract a specifil column of the matrix, will be needed for the ranking of the first and the last column.
Takes as a parameter a string, from which it builds the matrix using the create_matrix() function, together with the i - index, which
orients the code which of the columns of the matrix to substract. It returns the column as a string.'''
def substract_column(string, i):
    matrix = create_matrix(string)
    column_string = ''
    for row in matrix:
        column_string+=row[i]
    return column_string

'''The function to rank the characters of a given string, in our case the characters of a chosen column of the rotations matrix. For this we are needed
 an empty dictionary and an empty list. In the dictionary to keep track of the occurences of each character, the list to insert all the characters which have
 been ranked. Since the ranking starts from the bottom of the column, we revert it using [::-1]. For every character of the column string, if it is not
 already part of the dictionary, we create a key:value pair (character:occurence_number), where the value is initially set to 0, this corresponds to the rank of the very first x charater
 we find in the string. The character x (key of dictionary) together with its rank (value of dictionary )are added as a string to the list.
 In case that the character x has occured before in our list, it will already be in the dictionary, its value will not be 0. Every time we find another x character, its
 value in the dictionary increases by one. This value will be the rank of this x character in the list. 
 In the end, the outcome is inverted, to obtain the initiall column, but now with the right ranks. '''
def ranks_calculation(string, i):
    column = substract_column(string, i)#i is the index, the forst or last column
    d_ranks = {}
    l_ranks = []
    for c in column[::-1]:
        if c not in d_ranks:
            d_ranks[c]=0
            variable = c + str(d_ranks[c])
            l_ranks.append(variable)
        else:
            d_ranks[c]+=1
            number = d_ranks[c]
            variable = c + str(number)
            l_ranks.append(variable)
    return l_ranks[::-1]


'''The function to generate the offsets. The orientation is done by the $ sign. For every row of the matrix, meaning for every rotation, 
we find the index of the $ sign. The difference of the index of the $ in the initial string, with the actual index in the rotation, represents the offset. 
The offset of every rotation is the index of the first element of this row in the BWM matrix in the initial string. The offsets for every row of BWM 
are appended on a list, which is finally returned by the function. '''
def offset(string):
    M = create_matrix(string)
    offsets_list = []
    for row in M:
        o_s = len(string)
        for index in range(len(row)):
            if row[index] == '$':
                o_s -= index
                offsets_list.append(o_s)
    return offsets_list

'''This is the function which builds a small matrix out of two main columns, the first and the last one,by exploiting the column substracting function 
and the rank_calculation() which takes as a parameter not onlyt hte string from where to build the matrix, but also teh index of the column to be extracted 
and ranked. The building of the matrix involves taking indexing through 2 lists of columns ranks and the offsets list and elements of the list with the same indexes are inserted
in the same row of the matrix. The new matrix with two ranked columns and the offset column is returned. Each element of the matrix's two first columns
 is a string containing the character and the number of the rank.'''
def columns(string):
    first_column = ranks_calculation(string, 0)
    last_column = ranks_calculation(string, len(string)-1)
    offset_column = offset(string)
    M = []
    i = 0
    while i < len(first_column):
        row = []
        while len(row) <= 3:
            row.append(first_column[i])
            row.append(last_column[i])
            row.append(offset_column[i])
            if len(row) == 3:
                break
        M.append(row)
        i += 1
    return np.array(M)


'''The function finds a given element in a given matrix, returning the row of the first column in which you can find this element. The column is 
specifically set as the first one, because it is needed in the following function to obtain the reverse BWT.'''
def find_index(M, element):
    R = 0
    for row in range(len(M)):
        if M[row][0] == element:
            R = row
    return R

'''The function to obtain the reverse BWT. It takes as input a string, which is used by column() to built the matrix of the first and last ranked columns.
We set row to 0 because when we will add characters to the T (the reverse), we will start from the very fist row of the matrix, where $ is found.
 For as long as the length of the T doesn't exceed the length of the string given as a parameter, then to T we add the first character of the first
  element of the row (only the character added to T, not the rank number). Then for the character we just added to T, we search in the 
first column of the matrix, and keep track of the row in which it is found. Now we will direct the searching in this new row where we found the 
specific element in the first column. In this new row, we will find the element of the second column which will be added to T, and so on the proceedure repeats
till the length of the T does not exceed length of the given string'''
def reverse(string):
    T = ''
    M = columns(string)
    row = 0
    while len(T)<len(string):
        T += M[row][1][0]
        r = find_index(M, M[row][1])
        row = r
    return T[-2::-1]+T[-1:] #In the end, it returns the reverse of the given string. However the slicing is needed to reverse the output
    # because the columns of the matrix are itself the inverted version of the string's rotations. In the end, the $ is positioned.


'''Auxilary function which searches for an element in a matrix, and returns the list with indexes of all the rows which start with this element'''
def list_indexes(M, element):
    indexes = [i for i in range(len(M)) if M[i][0][0] == element]
    return indexes


'''The function searches for the query in the matrix. Query is inverted to facilitate the indexing. The searching starts based on the find_index function, 
 which returns the list with indexes of all rows which start with the first element of reversed query. The searching continues for all Q[i], if it stops before 
 this tells that the query not found in our initial string. While searching, every met character in the matrix is added to T, which is/are returned by the function. '''
def find_query(string, query, index):
    T = ''
    Q=query[::-1]
    M = columns(string)
    row = index #where it starts given by the other function
    T += M[row][0][0]
    i = 1
    while i < len(Q):
        if M[row][1][0] == Q[i]:
            r = find_index(M, M[row][1])
            T += M[r][0][0]
            row = r
        i+=1

    return T

'''This function considers the output of the find_query() for all the indexes of rows which start with the first element of reversed query,
compares it/them with the reversed query, and if they are the same, it returns the offset of this BWM matrix row. In the end the function returns the
 list with all possible offsets.'''
def prova(string, query):
    M = columns(string)
    Q = query[::-1]
    i = 1
    indexes = list_indexes(M, Q[0])
    L = []
    for index in indexes:
        option = find_query(string, query, index)
        if option == Q:
            L.append(int(M[index][2]))
    return L

'''The function maps the query to the initial string and prints the offset.
 For every offset, finds where the query starts in the initial string by substracting the length of the 
query (the offset actually tells us where the query ends). The query then printed aligned together with the initial string and the offset.'''
def map(string, query):
    L = prova(string, query)
    query_length = len(query)
    for index in L:
        initial_index = index - query_length
        print([initial_index, initial_index+query_length-1])
        print('_'*(initial_index) + query)
        print(string)

'''This function is needed for the testing. It has the genome as a parameter, to modify it by inserting the query n times. The insertion point, its index
is generated randomly. The function returns the modified genome and the query.'''
def in_serts(genome, n):
    in_sert = getGenome(inp = 'ACGT', length=5)
    for insertion in range(n):
        random_point = random.randint(0, len(genome)-len(in_sert))
        genome = genome[:random_point] + in_sert + genome[random_point:]
        #genome.insert(random_point, in_sert)
    return genome, in_sert


'''Function to perform teh testing with all the possible input cases by calling map(genome, query). If input is 1, then the query maps only once in the genome, if 2 it is inserted in the
genome two times and consequently maps twice and in the case of input 3, the user is asked to input a weird query which isn't DNA related. It will 
not return anything.'''
def testing():
    test = input('Which test would you like to perform, 1/2/3 ?: ')
    genome = getGenome(inp = 'ACGT', length=20)
    if test == '1':
        function = in_serts(genome, 1)
        genome = function[0]+'$'
        query = function[1]
        return map(genome, query)
    if test=='2':
        function = in_serts(genome, 2)
        genome = function[0] + '$'
        query = function[1]
        return map(genome, query)
    if test=='3':
        insert_query = input('Insert a string not DNA related: ')
        return map(genome+'$', insert_query)



if __name__ == '__main__':
    testing()


