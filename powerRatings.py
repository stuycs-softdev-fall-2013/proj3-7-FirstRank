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
    return (opr(M, S), dpr(Mprime, Sprime), diffpr(M, Mprime, S, Sprime))

#M_list[i][j] is the total number of matches in which team i and team j were on the same alliance.
#Mprime_list[i][j] is the total...team i and team j were on opposing alliances.
#S_list[i] is the total number of points scored by team i in all of their matches.
#Sprime_list[i] is the total number of points scored against team i in team i's matches    
def getEverythingWithLists(M_list, Mprime_list, S_list, Sprime_list):
    M = matrix(M_list)
    Mprime = matrix(Mprime_list)
    S = matrix([[x] for x in S_list])
    Sprime = matrix([[x] for x in Sprime_list])
    return getAllRatings(M, Mprime, S, Sprime)
