import requests
import csv
import json
import pandas as pd
import time
checkAll = 1

MaTinh = ['','HaNoi','Tp.HoChiMinh','HaiPhong','DaNang','HaGiang','CaoBang','LaiChau','LaoCai','TuyenQuang','LangSon','BacKan','ThaiNguyen','YenBai','SonLa','PhuTho','VinhPhuc','QuangNinh','BacGiang','BacNinh','','HaiDuong','HungYen','HoaBinh','HaNam','NamDinh','ThaiBinh','NinhBinh','ThanhHoa','NgheAn','HaTinh','QuangBinh','QuangTri','ThuaThien-Hue','QuangNam','QuangNgai','KonTum','BinhDinh','GiaLai','PhuYen','DakLak','KhanhHoa','LamDong','BinhPhuoc','BinhDuong','NinhThuan','TayNinh','BinhThuan','DongNai','LongAn','DongThap','AnGiang','BaRia-VungTau','TienGiang','KienGiang','CanTho','BenTre','VinhLong','TraVinh','SocTrang','BacLieu','CaMau','DienBien','DakNong','HauGiang','CucNhatruong–BoQuocphong'
]

def get_api_sbd(sbd,year):
    return f'https://diemthi.vnanet.vn/Home/SearchBySobaodanhFile?code={sbd}&nam={year}'

def write_to_csv_file(r,provide_id):
    with open(str(provide_id)+"-"+str(MaTinh[int(provide_id)])+'.csv', mode='a',newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([r["Code"],r["Toan"],r["NguVan"],r["NgoaiNgu"],r["VatLi"],r["HoaHoc"],r["SinhHoc"],r["LichSu"],r["DiaLi"],r["GDCD"]])

def get_data(sbd,year,provide_id):
    global checkAll
    api_diemthi = get_api_sbd(sbd=str(sbd),year=str(year))
    response = requests.get(api_diemthi)
    response.encoding='utf-8-sig'
    content = response.text.encode().decode('utf-8-sig')
    content_json = json.loads(content)
    mes = content_json["message"]
    print(len(content))
    if (mes == "success") and (len(content) > 33):
        res = content_json["result"]
        result = res[0]
        write_to_csv_file(result,provide_id)
    else:
        checkAll += 1

if __name__ == '__main__':
    lst_provide = ['{0:02}'.format(num) for num in range(1,2)]
    lst_sbd = ['{0:06}'.format(num) for num in range(0,30)]
    for provide_id in lst_provide:
        with open(str(provide_id)+"-"+str(MaTinh[int(provide_id)])+'.csv', mode='w',newline='') as file:
            writer = csv.writer(    file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["SBD","Toan","NguVan","NgoaiNgu","VatLi","HoaHoc","SinhHoc","LichSu","DiaLi","GDCD"])
        for sbd_num in lst_sbd:
            if (checkAll < 4000):
                sbd = str(provide_id) + str(sbd_num)
                get_data(sbd,str(2021),str(provide_id))
                if (int(sbd_num) % 100 == 0):
                  print(sbd)
            else:
                break
