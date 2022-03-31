import numpy as np
import random

'''Function to access the content of the file containing the chromosome sequence. The file is opened and all its lines, excluding the special character '>'
of FASTA, are concatenated together and capitalized, in order to unify it and avoid problems during the searching and computing query score.'''
def obtain_seq():
    file = open('chr22.fa')
    seq = ''
    for line in file:
        if line[0] != '>':
            seq += line[:-1]
    return seq.upper()

'''The function to access the file containing all the information about CpGis, every line is modified by removing the empty spaces and instead these are replaced
by commas. Each line's element will be included in a list, called modified_line, and all the lines appended on a final list, named info. Info will contain every
line of the file, represented as a list.'''
def obtain_info():
    file = open('CpGI_chr22')
    info = []
    for line in file:
        modified_line = []
        for element in line.split(): #remove the empty spaces and then to list
            modified_line.append(element)
        info.append(modified_line)
    return info

'''This function returns all the CpGis and all obtained sequences for the outside model, concatenated together, as well as the average length af the CpGis.
It consideres all the list-lines of obtain_info(), and indexes them to obtain their starting and ending coordinates as well as the length. 
The coordinates are used to slice the whole chromosome sequence, and the slice is added to cgi_sequences. The length has two functions:
First is added to total_length, which later is divided by the number of lines (number of CpGis) to obtain the average length.
Second, we first generate a random integer, which will be the starting point of the outside model sequence for this CpGi, and the length needed to find the 
ending coordinate (index) by slicing the chromosome. Just as for the CpGis, the outside model sequences are all merged together in a variable cgio_sequences.'''
def condense_sequences():
    chromosome = obtain_seq()
    information = obtain_info()
    cgi_sequences = ''
    cgio_sequences = ''
    total_length = 0
    for seq in information:
        begin = int(seq[1])
        end = int(seq[2])
        sequence_i = chromosome[begin - 1: end - 1]
        cgi_sequences += sequence_i

        length = int(seq[3])
        start = random.randint(16050050, 52269464 - length)#the numbers correspond to the coordinates in which the N regions are excluded.
        #This could have been done by a specific function rather than calculated manually, but it would create problems if in teh sequence are other N.
        # -length so it will not exceed the unambigous region of nucleotides.
        sequence_o = chromosome[start: start + length]
        cgio_sequences+=sequence_o

        total_length+= length

        total_length+= length

    average_length = total_length / len(information)

    return cgi_sequences, cgio_sequences, round(average_length, 0)


'''The function computes the frequency of each dimer in the string. Takes as parameters the sequence and 2 nucleotides, iterrates througth the sequence, 
and when it meets a nucleotide which is the same as the second_nt, in case that the previous nucleotide corresponds to the first_nt, then it adds +1 to the 
variable that keeps track of the dimer occurrence and the total dimers number.If the previous nucleotide and the first_nt do not correspond, then only to toatl_dimers
the +1 is added.
In the end, it is returned the frequency of this dimer in the sequence, the ratio dimer_occurences / total_dimers '''
def freq_dimer(sequence, second_nt : str, first_nt : str):
    dimer_occurences = 0
    total_dimers = 0
    for i in range(0, len(sequence)-1):
        if sequence[i] == second_nt:
            if sequence[i+1]== first_nt:
                dimer_occurences += 1
                total_dimers +=1
            else:
                total_dimers+=1

    if total_dimers!=0 and dimer_occurences != 0:
        frequency = dimer_occurences / total_dimers
        return frequency
    else:
        return 0

'''The function to initialise each table for each model. it creates only the row and column labels, based on the elements of a list called lables, 
that we give to this function.'''
def table(lables):
    initial = ['/']
    columns = initial+lables
    M = [columns]
    for element in lables:
        row = [element]
        M.append(row)
    return M

'''The function which creates the other cells of the table and fills them. The nulcotides are given as labels of the table() function.
 To till every cell, teh labels of the rows and columns are considered, given as the first_nt and second_nt to the freq_dimer(). The first_nt is the
 row label and the second_nt is the column label. The values correspond to the conditional probabilities to find the second_nt, after the first_nt in the sequence.'''
def fill_table(sequence):
    M = table(['A', 'C', 'G', 'T'])
    for row in range(1, len(M)):
        for column in range(1, len(M[0])):
            M[row].append(round(freq_dimer(sequence, M[row][0], M[0][column]), 2))
    return M


'''The function to access a cell in the table and substract its probability value. It iterrates throught the table and in case that the first_nt correspond to the 
first column label, and the second_nt correspond to the row label, then the M[row][column] value is returned by the function. This is needed for the following 
computational step.'''
def get_probability(M, first_nt, second_nt):
    for row in range(1, len(M)):
        for column in range(1, len(M[0])):
            if M[0][column] == first_nt:
                if M[row][0] == second_nt:
                    return M[row][column]


'''The function to compute the score of a query based on a given model. It takes as parameters the query and a sequence, which can be the CpGis one or the outise 
model sequence CpGo. For every dimer of the query, it calls the get_probability(), which as a model, a table, takes M = fill_table(given sequence), and it returns
the conditional probability of this dimer in the model sequence. For the all probabilities, ln are computed and summed together.  '''
def probability(query, sequence):
    M = fill_table(sequence)
    score = 0
    for i in range(0, len(query)):
        probability = get_probability(M, query[i-1], query[i])
        score += np.log(probability)
    return score

'''This function takes the query, the Cpgi sequence and the CpGo seqeunces, computes the probability scores of this query based on each model, exploting 
probability() function, and returns the difference between them, which determines if the query is a CpG island or not'''
def score(query, cpgi, cpgo):
    i_m = probability(query, cpgi)
    o_m = probability(query, cpgo)
    ratio = i_m - o_m #since the scores are computed in log
    return ratio

'''The function to take the input query from the user, and call the score() function in order to return the value which determines if query is a CpGi or not.'''
def given_input(cpgi,cpgo):
    user_input = input("Insert a sequence to evaluate if it contains a CpG island: ")
    s = score(user_input, cpgi, cpgo)
    if s <= 0:
        print("The inserted sequence with score", s, "is not a CpG")
    else:
        print("The inserted sequence with score", s, "is a CpG")



'''It takes around 4 minutes for a single model to be computed, considering the transformation of the files to string and to lists, indexing ang slicing and
then counting and computations. The following are two models, the inside one which is based on the given CpGis of chromosome 22 and it is always the same in
every computation, and the outside, whcih is created by random splicing, and its values always vary, however both are obtained by executing the program.
Are inserted here in order to speed up the testing process.'''
inside_model = [['/', 'A', 'C', 'G', 'T'], 
               ['A', 0.19, 0.28, 0.4, 0.14], 
               ['C', 0.19, 0.36, 0.25, 0.2], 
               ['G', 0.17, 0.33, 0.35, 0.14], 
               ['T', 0.09, 0.34, 0.38, 0.19]]
               
               
outside_model = [['/', 'A', 'C', 'G', 'T'],
                 ['A', 0.29, 0.2, 0.29, 0.22],
                 ['C', 0.32, 0.3, 0.07, 0.31],
                 ['G', 0.26, 0.24, 0.3, 0.21],
                 ['T', 0.18, 0.24, 0.3, 0.29]]

'''For the testing, since the models are already computed for time effect, the above written fucntions change a bit. The probability_testing() is more
or less the same with the probability(), jsut takes the model as a input and not the sequence itself used to obtain the model. However it returns 
the score of the query calculated on the given model.'''
def probability_testing(query, model):
    score = 0
    for i in range(0, len(query)):
        probability = get_probability(model, query[i - 1], query[i])
        score += np.log(probability)
    return score

'''Similar to score(), it needs only the query as a parameter and directly accesses the models, to obtain the ratio.'''
def score_testing(query):
    inside_model_score = probability_testing(query, inside_model)
    outside_model_score = probability_testing(query, outside_model)
    ratio = inside_model_score - outside_model_score
    return ratio

'''The intup taker for the testing proceedure, identical to given_input(), just applies teh score_testing() function.'''
def given_input_testing():
    user_input = input("Insert a sequence to evaluate if it contains a CpG island based on already calculated models : ")
    score = score_testing(user_input)
    if score <= 0:
        print("The inserted sequence with score", score, "is not a CpG")
    else:
        print("The inserted sequence with score", score, "is a CpG")


##########################################################################################################################################################

#Bonus
'''The function to generate a random string (genome) of a given length.'''
def getGenome(inp:str, length=1000):
    genome = ''.join(random.choice(inp) for i in range (length))
    return genome


'''The function to compute the sliding window for a randomly generated genome, based on the above written models. For every substring of the genome
,that has the average length of a CpGi, starting from the very first character of the genome and shifting by one to create the other window, 
this substring is given as a query to the score_testing() function which will compute the defining CpGi score. If higher than 0, this query offset (i+1, i+length+1)
since index i starts from 0, is appended to the cpg_list=[], which will be returned in the end by the function. '''
def windows(genome, length):
    cpg_list = []
    for i in range(0, len(genome)-length):
        query = genome[i: i+length]
        result = score_testing(query)

        if result > 0:
            offset = (i + 1,  i + length+1)
            cpg_list.append(offset)
    return cpg_list


if __name__ == '__main__':
    #printing the program testing with the already computed model

    #given_input_testing()

    #printing the program as it works, computing a random model for the outside model, on my computer takes around 3-4min to display the insertion phrase
    #and few seconds to display the final result

    sequences = condense_sequences()
    cpgi = sequences[0]
    cpgo = sequences[1]

    #given_input(cpgi, cpgo)
    I = fill_table(cpgi)
    O = fill_table(cpgo)
    print(np.array(I)) # to print the inside model
    print(np.array(O)) # to print a random outside model



    #printing the windows using the already computed models

    #sequences = condense_sequences()
    #average_length = int(sequences[2])
    #genome = getGenome('ACGT', length=5000)
    #print(windows(genome, average_length))



