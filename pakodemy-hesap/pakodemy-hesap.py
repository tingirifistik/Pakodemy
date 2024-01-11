import requests
from string import ascii_lowercase
from random import choice
from os import system
from time import sleep
from getpass import getpass


while 1:
    system("cls||clear")
    try:
        menu = int(input("1- Puan kazan\n2- Kazandım mı?\n3- Kazanma Olasılığım\n4- Hesapları Sil\n5- Çıkış\n\nSeçim: "))
    except ValueError:
        system("cls||clear")
        print("Hatalı giriş yaptınız. Tekrar deneyiniz.")
        sleep(3)
        continue
    system("cls||clear")
    
    if menu == 1:
        system("cls||clear")
        davet_kodu = str(input("Davet kodu: "))
        system("cls||clear")
        try:
            adet = int(input("Kaç kişi davet edilsin: "))
        except ValueError:
            system("cls||clear")
            print("Doğal sayı yazınız!")
            sleep(3)
            continue
        system("cls||clear")
        x = 1
        while adet > 0:
            try:
                DeviceId = ''.join(choice(ascii_lowercase) for i in range(36))
                random_mail = ''.join(choice(ascii_lowercase) for i in range(11))+str(x)
                ad = choice(open('isimler.txt', encoding="utf-8").read().splitlines())
                soyad = choice(open("soyadlar.txt", encoding="utf-8").read().splitlines()).lower()

                
                url = "https://admin.tosanalytics.com:443/api/Account/registerv4"
                headers = {"User-Agent": "Mozilla/6.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/json-patch+json", "Access-Control-Allow-Origin": "*", "Origin": "https://web.pakodemy.com", "Dnt": "1", "Referer": "https://web.pakodemy.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "Te": "trailers"}
                json={"channelCode": "Web", "deviceId": "?", "email": f"{random_mail}@gmail.com", "isEmailConfirmed": False, "name": ad, "names": ad, "password": "BirVarmisBirYokmus", "surname": soyad, "userName": f"{random_mail}@gmail.com"}
                r = requests.post(url, headers=headers, json=json)
                jwt = r.json()["JwtToken"]
                userid = r.json()["UserId"]
                email = r.json()["Email"]
                
                url = "https://admin.tosanalytics.com:443/api/accountprofile/examcategory/1"
                headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Accept-Encoding": "gzip, deflate", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/468 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9"}
                requests.put(url, headers=headers)
                
                with open("hesaplar.txt", "a", encoding="utf-8")as f:
                    f.write(f"{userid}:{email}:{ad}:{soyad}:{jwt}\n")
                    
                url = "https://admin.tosanalytics.com:443/api/Invitation/enter"
                headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/466 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
                json={"DeviceId": "?"}
                requests.post(url, headers=headers, json=json)

                url = "https://admin.tosanalytics.com:443/api/Invitation/validate"
                headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Authorization": f"Bearer {jwt}", "Access-Control-Allow-Origin": "*", "User-Agent": "Pakodemy/466 CFNetwork/1335.0.3 Darwin/21.6.0", "Accept-Language": "tr-TR,tr;q=0.9", "Accept-Encoding": "gzip, deflate"}
                json={"DeviceId": DeviceId, "InvitationCode": davet_kodu}
                r = requests.post(url, headers=headers, json=json)
                print(f"{x}- {userid} --> "+r.json()["ResponseData"]["Message"])        
                    
                adet-=1
                x+=1
            except:
                print("\nBiraz Bekle!")
                sleep(60)
                system("cls||clear")
                
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
        
    elif menu == 5:
        break
    
    elif menu == 4:
        try:
            with open("hesaplar.txt", "r", encoding="utf-8") as f:
                r = f.read()
        except FileNotFoundError:
            print("Kaydedilmiş bir hesap dosyası yok!")
            sleep(2)
            continue
        x = 1
        for i in (r.strip("\n").split("\n")):
            try:
                userid, jwt = i.split(":")[0], i.split(":")[4]
            except IndexError:
                print("Silinebilecek hesap yok!")
                sleep(3)
                continue
            url = "https://admin.tosanalytics.com:443/api/Account/cancellation"
            headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "User-Agent": "Pakodemy/466 CFNetwork/1335.0.3 Darwin/21.6.0", "Authorization": f"Bearer {jwt}", "Accept-Language": "tr-TR,tr;q=0.9", "Access-Control-Allow-Origin": "*"}
            r = requests.get(url, headers=headers)
            print(f"{x}- {userid} --> "+r.json()["ResponseData"])
            x+=1
        with open("hesaplar.txt", "w") as f:
            pass   
        
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
        try:
            with open("hesaplar.txt", "r", encoding="utf-8") as f:
                line = len(f.read().strip("\n").split("\n"))
        except FileNotFoundError:
            print("hesaplar.txt bulunamadı!")
            sleep(3)
            pass
        print('\n\033[1m'+js["Description"]+'\033[0m'+"\n\nBitiş Tarihi: "+js["EndDate"]+"\nHesabımın kazanma olasılığı: "+str(100*js["UserTicket"]/js["TotalTicket"])+"\nHesabımın ve bot hesaplarının toplam kazanma olasılığı: "+str(100*(js["UserTicket"])/js["TotalTicket"]))
        input("\n\nMenüye dönmek için 'enter' tuşuna basınız..")
    else:
        print("Hatalı giriş yaptınız. Tekrar deneyiniz.")
        sleep(3)
