from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import csv

s = HTMLSession()

def get_url_check_sbd(sbd):
    #return f'https://diemthi.tuoitre.vn/kythi2019.html?FiledValue={sbd}&MaTruong={sbd[:2]}'
    return f'https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2021&sbd={sbd}'

def getdata(sbd):
    url_diemthi = get_url_check_sbd(sbd=str(sbd))
    response = requests.get(url_diemthi)
    r = s.get(url_diemthi)
    soup = BeautifulSoup(r.text,'html.parser')
    checknone = True
    #if (soup.find_all("Không Tìm thấy kết quả phù hợp") != None) or (soup.find_all("chartefws-of-toan") != None) :
    #    checknone = False
    print(checknone)
    if checknone:
        #sdb = soup.find("span",{"class":"student-id text-dc3545"}).get_text()
        #N1 - Tiếng Anh, N2 - Tiếng Nga, N3 - Tiếng Pháp, N4 - Tiếng Trung, N5 - Tiếng Đức, N6 - Tiếng Nhật.
        if (soup.find_all("N1") != None):
            ngoaingu = "Anh"
        elif (soup.find_all("N2") != None):
            ngoaingu = "Nga"
        elif (soup.find_all("N3") != None):
            ngoaingu = "Phap"
        elif (soup.find_all("N4") != None):
            ngoaingu = "Trung"
        elif (soup.find_all("N5") != None):
            ngoaingu = "Duc"
        elif (soup.find_all("N6")!= None):
            ngoaingu = "Nhat"

        toan = soup.find_all("div",{"class":"font-weight-bold"})
        check = False
        if (soup.find_all("Sinh") != None):
            check = True
        i = 0
        for my_tags in toan:
            i +=1
            if (i==2):
                dtoan = my_tags.string
            if (i==3):
                d1 = my_tags.string
            if (i==4):
                d2 = my_tags.string
            if (i==5):
                d3 = my_tags.string
            if (i==6):
                dvan = my_tags.string
            if (i==7):
                dngoaingu = my_tags.string
        if check:
            tohop = "KHTN"
        else:
            tohop = "KHXH"
        detail = str(sbd) + "," + dtoan + "," + dvan + "," + dngoaingu + "," + d1+ "," + d2+ "," + d3 + "," + tohop + "," + ngoaingu
        with open('Data.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([sbd,dtoan,dvan,dngoaingu,d1,d2,d3])
        print(detail)

def create_sbd(provide_id, post_sbd):
    prefix = ''.join(['0' for i in range(6 - len(str(post_sbd)))])
    # logger.info(prefix)
    return f'{provide_id}{prefix}{post_sbd}'

if __name__ == '__main__':
    lst_provide = ['{0:02}'.format(num) for num in range(33,34)]
    lst_sbd = ['{0:06}'.format(num) for num in range(3748,3751)]
    for provide_id in lst_provide:
        for sbd_num in lst_sbd:
            sbd = str(provide_id) + str(sbd_num)
            print(sbd)
            getdata(sbd)
    #getdata(33003748)
