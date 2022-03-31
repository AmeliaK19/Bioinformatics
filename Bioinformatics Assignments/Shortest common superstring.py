import random
import itertools

def getGenome(length=1000):
    genome = ''.join(random.choice('AGCT') for i in range (length))
    return genome

def getSubstring(seq, length=100):
    L = []
    for i in range(len(seq)-length+1):
        L.append(seq[i:i+length])
    return L

'''The sim(a, b) is the function to determine the suffix prefix matching between the given strings a and b. Since this is needed for the filling og the matrix
we are actually interested to know how many characters are involved in the overlap. For this reason we set the initial value of the overlap to 0.
In several cases we would need to compare strings with different length. To index through them without a problem, we index based on the length of the shortest string.
The i takes value from 1 to length of the shortest string,  because when slicing from the end of the string, we would get nothing if i = 0.
We slice two strings by i and -i to compare the characters of the pretended suffic and prefix.
In case that the suffix and prefix returned by slicing with i are the same, overlap is set i. Why so? Because if we slice till index 3 for example, we include
character with index 0, 1 and 2. so we substract 3 elements.
'''
def sim(a:str, b:str):#first string gives the suffix
    overlap = 0
    length = min(len(a), len(b))+1
    for i in range(1, length):
        if a[-i:] == b[:i]:
            overlap = i
    return overlap

'''this function iniciates the labels of the matrix, given a list of subsequences. The first row and first column correponds to the subsequences. 
The special character / is inserted to position properly the labels and cells. The matrix will display a L shape. 
WIll be fileld during the next step.'''
def matrix(a):
    initial = ['/']
    columns = initial+a
    M = [columns]
    for element in a:
        row = [element]
        M.append(row)
    return M

'''The function which filles the matrix, as well as keep track of the cell who has the highest value of overlap in the matrix.
  To create and fill each cell, we have to combine the labels corresponding to that cell, if they are the same subsequence we return -1 to fill the cell.
  In the provided example during the lecture the cell corresponding to two same subseqeunces was marked with an -
  However this could complicate the matrix filling, since all the other possible characters integers and especially the variable 'highest_val' which will 
   keep track of the number of the highest value in the matrix from which the computation of the shortest common superstring will start. 
   Another peculiarity of this function is tuple, it keeps track of the subsequences' labels, whose common cell corresponds to the cell containing the highest value
   and are these two labels which will be combined together to start the superstring formation.
   r stands for index that the suffix subsequence has in the initial list provided to the function, which is the list of all the subsequences.
   In the end, the function returns the filled matrix, the subsequences which will be merged first, the highest value of the matrix from which the merging will
   start and the index of the very first subsequence which contains the prefix '''
def fill(sub_list):
    M = matrix(sub_list)
    index = 0
    highest_val = -1
    tup = ('', '')
    for r in range(1, len(M)): #r for rows, c for columns
        for c in range(1, len(M[0])):
            if r == c:
                M[r].append(-1)
            else:
                M[r].append(sim(M[r][0], M[0][c]))

            if M[r][c] > highest_val:
                highest_val = M[r][c]
                tup = (M[r][0], M[0][c])
                index = r-1 #because our initial list of the substrings, gets shortened in every step.
    return M, tup, highest_val, index

'''This is a trivial auxiliary function which calculates the new string formed by the merging or concatenation of the two given strings. The overlap_no
determines the index which will be used to slice one of the strings, in order to avoid suffix-prefix repetition. It returns the new string formed by the given ones'''
def conc(str1:str, str2:str, overlap_no:int):
    new_string = str1 + str2[overlap_no:]
    return new_string

'''This function is the greedy algorithm application. It is built in base of recursion. The base case its that the list given as a parameter has a lenght of 1.
If so it will return only twhat is inside the list, in a string format. If the lenght is higher than 1, then there are some steps to be followed.
The fill() function is called, filling and creating the matrix based on the list which is passed to the greedy() function as a parameter.
 We already mentioned that the fill() returns also as a tuple the subsequences that should be the first one to be merged. THese are accessed here
 by indexing, named first_seq and second_seq. These subsequences are given as a parameter to the concatenate() function, together with the overlap_no which sorresponds 
 to the highest_val given by the fill(), so its the number of characters which overlap between these two subseqeunces.
 After the concatenate() gives us the new string, this will be placed in subs list, in the position where the subseqeunce that contained the suffix is. So at the 
 same index. Who do we know this index? It is the i, returned by the fill() function.Then the first_seq and the second_seq are removed from the subs list. 
 So the new subs is different from the previous one, it contains the merged subsequence, not 2 shorter subsequences anymore. This new subs list is 
 used as an input to call again the greedy(). till the list length goes one and it returns what is described in the base case.'''
def greedy(subs):
    if len(subs)==1:
        return subs
    function = fill(subs)
    first_seq = function[1][0]
    second_seq = function[1][1]
    overlap_no = function[2]
    index = function[3]
    new_seq = conc(first_seq, second_seq, overlap_no)
    subs.insert(index, new_seq)
    subs.remove(first_seq)
    subs.remove(second_seq)
    return greedy(subs)

'''The function takes a list as a parameter and in another empty list appends all the permutations which will can be formed by the given list, exploiting itertools
'''
def permutation(subs):
    permutations_list = []
    for permutation in itertools.permutations(subs):
        permutations_list.append(list(permutation))
    return permutations_list

'''The function is needed for the exhaustive search, A part of it is almost identical to the greedy(). If the length of the given list is 1, returns what is inside
the list. Otherwise teh recursion starts. First the sim() function is called given as parameters the very first elements of the list.
It will return what is the number of charactrers that are involved in suffix-prefix overlap. This overlap number, is used by the concatenate(), to 
form the new string by combining again the first and second element of the given list subs. After this is performed, we remove from subs the first element and the 
second one (when we remove the first element, the element who used to be in the second place will move to the first one, so its index becomes 0). After this we
insert to the list the new string, in position 0. The modified subs will be used again by the compact_es() function, until all the subseqeunces are 
combined together and the list ends up with a length of 1.'''
def compact_es(subs):
    if len(subs)==1:
        return subs[0]
    overlap_no = sim(subs[0], subs[1])
    new_string = conc(subs[0], subs[1], overlap_no)
    subs.remove(subs[0])
    subs.remove(subs[0])
    subs.insert(0, new_string)
    return compact_es(subs)

'''The trivial auxilary function computes the length of the superstring that can be obtained by concatenating all the substrings found on a list'''
def length(subs):
    total = ''
    for element in subs:
        total+=element
    return len(total)

'''This function applies the exhaustive search method. In this case we do not search for the 2 subsequences that overlap the most, but we consider the subseq
uences as in the order they are placed on the list given as a parameter. We declare a variable, the max_length which by calling length() determines what nis the length
of the superstring in the worst case scenario in which the subsequences do not overlap at all. The reason behind this is to compare this result with all the other 
possible superstrings formed, in order that in the end the program returns the shortest superstring. Considering all the possible permutations of the subsequences
in the list (different positioning of them), we use eac permutation as an inpt for compact_es(). Every result will be compared with the max_length till
the shortest result is found. The shortest superstring is assigned to best_sequence and returned by the function.
'''
def exhaustive_s(subs):
    max_length = length(subs)
    best_sequence = ''
    possibilities = permutation(subs)
    for possibility in possibilities:
        string = compact_es(possibility)
        if len(string) <= max_length:
            max_length = len(string)
            best_sequence=string
    return best_sequence

'''The function which provides the user interface and takes one's inputs. Inside it, based on the input are called getGenome() and getSubstring()
which respectively from their name thier functions can be understood, generate a genome of a given size and divide it in substrings of a given length.
The list of the substrings is given as an input to either of functions, greedy or exhaustive search'''
def take_inputs():
    genome = getGenome(length=length_sequence)
    stringset = getSubstring(genome, length=substring_size)
    if Type == 'GREEDY':
        return greedy(stringset)
    if Type == 'EXHAUSTIVE SEARCH':
        return exhaustive_s(stringset), stringset
    else:
        message = 'ERROR'
        return message
Type = input("Chose GREEDY or EXHAUSTIVE SEARCH:" )
length_sequence = int(input("The length of the sequence: "))
substring_size= int(input("The size of the subsequences: "))


if __name__ == '__main__':
    print(take_inputs())

