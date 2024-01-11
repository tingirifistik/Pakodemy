import requests
from base64 import b64decode
from Crypto.Cipher import AES
from random import randint
from time import sleep
from os import system, remove
from getpass import getpass


def GetId(jwt):
    a = 1
    while 1:
        if a == 3:
            break
        url = f"https://admin.tosanalytics.com/api/Book/getnestedtitles?={a}"
        headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
        r = requests.get(url,headers=headers)
        dersler = r.json()[0]['Courses']
        x = 0
        with open("gecici.txt", "a", encoding="utf-8") as f:
            while x < len(dersler):
                y = 0
                while y < len(dersler[x]["CourseTopics"]):
                    topic = dersler[x]["CourseTopics"][y]["SubCourseTopics"]
                    z = 0
                    while z < len(topic):
                        id = topic[z]["SubCourseTopicUniqueId"]
                        f.write(str(id)+"\n")
                        z+=1      
                    y+=1
                x+=1
        a+=1
    print("Geçici ID dosyası oluşturuldu\n\nCourseTopicUniqueId dosyası oluşturuluyor.Bu işlem biraz zaman alabilir..\n\n")
  

def Kontrol(jwt):
    with open("gecici.txt", "r+", encoding="utf-8") as f:
        for i in f.read().strip("\n").split("\n"): 
            url = "https://admin.tosanalytics.com:443/api/testsection/createtestsectionv5"
            headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
            json={"ChannelCode": "Web", "AnswerOptionStatus": 0, "DeviceId": "?", "SubCourseTopicId": int(i), "TestSectionType": 2}
            r = requests.post(url, headers=headers, json=json)
            if r.json()["ResponseMessage"] == "Tebrikler! Bu konudan tüm soruları çözdün, yayıncı tercihlerine uygun yeni sorular eklendiğinde bu konudan test çözmeye devam edebilirsin.":
                print(f"{i} numaralı konu çözülmüş!")
                pass
            else:
                with open("CourseTopicUniqueId.txt", "a", encoding="utf-8") as f:
                    f.write(i+"\n")
    system("cls||clear")
    print("ID'ler başarıyla kaydedildi.")
    sleep(1.5)
    remove("gecici.txt")
  

def Decrypt(enc):
    enc = b64decode(enc)
    cipher = AES.new(b'3Snpmd99YZ7fhAJWygrEd8bb5vEmqpR3', AES.MODE_CBC, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    return cipher.decrypt(enc).decode("utf-8").strip("\x00").split("|")


def Sec(kod, cevap):
    saniye = randint(50,120)
    url = "https://admin.tosanalytics.com:443/api/testsection/updatetestsectionelementv2"
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
    json={"AnswerOption": cevap, "Duration": saniye, "TestSectionElementId": kod, "TestSectionElementStatus": 3, "Type": 1, "ChannelCode": "Web"}
    requests.post(url, headers=headers, json=json)


def Bitir(TestNo):
    url = "https://admin.tosanalytics.com:443/api/testsection/finishsectionv3"
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
    json={"TestSectionId": TestNo, "ChannelCode": "Web"}
    r = requests.post(url, headers=headers, json=json)
    return(r.json()["ResponseData"]["LotteryMessage"])

def SoruCoz(jwt):
    with open("CourseTopicUniqueId.txt", "r", encoding="utf-8") as f:
        liste = f.read().strip("\n").split("\n")
    try:
        for i in liste:
            while True:
                ders = int(i)
                system("cls||clear")
                url = "https://admin.tosanalytics.com:443/api/testsection/createtestsectionv5"
                headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
                json={"ChannelCode": "Web", "AnswerOptionStatus": 0, "DeviceId": "?", "SubCourseTopicId": ders, "TestSectionType": 2}
                r = requests.post(url, headers=headers, json=json)
                if r.json()["ResponseMessage"] == "Ooopss...🤪 Biraz hızlı gidiyorsun.":
                    system("cls||clear")
                    print("Ooopss...🤪 Biraz hızlı gidiyorsun.")
                    sleep(60)
                    continue
                elif r.json()["ResponseMessage"] == "Tebrikler! Bu konudan tüm soruları çözdün, yayıncı tercihlerine uygun yeni sorular eklendiğinde bu konudan test çözmeye devam edebilirsin.":
                    system("cls||clear")
                    print(r.json()["ResponseMessage"])
                    sleep(1.5)
                    break
                try:
                    testNo = r.json()["ResponseData"]["TestSectionId"]
                except TypeError:
                    print(r.json()["ResponseMessage"])
                    sleep(1.5)
                    break
                print(f"{testNo} numaralı test oluşturuldu.\n")
                url = "https://admin.tosanalytics.com:443/api/testsection/gettestsectionelementv2"
                headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
                json={"QuestionNumber": 0, "TestSectionId": testNo, "ChannelCode": "Web"}
                r = requests.post(url, headers=headers, json=json)
                kod, cevap = Decrypt(r.json()["CorrectAnswer"])
                Sec(kod, cevap)
                print("1. Soru cevaplandı!")
                while 1:
                    url = "https://admin.tosanalytics.com:443/api/testsection/createtestsectionelementv3"
                    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3.1 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
                    json={"CourseId": 2, "DeviceId": "?", "SubCourseTopicId": ders, "TestSectionId": testNo, "ChannelCode": "Web"}
                    r = requests.post(url, headers=headers, json=json)
                    if r.json()["ResponseMessage"] == "Bu test icin soru sınırına ulaşıldı.":
                        print(f"\n{testNo} numaralı test bitirildi.")
                        print(Bitir(testNo))
                        break
                    try:
                        kod, cevap = Decrypt(r.json()["ResponseData"]["CorrectAnswer"])
                    except TypeError:
                        system("cls||clear")
                        print(r.json()["ResponseMessage"])
                        sleep(1.5)
                        break
                    soru = r.json()["ResponseData"]["QuestionNumber"]
                    Sec(kod, cevap)
                    print(f"{soru}. Soru cevaplandı!")
                sleep(1)
    except KeyboardInterrupt:
        system("cls||clear")
        

while 1:
    system("cls||clear")
    try:
        menu = int(input("1- Test çöz\n2- Kazandım mı?\n3- Kazanma Olasılığım\n4- Konu ID'lerini kaydet\n5- Çıkış\n\nSeçim: "))
    except ValueError:
        system("cls||clear")
        print("Hatalı giriş yaptınız. Tekrar deneyiniz.")
        sleep(3)
        continue
    system("cls||clear")
    if menu == 1:
        mail = str(input("Email: "))
        password = getpass()
        system("cls||clear")
        url = "https://admin.tosanalytics.com:443/api/account/loginV2"
        headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9"}
        json={"DeviceId": "?", "DeviceModel": "iPhone 31 Plus", "DeviceType": 2, "DeviceVersion": "31.6.1", "Email": mail, "OSType": 2, "Password": password, "VersionName": "84.1.29"}
        try:
            jwt = requests.post(url, headers=headers, json=json).json()["JwtToken"]
        except KeyError:
            print("Email veya parola yanlış!")
            sleep(3)
            continue
        try:
            SoruCoz(jwt)
        except FileNotFoundError:
            print("İlk önce konu id'lerini kaydet.")
            sleep(2)
            
    elif menu == 2:
        mail = str(input("Email: "))
        password = getpass()
        system("cls||clear")
        url = "https://admin.tosanalytics.com:443/api/account/loginV2"
        headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9"}
        json={"DeviceId": "?", "DeviceModel": "iPhone 31 Plus", "DeviceType": 2, "DeviceVersion": "31.6.1", "Email": mail, "OSType": 2, "Password": password, "VersionName": "84.1.29"}
        try:
            jwt = requests.post(url, headers=headers, json=json).json()["JwtToken"]
        except KeyError:
            print("Email veya parola yanlış!")
            sleep(3)
            continue
        url = "https://admin.tosanalytics.com:443/api/Lottery/completed"
        headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Authorization": f"Bearer {jwt}", "Accept-Language": "tr-TR,tr;q=0.9", "Access-Control-Allow-Origin": "*"}
        r = requests.get(url, headers=headers).json()["ResponseData"][0]
        print('\n\033[1m'+r["Description"]+'\033[0m'+"\n\nBitiş Tarihi: "+r["EndDate"]+"\nKazandım mı: "+str(r["WinnerUsers"][0]["IsWinner"])+"\nKazananın ismi: "+r["WinnerUsers"][0]["NameSurname"]+"\nKazananın UserId'si: "+str(r["WinnerUsers"][0]["UserId"]))
        input("\n\nMenüye dönmek için 'enter' tuşuna basınız..")
    elif menu == 4:
        mail = str(input("Email: "))
        password = getpass()
        system("cls||clear")
        
        url = "https://admin.tosanalytics.com:443/api/account/loginV2"
        headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9"}
        json={"DeviceId": "?", "DeviceModel": "iPhone 31 Plus", "DeviceType": 2, "DeviceVersion": "31.6.1", "Email": mail, "OSType": 2, "Password": password, "VersionName": "84.1.29"}
        try:
            jwt = requests.post(url, headers=headers, json=json).json()["JwtToken"]
        except KeyError:
            print("Email veya parola yanlış!")
            sleep(3)
            continue
        GetId(jwt)
        Kontrol(jwt)
    elif menu == 3:
        mail = str(input("Email: "))
        password = getpass()
        system("cls||clear")
        
        url = "https://admin.tosanalytics.com:443/api/account/loginV2"
        headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9"}
        json={"DeviceId": "?", "DeviceModel": "iPhone 31 Plus", "DeviceType": 2, "DeviceVersion": "31.6.1", "Email": mail, "OSType": 2, "Password": password, "VersionName": "84.1.29"}
        try:
            jwt = requests.post(url, headers=headers, json=json).json()["JwtToken"]
        except KeyError:
            print("Email veya parola yanlış!")
            sleep(3)
            continue
        url = "https://admin.tosanalytics.com:443/api/Lottery/detail"
        headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Authorization": f"Bearer {jwt}", "Accept-Language": "tr-TR,tr;q=0.9", "Access-Control-Allow-Origin": "*"}
        js = requests.get(url, headers=headers).json()["ResponseData"]["ContinuingLottery"]
        print('\n\033[1m'+js["Description"]+'\033[0m'+"\n\nBitiş Tarihi: "+js["EndDate"]+"\nKazanma olasılığım: "+str(100*js["UserTicket"]/js["TotalTicket"]))
        input("\n\nMenüye dönmek için 'enter' tuşuna basınız..")
    elif menu == 5:
        break
    else:
        print("Hatalı giriş yaptınız. Tekrar deneyiniz.")
        sleep(3)
