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
# Create your views here.
@api_view(["POST"])
def MainProg(inp):
    try:
        #while (True):
        #temporary dictionary untuk testing program
        question_dict = {
            "kamu jeleg" : "pepega",
            "aku siap" : "uwah",
            "aku tidak siap" : "men",
            "kenapa kau" : "aing cool",
            "tapi kan" : "watashi sasuke desu",
            "keluar" : "Bye bye"
        }

        u = str(json.loads(inp.body))
        if (u == "keluar"):
            answer = question_dict[u]
            #break
        else:
            sudah = False
            #sudah bernilai True jika sudah ada keluaran yang dikeluarkan
            sim = []
            for i, val in question_dict.items():
                if (BoyerMoore(u, i)):
                    answer = val
                    sudah = True
                    break
                else:
                    sim.append([check(u, i), i])

            if (not sudah):
                sim.sort() #terurut membesar, akses elemen terakhir untuk similarity terbesar
                # print(sim[-1][0], sim[-1][1])
                if (sim[-1][0] >= 90): #apabila similarity terbesar >= 90, perintah dijalankan
                    answer = question_dict[sim[-1][1]]
                else:
                    answer = "command tidak ditemukan, apakah maksudmu ini:<br>"
                    for i in range(-1, -4, -1): #print 3 kemungkinan terbesar
                        answer += ("- " + sim[i][1] + "<br>")

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

def check(textIn, textDB):
    similarity = 0
    temp_text_In = list(textIn)
    for i in list(textDB):
        if (i in temp_text_In):
            temp_text_In.remove(i)
            similarity += 1

    return (similarity/len(textDB))*100