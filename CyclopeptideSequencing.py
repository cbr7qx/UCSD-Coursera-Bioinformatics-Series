#This code takes a spectrum of peptide masses and returns the most probable peptides that generated that spectrum.
#It consists of multiple rounds of trimming a leaderboard of peptides that have the highest score according to the spectrum.

n = 10 #The number of candidate peptides including ties that are included in the trimmed leaderboard at each step.
spectrum = [0, 71, 113, 129, 147, 200, 218, 260, 313, 331, 347, 389, 460]

            
def leaderboard_cyclopeptide_sequencing(n, spectrum):
    best_peptides = []
    best_score = 0
    parent_mass = max(spectrum)
    leaderboard = [[x] for x in masses] #Starting it with the whole mass library.
    print('original leaderboard: ',leaderboard)
    
    while leaderboard != []: 
    
        #Expand the leaderboard:
        print('\n starting leaderboard: ', leaderboard)
        leaderboard = expand(leaderboard)
        new_leaderboard = []
        print('expanded leaderboard: ',leaderboard)
        
        for candidate in leaderboard:
            
            #Split and sum the candidate peptide string to get its mass:
            split_candidate = str(candidate).replace("'",'').replace('[','').replace(']','').replace(',','').split( )
            split_candidate2 = [eval(x) for x in split_candidate]
            candidate_sum = sum(split_candidate2)
            #print('candidate: ',split_candidate2,'mass sum: ',candidate_sum)
            
            #Check if the candidate is in best peptides:
            if candidate_sum == max(spectrum):
                candidate_score = cyclopeptide_score(candidate,spectrum)
                if candidate_score > best_score:
                    best_peptides = ['-'.join([str(x) for x in split_candidate2])]
                    best_peptide = '-'.join([str(x) for x in split_candidate2])
                    best_score = candidate_score
                if candidate_score == best_score:
                    best_peptides.append('-'.join([str(x) for x in split_candidate2]))
                new_leaderboard.append(candidate)
            elif candidate_sum < max(spectrum):
                new_leaderboard.append(candidate)
        
        #trim the leaderboard:
        leaderboard = trim_cyclo(new_leaderboard, spectrum, masses, n)
        
    #remove duplicates and return best_peptides2:
    best_peptides2 = [] 
    for peptide in best_peptides:
        if peptide not in best_peptides2: best_peptides2.append(peptide)
    print('len(best_peptides): ',len(best_peptides2), ' best score: ',best_score)
    return best_peptides2 


    
def trim_cyclo(leaderboard, spectrum, aa_masses, n):
    scores = []
    new_leaderboard = []
    for i in range(len(leaderboard)): scores.append(0)
    for j in range(len(leaderboard)): scores[j] = cyclopeptide_score(leaderboard[j], spectrum)
    leaderboard.sort(key= lambda x: cyclopeptide_score(x, spectrum), reverse=True)
    scores.sort(reverse = True)
    if len(leaderboard) < n: return leaderboard
    print('cutoff: ',scores[n-1])
    for k in range(len(leaderboard)):
        if cyclopeptide_score(leaderboard[k], spectrum) >= scores[n-1]: new_leaderboard.append(leaderboard[k])
    return new_leaderboard
            
    
def cyclopeptide_score(peptide, experimental_spectrum):
    count = 0
    theoretical_spectrum = cyclospectrum(peptide)
    for mass in experimental_spectrum:
        if mass in theoretical_spectrum:
            count+=1
            theoretical_spectrum.remove(mass)
    return count

def cyclospectrum(peptide_masses):
    doubled_peptide = peptide_masses + peptide_masses
    spectrum = [0]
    n = len(peptide_masses)
    for i in range(n):
        for j in range(1,n):
            fragment = doubled_peptide[i:i+j]
            spectrum.append(sum(fragment))
    spectrum.append(sum(peptide_masses)) #add the sum of the whole peptide
    spectrum.sort()
    return(spectrum)


def expand(peptides):
    new_peptides = []
    for peptide in peptides:
        for mass in masses:
            new_peptide = []
            for i in range(len(peptide)):
                new_peptide.append(peptide[i])
            new_peptide.append(mass)
            new_peptides.append(new_peptide)
    return(new_peptides)    



masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
    
print(*leaderboard_cyclopeptide_sequencing(n, spectrum)) 
    



