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
import re

# Create your views here.

@api_view(["POST"])
def IdealWeight(heightdata):
    try:
        height=json.loads(heightdata.body)
        weight=str(height*10)
        return JsonResponse("Ideal weight should be:"+weight+" kg",safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

# ======== String Matching ==========

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
                i += 1

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
    for i in textDB:
        if (i in textIn):
            similarity += 1

    return (similarity/len(textDB))*100


question_dict = {
    "kamu jeleg" : "pepega",
    "aku siap" : "uwah",
    "aku tidak siap" : "men",
    "kenapa kau" : "aing cool",
    "tapi kan" : "watashi sasuke desu",
    "keluar" : "Bye bye"
}

@api_view(["POST"])
def stringMatch(stringData):
    try:   
        u = json.loads(stringData.body)
        if (u == "keluar"):
            return JsonResponse(question_dict[u], safe=False)
        else:
            sudah = False
            sim = []
            for i, val in question_dict.items():
                if (BoyerMoore(u, i)):
                    return JsonResponse(val, safe=False)
                    sudah = True
                    break
                else:
                    sim.append([check(u, i), i])
            if (not sudah):
                sim.sort()
            return JsonResponse("sim", safe=False)
                # print("not found, mungkin pake ini:")
                # for i in range(-1, -4, -1):
                #     print("-", sim[i][1])
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def Idealweight(heightdata):
    try:
        height=json.loads(heightdata.body)
        weight=str(height*100)
        return JsonResponse("Ideal weight should be:"+weight+" kg",safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

