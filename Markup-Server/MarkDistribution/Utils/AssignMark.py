import csv
import os

def count_words(string):
    # Split the string into words
    words = string.split()

    # Count the number of words
    num_words = len(words)

    return num_words
def getMark(hwrFinal,fd_sim,FigureTemp,fd_ans):
    isDrawn=0
    Mark_3={}
    Mark_7={}
    Mark_fig=0
    with open('IQA_Files/Result/modified.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Requirement'] == '1' and row['QNO'] in FigureTemp:
                if(len(fd_ans[row['QNO']])>0):
                    isDrawn=1
            if row['Mark'] == '3' and "QNO"+row['QNO'] in hwrFinal.keys():
                if len(hwrFinal["QNO"+row['QNO']])>=300:
                    Mark_3[row['QNO']]=3
                elif len(hwrFinal["QNO"+row['QNO']])>=200:
                    Mark_3[row['QNO']]=2
                elif len(hwrFinal["QNO"+row['QNO']])>=100:
                    Mark_3[row['QNO']]=1
                else:
                    Mark_3[row['QNO']] = 0
            elif row['Mark'] == '7' and "QNO"+row['QNO'] in hwrFinal.keys():
                if row['Requirement'] == '1':
                    if isDrawn==1:
                        if(fd_sim[row['QNO']]>=.4):
                            Mark_fig=2
                        else:
                            Mark_fig=1
                    else:
                        Mark_fig=0
                    if len(hwrFinal["QNO" + row['QNO']]) >= 450:
                        Mark_7[row['QNO']] = 5+Mark_fig
                    elif len(hwrFinal["QNO" + row['QNO']]) >= 400:
                        Mark_7[row['QNO']] = 4+Mark_fig
                    elif len(hwrFinal["QNO" + row['QNO']]) >= 300:
                        Mark_7[row['QNO']] = 3+Mark_fig
                    elif len(hwrFinal["QNO" + row['QNO']]) >= 200:
                        Mark_7[row['QNO']] = 2+Mark_fig
                    elif len(hwrFinal["QNO" + row['QNO']]) >= 100:
                        Mark_7[row['QNO']] = 1+Mark_fig
                    else:
                        Mark_7[row['QNO']] = Mark_fig
                else:
                    if count_words(hwrFinal["QNO" + row['QNO']])>=200:
                        Mark_7[row['QNO']] = 7
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=150:
                        Mark_7[row['QNO']] = 6
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=120:
                        Mark_7[row['QNO']] = 6
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=100:
                        Mark_7[row['QNO']] = 5
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=80:
                        Mark_7[row['QNO']] = 4
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=60:
                        Mark_7[row['QNO']] = 3
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=40:
                        Mark_7[row['QNO']] = 2
                    elif count_words(hwrFinal["QNO" + row['QNO']])>=20:
                        Mark_7[row['QNO']] = 1
                    else:
                        Mark_7[row['QNO']] = 0

    FinalMark={**Mark_3, **Mark_7}
    return FinalMark