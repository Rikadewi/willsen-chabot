from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json

@api_view(["POST"])
def MainProg(inp):
    try:
        #temporary dictionary diambil dari qna.txt
        question_dict = ReadQnA()
        question_dict.update({'keluar' : 'bye bye'})
        #make input lowercase, convert synonym, delete stopwords
        u = DelStopwords(ToSynonym(str(json.loads(inp.body)).lower()))
        if (u == "keluar"):
            answer = question_dict[u]
            #break
        else:
            del question_dict['keluar']
            sudah = False
            #sudah bernilai True jika sudah ada keluaran yang dikeluarkan
            sim = []
            for i, val in question_dict.items():
                pattern = DelStopwords(i)
                if (BoyerMoore(u, pattern)):
                    answer = val
                    sudah = True
                    break
                else:
                    sim.append([check(u, pattern), i])

            if (not sudah):
                sim.sort() #terurut membesar, akses elemen terakhir untuk similarity terbesar
                # print(sim[-1][0], sim[-1][1])
                if (sim[-1][0] >= 90): #apabila similarity terbesar >= 90, perintah dijalankan
                    answer = question_dict[sim[-1][1]]
                else:
                    answer = "command tidak ditemukan, apakah maksudmu ini:\n"
                    for i in range(-1, -4, -1): #print 3 kemungkinan terbesar
                        answer += ("- " + sim[i][1] + "\n")

        return JsonResponse(answer, safe = False)
    except ValueError as ve:
        return Response(ve.args[0], status.HTTP_400_BAD_REQUEST)


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

#Algoritma Knuth-Morris-Pratt
def KnuthMorrisPratt(text, pattern): #text, pattern = string
    t = len(text)
    p = len(pattern)
    #lps = longest prefix suffix
    lps = [0 for _ in range(t)]
    countLongestPrefSuf(lps, pattern, p)

    i = 0; j = 0
    while i < t:
        if (pattern[j] == text[i]):
            i += 1
            j += 1

        if (j == p):
            #pattern found
            return True
        elif (i < t) and (pattern[j] != text[i]):
            if (j != 0):
                j = lps[j-1]
            else:
                i += 1
    return False

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
                i += 1
                
#percentage check
def check(textIn, textDB):
    similarity = 0
    temp_text_In = list(textIn)
    for i in list(textDB):
        if (i in temp_text_In):
            temp_text_In.remove(i)
            similarity += 1

    return (similarity/len(textDB))*100

#QnA, Synonym, Stopword Functions
def ReadQnA():
    qna = open('QnA.txt', 'r', encoding = 'utf8')
    question_dict = {}
    a = qna.read(1)
    while (a != ""):
        temp_pert = []
        while (a != '?'):
            temp_pert.append(a)
            a = qna.read(1)
        temp_pert.append('?')
        pert = ''.join(temp_pert)
        a = qna.read(1)
        a = qna.read(1) #ilangin spasi agar tidak ada pada jawaban
        temp_jaw = []
        while (a != '\n' and a != ""):
            temp_jaw.append(a)
            a = qna.read(1)
        jaw = ''.join(temp_jaw)

        question_dict.update({pert.lower() : jaw})#make question in lowercase
        a = qna.read(1)

    return question_dict

def ReadSynonym():
    synonym = open('Sinonim.txt', 'r', encoding = 'utf8')
    a = synonym.read(1)
    dict_of_syn = {}
    while (a != ""):
        temp_word = []
        while (a != ' '):
            temp_word.append(a)
            a = synonym.read(1)
        word = ''.join(temp_word)
        a = synonym.read(1)#read space
        list_of_syn = []
        while (a != '\n' and a != ''):
            temp_syn = []
            while (a != ' ' and a != '\n' and a != ''):
                temp_syn.append(a)
                a = synonym.read(1)
            syn = ''.join(temp_syn)
            if (a == ' '):
                a = synonym.read(1)
            list_of_syn.append(syn.lower())#make synonym lowercase

        dict_of_syn.update({word.lower() : list_of_syn})#make word lowercase
        a = synonym.read(1)#read \n
    
    return dict_of_syn

def ToSynonym(inp):
    dict_of_syn = ReadSynonym()
    inp_sp = inp.split(' ')
    inp_sp[-1] = inp_sp[-1].replace('?', '')
    
    for i, val in enumerate(inp_sp):
        for key, value in dict_of_syn.items():
            if (val in value):
                inp_sp[i] = key

    inp_final = ' '.join(inp_sp)
    inp_final += '?'
    return inp_final

def ReadStopwords():
    stopword_list = []
    stopwords = open('Stopwords.txt', 'r', encoding = 'utf8')
    a = stopwords.read(1)
    while (a != ''):
        temp_stopword = []
        while (a != '\n' and a != ''):
            temp_stopword.append(a)
            a = stopwords.read(1)
        stopword = ''.join(temp_stopword)
        a = stopwords.read(1)
        stopword_list.append(stopword.lower())#make stopwords lowercase

    return stopword_list

def DelStopwords(inp):
    stopword_list = ReadStopwords()
    inp_sp = inp.split()
    inp_sp[-1] = inp_sp[-1].replace('?', '')
    inp_sp = [i for i in inp_sp if (i not in stopword_list)]

    inp_final = ' '.join(inp_sp)
    inp_final += '?'
    return inp_final