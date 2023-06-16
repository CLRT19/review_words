from bs4 import BeautifulSoup
import csv
import requests


# Can only use i smaller than current day
def getCSVByDay(i, url="https://xcx.testdaily.cn/td_wxcx/courseWordsTask/12wLu"):

    num = i
    # Send a GET request to the URL
    response = requests.get(url+convert_i_to_alphabet(i))

    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    # for each item, get the relevant information
    for item in soup.find_all('li', class_='exampleItem'):
        # to avoid grabbing the img tag, we split by newline and grab the first part
        word = item.find('span', class_='span1').text.strip().split('\n')[0]
        pronunciation = item.find_all('span', class_='span2')[0].text.strip()
        transList = item.find_all('span', class_='span2')[
            1].text.strip().split('\n')
        translation = ""
        for i in range(len(transList)):
            if i != len(transList)-1:
                translation += transList[i] + "; "
            else:
                translation += transList[i]
            
        defList = item.find(
            'span', class_='textSpan').text.strip() .split('\n')
        definition = ""
        for i in range(len(defList)):
            if i!= len(defList)-1:
                definition += defList[i] + "; "
            else: 
                definition += defList[i]
        familiarity = '2'
        data.append([word, pronunciation, translation,
                    definition, familiarity])

    # write to CSV
    with open('Day'+str(num)+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Pronunciation', 'Translation',
                        'Definition', 'Familiarity'])  # header
        writer.writerows(data)  # data


def convert_i_to_alphabet(i):
    if i <= 8:
        i += 82  # 83 is the ASCII code for 'S'
    else:
        i += 88
    return chr(i)


for i in range(1, 11):
    getCSVByDay(i)
