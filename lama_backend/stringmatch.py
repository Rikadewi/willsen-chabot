'''import re

#Algoritma KMP
def KnuthMorrisPratt(text, pattern): #text, pattern = string
    t = len(text)
    p = len(pattern)
    #lps = longest prefix suffix
    lps = [0 for i in range(t)]
    countLongestPrefSuf(lps, pattern, p)

    i = 0; j = 0
    found_at_least_one = False
    while i < t:
        if (pattern[j] == text[i]):
            i += 1
            j += 1

        if (j == p):
            #pattern ditemukan
            print("pattern ada di", (i-j))
            found_at_least_one = True
            j = lps[j-1]
        elif (i < t) and (pattern[j] != text[i]):
            if (j != 0):
                j = lps[j-1]
            else:
                i += 1
    if (not found_at_least_one):
        print("pattern tidak ditemukan")

def countLongestPrefSuf(lps, pattern, len_of_pattern):
    temp_len = 0

    lps[0] = 0
    
    i = 1
    while (i < len_of_pattern):
        if (pattern[i] == pattern[temp_len]):
            temp_len += 1
            lps[i] = temp_len
            i += 1
        else:
            if (temp_len != 0):
                temp_len = lps[temp_len-1]
            else:
                lps[i] = 0
                i += 1'''

#Algoritma Boyer-Moore
def BoyerMoore(text, pattern): #text, pattern = string
    last = LastOccurenceFunction(pattern)
    t = len(text)
    p = len(pattern)
    i = p-1 # where matching starts
    if (i > t-1):
        return False

    j = p-1
    while (i <= t-1):
        if (pattern[j] == text[i]):
            if (j == 0):
                return True
            else:
                j -= 1
                i -= 1
        else:
            last_occurence = last[ord(text[i])]
            i += (p - min(j, (last_occurence + 1)))

    return False
    
def LastOccurenceFunction(pattern): #pattern = string
    last = [-1 for _ in range(256)] # 256 as in ASCII

    for i in range(len(pattern)):
        last[ord(pattern[i])] = i

    return last

def check(textIn, textDB):
    similarity = 0
    temp_text_In = list(textIn)
    for i in list(textDB):
        if (i in temp_text_In):
            temp_text_In.remove(i)
            similarity += 1

    return (similarity/len(textDB))*100

#temporary dictionary untuk testing program
question_dict = {
    "kamu jeleg" : "pepega",
    "aku siap" : "uwah",
    "aku tidak siap" : "men",
    "kenapa kau" : "aing cool",
    "tapi kan" : "watashi sasuke desu",
    "keluar" : "Bye bye"
}

if __name__ == '__main__':
    while (True):
        u = input(">>> ")
        if (u == "keluar"):
            print(question_dict[u])
            break
        else:
            sudah = False
            #sudah bernilai True jika sudah ada keluaran yang dikeluarkan
            sim = []
            for i, val in question_dict.items():
                if (BoyerMoore(u, i)):
                    print(val)
                    sudah = True
                    break
                else:
                    sim.append([check(u, i), i])

            if (not sudah):
                sim.sort() #terurut membesar, akses elemen terakhir untuk similarity terbesar
                # print(sim[-1][0], sim[-1][1])
                if (sim[-1][0] >= 90): #apabila similarity terbesar >= 90, perintah dijalankan
                    print(question_dict[sim[-1][1]])
                else:
                    print("command tidak ditemukan, apakah maksudmu ini:")
                    for i in range(-1, -4, -1): #print 3 kemungkinan terbesar
                        print("-", sim[i][1])
