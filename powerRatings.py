from numpy import matrix

#M is the matrix of alliance occurrences\
#M_ij is the number of matches in which teams i and j were on the same alliance
#
#S is the total score (column) vector
#S_i is the total number of points scored by team i in the matches they played
def opr(M, S):
    return [x[0] for x in list(M.getI() * S)]
#The vector V returned by the function is such that V_i is team i's tendency to cause their team to score points, or the average number of pointes contributed by team i to their alliance's score. Good teams will have large values.

#Mprime is the matrix of opposition occurrences
#Mprime_ij is the number of matches in which teams i and j were on opposing alliances.
#
#Sprime is the total opposing score (column vector)
#Sprime_i is the total number of points scored by the team i's opponents in the matches they played
def dpr(Mprime, Sprime):
    return [x[0] for x in list(Mprime.getI() * Sprime)]
#The vector V returned by this function is such that V_i is team i's tendency to allow their opponent to score points. Good teams will have small values.

#In order to get the differential power rating, we take the difference of the above arguments
def diffpr(M, Mprime, S, Sprime):
    return [x[0] for x in list((M - Mprime).getI() * (S - Sprime))]
#The vectofr V returned by this function is such that V_i is team i's tendency to contribute to the the number of points their alliance wins by, or the average number of points contributed to their score differential. This can be seen as a mix of opr and dpr, in that it takes both defensive power and offensive power into account. Good teams will have large values.

#This function just calls everything else.
def getAllRatings(M, Mprime, S, Sprime):
    return {'opr':opr(M, S), 'dpr':dpr(Mprime, Sprime), 
            'diffpr':diffpr(M, Mprime, S, Sprime)}
    
