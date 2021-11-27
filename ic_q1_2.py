# function that creates a huffman code dict for a given probability distribution
def huffman_dict(probability):

    if(len(probability) == 2):                                                           # for only 2 symbols, assign 0 and 1 (base case)
        return dict(zip(probability.keys(), ['0', '1']))

    # Creating a new distribution by merging the lowest probability pair
    q = probability
    temp = sorted(q.items(), key=lambda i: i[1])                                         # sorting the distribution 
    p1, p2 = q.pop(temp[0][0]), q.pop(temp[1][0])                                        # extracting the probabilities of pair of symbols with lowest prob. 
    q[temp[0][0] + temp[1][0]] = p1 + p2                                                 # merging the probabilities 

    # Recursing and constructing code on new distribution
    c = huffman_dict(q)
    cword = c.pop(temp[0][0]+temp[1][0])
    c[temp[0][0]], c[temp[1][0]] = cword+'0', cword+'1'
    return c

# Function takes the input of text file and returns the huffman code for the generated probability distibution for the characters.
def get_huffman_code(input_file):

    with open(input_file, 'r') as file:                                                  # r - read mode
        count = collections.Counter(file.read())                                         # returns the frequency of each character
        print(pprint.pformat(count))                                                     # prints the frequency table 
        total = sum(count.values())                                                      # sum of all frequencies

    # probability distribution
    for i in count:
        count[i] /= total

    # Generating the huffman code for the given probability distribution.
    code = huffman_dict(count)
    print('\nHuffman code generated:')
    print(code)
    return code

# checking if the decoded file and the orignal file have no error
def check_file(input_file, dec_out_file):
    decode = open(dec_out_file, 'r')                                                    # reading the decoded file
    decoded_file = decode.read()
    decode.close()

    original = open(input_file, 'r')                                                    # reading the original input text file 
    original_text_file = original.read()
    original.close()

    return decoded_file == original_text_file                                           # returns 1 is the files are the same 


# main function 
# Collections are container encoded_data types. This is an in-built module providing additional encoded_data structures to store sets of encoded_data.
# The pprint module provides a capability to “pretty-print” encoded_data structures in a well-formatted and more readable way.
# The os. path module is used for processing files from different places in the system.
import collections
import pprint
import os
import time


input_file = input('Enter input text file name: ')                                       # get the input text file 
print('\nFrequency of each character in the text file')
start_time = time.time()
huffman_code = get_huffman_code(input_file)                                              # obtain the huffman code 

end_time = time.time()
timetaken = end_time- start_time
print("\nTime taken for generating huffman code: ", timetaken, "seconds") 

# encoding
file = open(input_file, 'r')
enc_output_file = input('\nEnter output text file name which stores the encoded data: ')
output =  open(enc_output_file, 'w')

start_time = time.time()

while 1:
    char = file.read(1)                                                                 # read one character at a time
    if not char:
        break                                                                           # break from the loop when no character is read
    output.write(huffman_code[char])                                                    # write the codewords of the characters read in the output file

# size of file
# get the current position of cursor, this will be equivalent to size of file
output.seek(0, os.SEEK_END)
print("\nSize of file is :", int(output.tell()/8), "bytes")
file.close()
output.close()

end_time = time.time()
timetaken = end_time- start_time
print("\nTime taken for compression: ", timetaken, "seconds")                           # time taken

# decoding
encoded_out_file = open(enc_output_file, 'r')
dec_output_file = input('\nEnter output text file name which stores the decoded data: ')
output2 =  open(dec_output_file, 'w')

start_time = time.time()

symbol_list = list(huffman_code.keys())                                                  # symbol
codeword_list = list(huffman_code.values())                                              # codeword

encoded_data = str(encoded_out_file.read())                                              # read the encoded file               
length = len(encoded_data)
i = 0
while i in range(length):                                                                # traverse through the encoded string
    b = ''
    while b not in codeword_list:                                                        # traverse until you reach a valid codeword 
        b += encoded_data[i]
        i += 1                                                                           # store the valid codeword
    position = codeword_list.index(b)                                                    # obtain the index of the codeword from the list of codewords 
    output2.write(symbol_list[position])                                                 # write the symbol of the codeword obtained in the decoded output file
encoded_out_file.close()
output2.close()

end_time = time.time()
timetaken = end_time- start_time
print("\nTime taken for decoding: ", timetaken, "seconds") 

if(check_file(input_file, dec_output_file)):
    print('\nThe decoded output is same as the original file, hence there is no error in decoding.')
else:
    print('\nThe decoded output is not the same as the original file')
