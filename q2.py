# Importing packages which are:
# 1. matplotlib.pyplot - used for plotting
# 2. random - used for generation of random numbers
import matplotlib.pyplot as plt
import random

# Initialising all the input parameters in an array to later iterate through
n1 = [15,15,15,20,20,20]
k = 10
p1 = [0.015,0.1,0.45,0.015,0.1,0.45]
ploterror = [0]*6

# Main code:
for index in range(6):
    # Initialising n,p values that will be used for the given iteration
    n = n1[index]
    p = p1[index]
    # Extra input parameters which are relatively small to work with, helps in debugging or running through the code.
    # Uncomment the same to use it.
    # n = 4
    # p = 0.25
    # k = 4
    lenCode = 2**k                                                                        # lenCode denotes number of codewords in the code
    code = [[0]*n]*lenCode                                                                # Initialise code array
    i = 0
    # Loop to generate the lenCode codewords without any repitition 
    while i in range(lenCode):
        flag = 0
        temp = [0]*n
        for j in range(n):
            temp[j]=random.randint(0,1)
        for ind in range(i):                                                        # Checks for repitition
            if(code[ind] == temp):                                                  
                flag = 1
                i-=1                                                                # If repeated, this codeword is not considered 
        if(flag == 0):
            code[i] = temp
            i+=1
    
    # Initialising E to 0, E represents number of errors while decoding the output after we pass N random codewords through a 
    # simulated version of the BSC.
    E = 0 
    N = 500
    for t in range(N):
        codeword = code[random.randint(0,lenCode-1)]
        store = codeword
        # Initialising y which stores the output after passing through BSC
        y = [0]*n
        # Simulation of BSC
        for x in range(n):
            rem = codeword[x]
            if(random.random() < p):                                                # Generates a random number. If it is < p, flip.
                rem = (rem+1)%2 # flipping the bit                                  # Works due to uniform distribution of random numbers
            y[x] = rem
        # Finding estimate after passing output through a minimum distance decoder
        MINerror = n
        for word in range(lenCode):
            other = code[word]
            error = 0
            # Finding Hamming distance between output and current word
            for s in range(n):
                if(other[s] != (y[s])):
                    error += 1
            if(error <= MINerror):
                MINerror = error
                estimate = code[word]
        # estimate stores the closest word to the original 
        I = 1                                                                       # Indicator to check if estimate is the same as original
        if(estimate == store):
            I = 0
        E += I                                                                      #Increasing E if estimate is not the original codeword
    
    AvgError = E/N                                                                  # Finding average error
    ploterror[index]=AvgError                                                       # Storing it to plot average error
    print('n = %d, k = 10, p = %f' %(n,p))
    print('Approximate average probability of error = %f' %AvgError)

label = ['n=15,p=0.015','n=15,p=0.1', 'n=15,0=0.45', 'n=20,p=0.015','n=20,p=0.1','n=20,p=0.45']
left = [1,2,3,4,5,6]

# Plotting bar graph of average error for different values of n,p,k
plt.bar(left,ploterror,tick_label=label)
plt.title("Approximate average probability of error for different (n,k,p) for k=10")
plt.ylabel("P_e(n,k,p)")
plt.show()

# Additional plots to see how the graph varies wrt n and p
# plt.plot(n1,ploterror,linestyle='dashed',marker='o',markerfacecolor='red')
# plt.title("P_e(n,k,p) vs n")
# plt.ylabel("P_e(n,k,p)")
# plt.xlabel("n")
# plt.show()

# plt.plot(p1,ploterror,linestyle='dashed',marker='o',markerfacecolor='red')
# plt.title("P_e(n,k,p) vs p")
# plt.ylabel("P_e(n,k,p)")
# plt.xlabel("p")
# plt.show()

