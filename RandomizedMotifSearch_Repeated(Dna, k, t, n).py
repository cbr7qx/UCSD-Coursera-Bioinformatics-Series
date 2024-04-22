import random

# Input:  Positive integers k and t, followed by a list of strings Dna
# Output: RandomizedMotifSearch(Dna, k, t)
def RandomizedMotifSearch_Repeated(Dna, k, t, n):
   best_motifs = RandomMotifs(Dna, k, t)
   for i in range(n):
       motifs = RandomizedMotifSearch(Dna, k, t)
       if Score(motifs) < Score(best_motifs):
           best_motifs = motifs
   return best_motifs


def RandomizedMotifSearch(Dna, k, t):
    M = RandomMotifs(Dna,k, t)
    BestMotifs = M
    while True:
        profile = ProfileWithPseudocounts(M)
        M = Motifs(profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs
        
def RandomMotifs(Dna, k, t):
    motifs = []
    for i in range(t):
        s = random.randint(1, len(Dna[0])-k)
        random_kmer = Dna[i][s:s+k]
        motifs.append(random_kmer)
    return motifs

def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = {'A':[], 'C':[], 'G':[], 'T':[]}
    count = CountWithPseudocounts(Motifs)
    for letter in profile:
            profile[letter] = [count[letter][j] / (t + 4) for j in range(k)] 
    return profile
def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    PseudoCount = {'A':[], 'C': [], 'G':[],'T': []}
    for letter in 'ACGT':
        for i in range(k): PseudoCount[letter].append(1)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            PseudoCount[symbol][j] += 1

def Motifs(profile, Dna):
    motifs = []
    for i in range(len(Dna)):
        motifs.append(ProfileMostProbableKmer(Dna[i], k, profile))
    return motifs               
def ProfileMostProbableKmer(text, k, profile):
    n = len(text)
    MaxProb = -1.0
    most_probable_kmer = ""
    for i in range(n-k+1):
        kmer = text[i:i+k]
        kmerProb = Pr(kmer, profile)
        if kmerProb > MaxProb:
            MaxProb = kmerProb  
            most_probable_kmer = kmer  
    return most_probable_kmer
def Pr(text, profile):
    probability = 1.0
    for i in range(len(text)):
        probability *= profile[text[i]][i]
    return probability
                   
def Score(Motifs):
    consensus = Consensus(Motifs)  
    k = len(consensus)
    t = len(Motifs)
    score = 0
    for j in range(k):
        for i in range(t):
            if Motifs[i][j] != consensus[j]:
                score += 1
    return score
def Consensus(Motifs):
    k = len(Motifs[0])
    count = CountWithPseudocounts(Motifs)  
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus
def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    PseudoCount = {'A':[], 'C': [], 'G':[],'T': []}
    for letter in 'ACGT':
        for i in range(k): PseudoCount[letter].append(1)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            PseudoCount[symbol][j] += 1
    return PseudoCount

dna_raw = 'AGCTATAGCTTCCATAAAGGTTTGAAACCACGTACATGCACTGATCATGGTTGTTGGCAATACTGAGCCGCAAAGTAAAGTATAGGTAGTAAAGTCCCAGGATATCACCTTTTGGACGTCCGGTCTACCCCATGCACTACTACCTTCCTCGATTGCCGAAGTATTGTCTGAACCGAGCTATAGCTTCCAT AAAGGTTTGAAACCACGTACATGCACTGATCATGGTTGTTGGCAATACTGAGCCGCAAAGTAAAGTATAGGTAGTAAAGTCCCAGGATATCACCTTTTGGACGTCCGGTCTACCCCATGCCCCGCATAGTGGTCCACTACTACCTTCCTCGATTGCCGAAGTATTGTCTGAACCGAGCTATAGCTTCCAT TGTGCTGTGTAGCCATAAATGACAAGATATTCTCGGCTGAGGGGGATACGTTATCCCGTGCGATTCATCACTTGCAATTTTACTGGCATTACCGTACCTTGGTGATGAAGAGCTTTGCATAGCAGCACTATTCCGTAGTCTTAGTTAGTGGTCCTTCGGAGGACCGCTGCCGACTCCTTGATTCAAACCA TGAAAACTACAAGTCCGCTCCGCTGCGGCTAGCAACTACGCGTGGATCCCCGTGGTTGGTCCGCGTTAAACCTAGTTGTTCTAGACTATGGACCTGGATACCCGATTTTTACCTCGTTTGGGCGTTGCAGTGCCGGGCCAGGTATGGAAGACCCGCACAGCGACGTACACGATGCACATCTAAACTACAC TCCATGGGAATCAGGTTGGCATTGACCTGCGGGTTGCATATGAATGGTGTTGGATCCAAGGTATCTTGTGCGGGTATTAAGGGCTAACTCAGGTGTATCTTTATTCACCTCCCCGTTCCCGGTCCCTAAATTCCAGCGCTTAGAGAGACGATCGGACTCGATACCTTCACGTCTAGACCGCCCCCACACT CCAAGCTGGAAAACACGCCATACGGACTGGACGCCCATTGGAAAGCAATGCTGCCAAAATTCAAGACACTATCGGGCCTTGAGTTACACTATTCACAGATGCGGCAACCCAAACGTCTCTGAGGTGCAGTGTGGTTTCCAACGCCCCGTTAGTCCACCTGATCGGGCTCTGCATGTTACTGAGGTGGCAA CACAGTGGGTACAGGGTTGTTACTCATGCTTGAGCCTGGTCCCCGATTCACGGTACTATGGATCTTGGTAGCTAGTTCTGTACCTTCCGCCATTTAGATAGGATGCACCATAAGATCAGGCCCAAAGACGTATCACAAGGTCCGCACAACCGTGCCAGTTGCGATCGTAGCGCCCCGTTACACGTCCGGT GGTCTATGGTTCCCGTTTTAGTGGTCCTTTAACAGAAGTAGTATACCGCGTATAGAATCAAGACCACTGCGCTGGTCCCATCGCAAGGTGGCCAGTAGCCTTTAAATCCGAGCTAGCCCACGAGTCGGGGCCGCCGATCGAACTCGCAGCTTACTGATACGCGATTATAATCTCTAGAGCTATAAAGCTT ATCATTCCTGCATTCGGTAGTTCCGTTGCGACACGTCCCACTGCAGGAGGGGTACTCTCCCTCAGTACGTGGAGCCTGGATGATTTTAAGACCCCTCGAGTGGTCCTCGCATCTAGTGCCGTCGGCAATTACGCAATGTGTTACTCGGGGGGACATTCATGCTCGAAGTAGCCAGGTTCATACCAAACTA TGCCAAAGCCAGTCAAATGAACAAGAGGTTCTACGGTATGTAAGATTGACGACGAAAACGGCCAGGAACGTGAGCGCCAGGAAGCGTATCTGGTTATTCAACATAGAGGGGTTGTTAATCGACTATGGGTTCCTCTCAGCATCGCGTGACAGTAAGCACCCGTTAGTGGTTGACCCGTATCTCCTGATTG CGGACGCGTCTTAAGTAACTGCGATAGGAATGGGGCTATGCAGGATCCCGGGGGGACTTCACCTTGTCGATTGAACGTTGGGTGTCGGTACACAAGAACTTGACAGGGCATGAAACTCCCCCCGTTAGTGGCTTTGAATCCTTACCCTTAAACCCGTGGCTTACAGTCCTTAGCGCGCAGCTCCGCAGTA CGTACTGAGGCCCCAGGAGTGGTCCGAGCCGGGCACGACCCCAACCGCACCCAGACGAGGTACAGTCAGTTCCTAATATTTATACGATCTGTGAGTGACCGGACGCGCGTCGCGACACCATACAATGAAGTTCCCGGTGACCAAACAGACAAGGTACGTCTACGTGAAGATCCGATCGATGCGAGCCACA GCAAACGGAATGATGGCCGTACGCAATGCTCATCCTTTTGTCAGGCTATGTGAGCCCGTGGCCCCCGTCATTGTCCTAATTACCCTATATGTTGCTATGCCGTTAGTGGTCGTACTCGTCTCTTACGTGAGCCTCAAGGATACTGAAAGCAGTATAAGCATAACGATATTACGCACGTAACCGGCTTGGA GCGTGCGAGAGCCCTTTACGCTCCGCTCCCTCCTTCTACCGCCGGTCCTCTCCAATGTTGTACATGTTTTGGGGGCAGCTACCTGAAAAATTTTTAGATAAAGAACTTCCTAAACGAACCCCCGCACGTGGTCCTCTCATCCGATCATGGGACAACGCACATTAGGCGGTTAAATTTCGCACCGGTGACT TTCAGTGACGACTCCGCAAATTATCCAATCCAAGCTGGAATTGCGGGAACCGATAGGTCGGTTTAACATTGACCGCAGCTGGTAATGAAACCCATTGTGCAGCCTCCGGAACTAATTTAGACCAAATAAACGCACGATCCTGCCCCCGTTAGTGACTCAACTAGTGTATACGACGAACCCACGATAGGGT GACGAATGTGTCGGACACTGCACCAGGATCACTCTCCCTTCCCAAATAGTGGTCCCTCTGCGGGCATATGCACCAATCGTGCATCGTAAGAAGGATGTGGTATACTATTCAAAAAGGTGGCCCCGGAGTTCAGCCGCCATCAGCTGACCATCGATAGAACCGATATATGGTGTTTGTGGTTTTCGCTGCA ACAAGTGCTACCGTCAGTTAATGTACTGTAAACCCCGTGTTTCTAAAATTAGGCCACCATACCATTGTGGCGTTAGCTAGTAACTGCACGGCATACTCCACTTGGGGCTTGCGACAAGTGACTCTCCTCGCGGAGACCCGCTACGCAGTGCACGGGGGGTGTGGAACCCCGTGCCTGGTCCGCGTCGTGT AATTAACACTTGTTCCCACATTAACAACGCCATGCGACGCTCAGTTAGGTAGCGAATAGCCATAGTCAACAATGTAGATCTCTCAGAGAATCATAGTTTGAGCGTTAGTGGTCCTGCACTGCGACACCGAATTGTAGTGTACATTACAGGTTTAGGACGTTTGTCCTCAAATGGGACCTTCAAGCAACAG TTGGCTAGTTGAAGGCTGGGCGAAAGGAGTAGGCACTTGCCGTGACCATACGAATCCAGCAGGTGATTCACTAGGATGGCGTGGGCTACGACCATGTCGCCGCTGACAATCCACCTCCGGCTTCCCGTTATGCATCAGAGGTATACACTATATCCCCGTTAGACCTCCCACATGGGGTCGGGCCTGCATT CTAACTCTACCCGAATCTAGTCGGAATCGCAATGTTTGTATAGATGACCAAACCCCGGGGGTGGTCCCTGCCCCTCCTGGCGTTTCCGGTGCTTTCTGTTCAACACGGGTGTAGGCCAATACCCGGTCGCCTTAAGTTTCTGACCTGCGAGGTCTCGTCGATAAAGTTAGCCTGCTGTCCGTTTACCTTA'
Dna = dna_raw.split()
k = 15
t = 20 #number of strings in Dna
n = 1000 #number of iterations of RandomizedMotifSearch
print(Dna)
print(*RandomizedMotifSearch_Repeated(Dna, k, t, n))
