import numpy as np
'''The first function is needed to take the input of the user, who specify the sequences to be aligned'''
def get_sequences():
    s1 = str(input('Insert a sequence of DNA/RNA: '))
    s2 = str(input('Insert the other sequence of DNA/RNA: '))
    return s1.replace(" ", ""), s2.replace(" ", "") # to remove spacing between sequences, found in some databases like NCBI
'''return the sequences as list, to be used later'''
sequences = get_sequences()
seq1 = list(sequences[0])
seq2 = list(sequences[1])

'''The function which builds the matrix, appending the inserted sequences in the 'mat' list.'''
def matrix(seq2): #matrix creation and addition of empty row and column
    mat = [['/', '_']+seq1] #addition of the new empty cell(of the empty column) and the first sequence as the lable of matrix
    mat.append(add_r(seq1)) #addition of empty row
    for element in seq2: #extends the rows based on the length of the first sequence
        row = list(element)
        i = len(seq1)+1
        while i>0:
            row.append(0)
            i-=1
        mat.append(row)
    #return np.array(mat)
    value = 0
    for i in range(1, len(mat)): #fill the empty row and column, depending on the choice of alignment, local or global
        mat[i][1] = value
        value += type(inp)
    return mat

'''The function that adds the additional row'''
def add_r(seq1) -> list :
    row = ['_']
    value = 0
    while len(row)<len(seq1)+2: #adding the values among the row
        row.append(value)
        value+=int(type(inp))
    return row

'''The function which takes the user's alignment preference, based on that returns a value needed to fill the extra row and column '''
def type(inp) -> str:
    if inp == 'GLOBAL':
        return gap_score
    if inp == 'LOCAL':
        return 0
inp = str(input('Chose the type of alignment you would like to perform, GLOBAL or LOCAL: '))

'''The function to fill a matrix with the values, and the other with the moves.'''
def cal():
    h_v = (0, 0)
    highest_value = 0
    #the highest value of the matrix needed for the initiation of local alignment???????????
    number = matrix(seq2) # values matrix, created by matrix() function
    move = matrix(seq2) # moves matrix, created by matrix() function
    highest_value = 0
    for i in range(2, len(number)): #iteration through the matrix to set the values of each cell
        for j in range(2, len(number[0])):
            left = number[i][j-1] + gap_score #score for moving to the left
            diagonal = number[i-1][j-1] + complete(i, j, Match, Mismatch) #score for moving diagonal based in the outcome of complete() function
            up = number[i-1][j] + gap_score #score for moving up
            choices = {'LEFT': left, 'DI':diagonal, 'UP':up} #create a dictionary to store the name of the move and the score associated to each move
            val = max(choices.values()) #the maximal value out of 3 computation possibilities
            number[i][j] = val #assign this value to the cell
            if val >= highest_value:
                highest_value = val
                h_v = (i, j)
            for key in choices: #iterating through the dictionary, based on the value we set in the values matrix,
                if choices[key] == val: #find the corresponding move and add it to the same cell of the Moves matrix
                    move[i][j] = key
    return move, number, h_v, highest_value
    #return np.array(number)

'''The function who compares each letter of each sequence, and returns the corresponding value if it's a match or a mismatch'''
def complete(row, col, Match, Mismatch):
    mat = matrix(seq2)
    if mat[0][col]==mat[row][0]:
        return Match
    else:
        return Mismatch

'''The function which takes the users input on the match and mismatch assigned values.
 He can chose to keep the previously decided ones, or to change based on his will'''
def set_score():
    match = 1 #the already assigned values
    mismatch = -1
    if feedback == 'NO': #based on the users input, the function knows which values to return
        return match, mismatch
    if feedback == 'YES':
        n_match = int(input('Match: '))
        n_mismatch = int(input('Mismatch: '))
        return n_match, n_mismatch

print('The scores are set as following: Match = +1, Mismatch = -1')
print('Would like to change them?')
feedback = str(input('Type YES or NO: '))
score = set_score() #calling the function, the first element is the Match value, the second the Mismatch value
Match = score[0]
Mismatch=score[1]

'''The fucntion which asks the user if he wants a customized value of gap, if yes, takes and returns it. Otherwise, passes as gap value -2'''
def gap_s():  # returns the value
    g = -2
    if feedback_g == 'YES':
        Gap = int(input('Gap: '))
        gap_1 = Gap
        return gap_1
    if feedback_g == 'NO':
        return g
print('The gap score is set automatically Gap = -2')
print('Would like to change it?')
feedback_g = str(input('Type YES or NO: '))

gap_score = gap_s() #setting a global variable with the returned value of gap_s() function

'''The function which returns the gap in the alignment of sequences'''
def gap():#->str:
    return '-' #for gaps


'''The function return the elements of each sequence, in lower case if they don't match, in upper case if they match'''
def association(el_1, el_2):
    if el_1 != el_2:
        return el_1.lower(), el_2.lower()
    else:
        return el_1.upper(), el_2.upper()


'''The backtracking function for the global alignment, takes as parameter the range i and j,
 the moves matrix and the sequences with will be filled with the sequences letters. My first tryout was with iteration,
  however the recursion if more efficient'''
def backtrack_g(i, j, matrix_m, sequence_1='', sequence_2=''):
    if i == 1 and j == 1: #in case we are dealing with the first cell of the matrix, we return just the sequences,
        return (sequence_1, sequence_2) # because its formed by the empty row and column
    elif i==1: #if the cell is in the row with index 1 (the added row)
        sequence_1 += matrix_m[0][j].upper()
        sequence_2 += '-'
        return backtrack_g(i, j-1, matrix_m, sequence_1, sequence_2) #return the function but with the new j-1 coordinate, passing to the previous column
    elif j==1:#if the cell is in the extra added column, the one with index 1.
        sequence_1 += '-'
        sequence_2 += matrix_m[i][0].upper()
        return backtrack_g(i-1, j, matrix_m, sequence_1, sequence_2)#return the function but with the new i-1 coordinate, passing to the revious row
    elif matrix_m[i][j] == 'DI': #recursion call in diagonal
        relation = association(matrix_m[i][0], matrix_m[0][j])
        sequence_1 += relation[1]
        sequence_2 += relation[0]
        return backtrack_g(i-1, j-1, matrix_m,sequence_1, sequence_2)
    elif matrix_m[i][j] == 'UP': #recursion call up, cell above
        sequence_1 += '-'
        sequence_2 += matrix_m[i][0].upper()
        return backtrack_g(i-1, j, matrix_m, sequence_1, sequence_2)
    elif matrix_m[i][j] == 'LEFT': #recursion call on the left
        sequence_1 += matrix_m[0][j].upper()
        sequence_2 += '-'
        return backtrack_g(i, j-1, matrix_m, sequence_1, sequence_2)

'''The function prints the global backtracking, making also the reverse of its result, since we start from the end of the matrix when we build the aligned sequences'''
def print_g():
    if len(seq1)>1 and len(seq2)>1: #Done to deal with sequence inputs of 1 or zero letter
        matrixs = cal()  # forming the global variables
        matrix_m = matrixs[0]  # the moves matrix
        output_g = backtrack_g(len(matrix_m)-1, len(matrix_m[0])-1, matrix_m)
        first_s = output_g[0]
        second_s = output_g[1]
        print(first_s[::-1] + '\n' + second_s[::-1])#inverting the sequences, since backtraking ang filling strat from teh very last cell
    else: #In case that we are dealing with sequences of length 1 or 0
        if len(seq1)<=1 and len(seq2)>1:
            print(seq1, sequences[1])#returns the first sequence in a list(with 1 or 0 element) and the other sequence of a given length
        elif len(seq1)>1 and len(seq2)<=1:
            print(sequences[0], seq2)
        elif len(seq1)<=1 and len(seq2)<=1:#in case of both sequences with length 1 or 0, then returns 2 lists, empty if length is 0
            print(seq1, seq2)

'''The function computes the local alignment, considering the highest value of the matrix, from which the alignment should start'''
def backtrack_l(i, j, matrix_n, matrix_m, sequence_1='', sequence_2=''):
    if i == 1 and j == 1:#in case we are dealing with the first cell of the matrix, we return just the sequences
        return (sequence_1, sequence_2)
    elif matrix_n[i][j] == 0: #in case the cell value is 0
        if i==1:#when the cell is found on the row with index 1 (added row)
            sequence_2 += '-'
            sequence_1 += matrix_n[0][j].upper()
        elif j==1:#when the cell is found on the column with index 1 (added column)
            sequence_1 += '-'
            sequence_2 += matrix_n[i][0].upper()
        else: #otherwise we end the recursion, based on the rule of local alignment, it stops when it reaches a zero
            relation = association(matrix_n[i][0], matrix_n[0][j])
            sequence_1 += relation[0]
            sequence_2 += relation[1]
        return (sequence_1, sequence_2)
    if matrix_m[i][j] == 'DI': #recursion call in diagonal
        relation = association(matrix_m[i][0], matrix_m[0][j])
        sequence_1 += relation[1]
        sequence_2 += relation[0]
        return backtrack_l(i - 1, j - 1, matrix_n, matrix_m, sequence_1, sequence_2)
    elif matrix_m[i][j] == 'UP':#recursion call up, cell above
        sequence_1 += '-'
        sequence_2 += matrix_m[i][0].upper()
        return backtrack_l(i-1, j, matrix_n, matrix_m, sequence_1, sequence_2)
    elif matrix_m[i][j] == 'LEFT':#recursion call on the left
        sequence_1 += matrix_m[0][j].upper()
        sequence_2 += '-'
        return backtrack_l(i, j-1, matrix_n, matrix_m, sequence_1, sequence_2)

'''The function prints the local backtracking, making also the reverse of its result, since we start from the end of the matrix when we build the aligned sequences'''

def print_l():
    if len(seq1)>1 and len(seq2)>1:
        matrixs = cal()  # forming the global variables
        matrix_m = matrixs[0]  # the moves matrix
        matrix_n = matrixs[1]#the value matrix
        coordinates = matrixs[2] #coordinates of the highest value from which the backtracking should start
        co_i = coordinates[0]
        co_j = coordinates[1]
        output_l = backtrack_l(co_i, co_j, matrix_n, matrix_m, sequence_1='', sequence_2='')
        first_s = output_l[0]
        second_s = output_l[1]
        print(first_s[::-1] + '\n' + second_s[::-1])
    else:
        if len(seq1)<=1 and len(seq2)>1:
            print(seq1, sequences[1])
        elif len(seq1)>1 and len(seq2)<=1:
            print(sequences[0], seq2)
        elif len(seq1)<=1 and len(seq2)<=1:
            print(seq1, seq2)

'''The function prints a specific alignment based on a previous input of the user, in inp global parameter, also used in type(inp) function.'''
def alignment():
    if inp == 'GLOBAL':
        return print_g()
    if inp == 'LOCAL':
        return print_l()


if __name__ == '__main__':
    alignment()



