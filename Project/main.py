import datetime
import random
import pygame
import pymysql as pms


class MysqlController:
    def __init__(self, host, id, pw, db_name):
        self.conn = pms.connect(host=host, user=id, password=pw, db=db_name, port = 3306, charset='utf8')
        self.curs = self.conn.cursor()

    def insert_total(self, table, total):
        sql = 'INSERT INTO %s VALUES (%s)'
        self.curs.execute(sql%(table, total))
        self.conn.commit()

    def deleteTuple(self, table, where):
        sql = "DELETE FROM %s WHERE %s"
        self.curs.execute(sql %(table, where))
        self.conn.commit()

    def updateTuple(self, table, data, where):
        sql = "UPDATE %s SET %s WHERE %s"%(table, data, where)
        self.curs.execute(sql)
        self.conn.commit()

class QnA(object):
    def __init__(self, mgr_id):
        self.mgr_id = mgr_id

    def uploadAsk(self, id):
        print('\n' + '\033[93m' + "QnA-----------------------------------"+ '\033[0m')
        title = input("제목: ")
        data = "0, '" + input("문의사항을 입력하세요: ") + "', '" + self.mgr_id + "', '" + id + "', '" + title + "'"
        mysql_controller.insert_total("QnA(solved, txt, mgr_ID, asker_ID, Q_Title)", data)
        print("--------------------------------------")

    def showMyQuestion(self, id):
        sql = "select solved, Q_title, txt, answer from QnA where asker_ID = '%s'"%(id)
        mysql_controller.curs.execute(sql)
        ask = mysql_controller.curs.fetchall()
        print('\n' + '\033[93m' + "My_QnA--------------------------------" + '\033[0m')
        isSolved = [" (답변대기)", " (답변완료)"]
        for i in range(len(ask)):
            print(str(i+1) + ": " + ask[i][1] + isSolved[ask[i][0]])
        while(True):
            menu = int(input(("내용을 확인하시려면 번호를 입력하세요(이전: 0): ")))-1
            if menu == -1:
                break
            print("--------------------------------------")
            print("질문내용: " + ask[menu][2])
            if not ask[menu][0]:
                print("답변이 아직 달리지 않았습니다.")
            else:
                print("답변내용: " + ask[menu][3])
            print("--------------------------------------")

    def solveAsk(self):
        sql = "select Q_title, txt, answer, asker_ID, ask_No from QnA where solved = 0 AND mgr_ID = '%s'"%(self.mgr_id)
        mysql_controller.curs.execute(sql)
        ask = mysql_controller.curs.fetchall()
        if(len(ask) == 0):
            print("모든 질문에 답변하셨습니다.")
            return
        print('\n' + '\033[93m' + "Unsolved_QnA------------------------------" + '\033[0m')
        for i in range(len(ask)):
            print(str(i+1) + ": " + ask[i][0] + " -" + ask[i][3])

        while (True):
            menu = int(input(("답변하시려면 번호를 입력하세요(이전: 0): "))) - 1
            if menu == -1:
                break
            print("--------------------------------------")
            print("질문내용: " + ask[menu][1])
            data = "answer = '" + input("답변하기: ") + "', solved = 1"
            mysql_controller.updateTuple("QnA", data ,"ask_No = %s"%(str(ask[menu][4])))
            print("--------------------------------------")

class ManageUser(object):
    def __init__(self, id, pw):
        self.id = id
        self.pw = pw
        sql = "select * from STREAMING_SUBSCRIBER WHERE S_Mgr_ID = '%s'" % (self.id)
        mysql_controller.curs.execute(sql)
        self. user = mysql_controller.curs.fetchall()

    def showUserInfo(self):
        while(True):
            resUser = self.selectUser()
            if resUser == -1:
                return
            yesNo = ["X", "O"]
            print("USER-INFO--------------------------")
            print("아이디: %s"%(resUser[0]))
            print("이름 : %s"%(resUser[2]))
            print("이메일 : %s"%(resUser[4]))
            print("생년월일 : %s"%(resUser[5]))
            print("결제여부 : %s"%(yesNo[resUser[7]]))
            print("-----------------------------------")
            menu = int(input("다른 구독자 정보도 보시겠습니까?(0/1): "))
            if not menu:
                return

    def deleteUser(self):
        res = self.selectUser()
        menu = int(input("정말 삭제하시겠습니까?(0/1): "))
        if not menu:
            return
        where = "S_ID = '%s'"%(res[0])
        mysql_controller.deleteTuple("STREAMING_SUBSCRIBER", where)

    def selectUser(self):
        print("USER-------------------------------")
        for i in range(len(self.user)):
            print(str(i + 1) + ": " + self.user[i][0])
        print("-----------------------------------")
        menu = int(input("구독자를 선택하세요(이전:0): ")) -1
        if menu == -1:
            return -1
        resUser = self.user[menu]
        return resUser

    def deleteManager(self):
        if self.id == 'root':
            print("root 계정은 삭제가 불가능합니다.")
            return False
        npw = input("비밀번호를 입력해주세요: ")
        if npw != self.pw:
            print('\033[91m' + "비밀번호가 잘못되었습니다. 이전으로 돌아갑니다." + '\033[0m')
            return False
        menu = int(input("정말 삭제하시겠습니까?(0/1): "))
        if not menu:
            return False
        # 다른 매니저로 배정
        sql = "select M_ID from MUSIC_MANAGER WHERE M_ID != '%s'" % (self.id)
        mysql_controller.curs.execute(sql)
        mgr = mysql_controller.curs.fetchall()
        n = random.randint(0, len(mgr) - 1)
        where = "S_Mgr_ID = '%s'"%(self.id)
        data = "S_Mgr_ID = '%s'"%(mgr[n][0])
        mysql_controller.updateTuple("STREAMING_SUBSCRIBER", data, where)

        # QnA 넘겨주기
        n = random.randint(0, len(mgr) - 1)
        where = "mgr_ID = '%s'" % (self.id)
        data = "mgr_ID = '%s'" % (mgr[n][0])
        mysql_controller.updateTuple("QnA", data, where)

        # 계정삭제
        mysql_controller.deleteTuple("MUSIC_MANAGER", "M_ID = '%s'"%(self.id))
        return True

class Find(object):
    def __init__(self):
        sql = "select M_ID, M_Pw, M_Ssn from MUSIC_MANAGER"
        mysql_controller.curs.execute(sql)
        m = mysql_controller.curs.fetchall()
        sql = "select S_ID, S_Pw, S_Ssn from STREAMING_SUBSCRIBER"
        mysql_controller.curs.execute(sql)
        s = mysql_controller.curs.fetchall()
        self.idpw = s + m

    def findId(self):
        while(1):
            ssn = input("Ssn을 입력하세요 (이전: 0): ")
            flag = False
            if ssn == '0':
                break
            elif len(ssn) != 13:
                print("잘못 된 입력입니다.")
                continue
            for i in range(len(self.idpw)):
                if self.idpw[i][2] == ssn:
                    print(self.idpw[i][0])
                    flag = True
            if not flag:
                print("존재하지 않는 Ssn입니다.")
                continue
            return

    def findPw(self):
        while (1):
            id = input("ID를 입력하세요 (이전: 0): ")
            if id == '0':
                break
            for i in range(len(self.idpw)):
                if self.idpw[i][0] == id:
                    print(self.idpw[i][1])
                    return
            print("존재하지 않는 ID입니다.")

class SignUp(object):
    def __init__(self):
        print('\n' + '\033[93m' + "SignUp-----------------------------------"+ '\033[0m')
        isMgr = int(input("회원가입 : 0.취소  1.구독자 계정  2.관리자 계정\n"))
        if isMgr == 0:
            return
        sql = "select M_ID from MUSIC_MANAGER"
        mysql_controller.curs.execute(sql)
        self.m_id = mysql_controller.curs.fetchall()
        sql = "select S_ID from STREAMING_SUBSCRIBER"
        mysql_controller.curs.execute(sql)
        s_id = mysql_controller.curs.fetchall()
        self.sm_id = s_id + self.m_id
        if isMgr == 1:
            self.SignUpSubs()
        elif isMgr == 2:
            self.SignUpMgr()
        else:
            print("잘못 된 입력입니다.")

    def SignUpMgr(self):
        while(True):
            menu = 0
            id = input("ID: ")
            for i in range(len(self.sm_id)):
                if id == self.sm_id[i][0]:
                    print("사용할 수 없는 ID 입니다.")
                    print("menu: 1.재입력  2.이전으로")
                    menu = int(input())
                    break
            if menu == 1:
                continue
            elif menu == 2:
                return
            break
        pw = input("PW: ")
        name = input("이름: ")
        ssn = input("Ssn: ")
        mysql_controller.insert_total("MUSIC_MANAGER", '"'+id+'", "'+pw+'", "'+name+'", "'+ssn+'", 1')

    def SignUpSubs(self):
        while (True):
            menu = 0
            id = input("ID: ")
            for i in range(len(self.sm_id)):
                if id == self.sm_id[i][0]:
                    print("사용할 수 없는 ID 입니다.")
                    print("menu: 1.재입력  2.이전으로")
                    menu = int(input())
                    break
            if menu == 1:
                continue
            elif menu == 2:
                return
            break
        pw = input("PW: ")
        name = input("이름: ")
        ssn = input("Ssn: ")
        email = input("Email: ")
        birthDate = input("생년월일(yyyy-mm-dd): ")
        mgrId = self.m_id[random.randrange(len(self.m_id))][0]
        mysql_controller.insert_total("STREAMING_SUBSCRIBER", '"' + id + '", "' + pw + '", "' + name + '", "' + ssn + '", "' + email + '", "' + birthDate + '", "' + mgrId + '", 0')

class checkExist(object):
    def checkExistArtist(self, artist):
        # 존재하는 아티스트인지?
        sql = "select Artist_ID, Nick_Name from Artist"
        mysql_controller.curs.execute(sql)
        artistList = mysql_controller.curs.fetchall()
        aID = -1 # 음수는 안됨..
        for i in range(len(artistList)):
            if artistList[i][1] == artist:
                aID = artistList[i][0]
                break
        return aID

    def checkExistAlbum(self, albumName, aID):
        # 존재하는 앨범인지?
        sql = "select Album_Code, Album_Name from artist_album where Artist_ID = %s" % (str(aID))
        mysql_controller.curs.execute(sql)
        albumList = mysql_controller.curs.fetchall()
        albumId = -1 # 음수는 안됨..
        for i in range(len(albumList)):
            if albumList[i][1] == albumName:
                albumId = albumList[i][0]
                break
        return albumId

    def checkExistAlbumWithoutAid(self, albumName):
        # 존재하는 앨범인지?
        sql = "select Album_Code, Album_Name, Nick_Name from artist_album"
        mysql_controller.curs.execute(sql)
        albumList = mysql_controller.curs.fetchall()
        albumId = [] # 동명의 앨범 나열
        for i in range(len(albumList)):
            if albumList[i][1] == albumName:
                albumId.append(albumList[i])
        if len(albumId) == 0:
            return -1
        return albumId

    def checkExistMusic(self, musicName):
        # 존재하는 음악인지?
        sql = "select ICN, Music_Name, Nick_Name, isTitle, isMain from music_artist"
        mysql_controller.curs.execute(sql)
        musicList = mysql_controller.curs.fetchall()
        ICN = []  # 동명의 음악 나열
        for i in range(len(musicList)):
            if musicList[i][1] == musicName and musicList[i][4] == 1:
                ICN.append(musicList[i])
        if len(ICN) == 0:
            return -1
        return ICN

class Search(checkExist):
    def search(self):
        res = -1
        menu = int(input("menu : 0.이전  1.음원명으로 검색  2.앨범명으로 검색  3.아티스트명으로 검색: "))
        if menu == 0:
            pass
        elif menu == 1:
            mlist = self.searchMusic()
            if mlist == -1:
                res = -1
            else:
                self.searchAndPlay(mlist)
        elif menu == 2:
            res = self.searchAlbum()
            if res != -1:
                self.showAlbumIntroduction(res)
        elif menu == 3:
            res = self.searchArtist()
            if res != -1:
                self.showArtistIntroduction(res)
                menu = int(input("menu: 0.이전  1.앨범보기  2.음원보기: "))
                if menu == 1:
                    self.showArtistsAlbum(res)
                elif menu == 2:
                    self.showArtistsSongs(res)
        return res

    def searchAndPlay(self, mlist):
        print("음악 리스트: ")
        print("MUSIC------------------------------")
        for i in range(len(mlist)):
            print(str(i+1) + ": " + mlist[i][1] + " (" + mlist[i][2] + ")")
        print("-----------------------------------")

    def searchForPlaylist(self):
        res = -1
        menu = int(input("menu : 0.이전  1.음원명으로 검색  2.앨범명으로 검색  3.아티스트명으로 검색: "))
        if menu == 0:
            pass
        elif menu == 1:
            mlist = self.searchMusic()
            if mlist == -1:
                res = -1
            else:
                res = self.selectMusic(mlist)
        elif menu == 2:
            aid = self.searchAlbum()
            mlist = self.returnTrackedSongs(aid)
            if mlist == -1:
                res = -1
            else:
                res = self.selectMusic(mlist)
        elif menu == 3:
            aid = self.searchArtist()
            mlist = self.returnArtistsSongs(aid)
            if mlist == -1:
                res = -1
            else:
                res = self.selectMusic(mlist)
        return res

    def returnArtistsSongs(self, aId):
        sql = "SELECT ICN, Music_Name, Nick_Name, IsTitle, isMain FROM music_artist WHERE Artist_ID = %s" % (str(aId))
        mysql_controller.curs.execute(sql)
        mlist = mysql_controller.curs.fetchall()
        if len(mlist) == 0:
            print("해당 아티스트의 곡이 아직 등록되지 않았습니다.")
            return -1
        print("\n'%s'가 참여한 곡은 다음과 같습니다:" % (mlist[0][2]))
        return mlist

    def showArtistsSongs(self, aId):
        mList = self.returnArtistsSongs(aId)
        if mList == -1:
            return
            print("MUSIC------------------------------")
            for i in range(len(mList)):
                if mList[i][4] == 1:
                    print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]))
                else:
                    sql = "SELECT Nick_Name FROM music_artist WHERE isMain = 1 AND ICN = %s" % (str(mList[i][0]))
                    mysql_controller.curs.execute(sql)
                    mainArtist = mysql_controller.curs.fetchone()[0]
                    print("%s: %s(%s)" % (str(i+1), mList[i][1], mainArtist))
            print("-----------------------------------")

    def returnArtistsAlbum(self, aId):
        sql = "SELECT Album_Name, Nick_Name, Album_Code FROM artist_album WHERE Artist_ID = %s" % (str(aId))
        mysql_controller.curs.execute(sql)
        mlist = mysql_controller.curs.fetchall()
        if len(mlist) == 0:
            print("해당 아티스트의 앨범이 아직 등록되지 않았습니다.")
            return -1
        print("\n'%s'가 작업한 앨범은 다음과 같습니다:" % (mlist[0][1]))
        return mlist

    def showArtistsAlbum(self, aId):
        mList = self.returnArtistsAlbum(aId)
        if mList == -1:
            return
        while(True):
            print("ALBUM------------------------------")
            for i in range(len(mList)):
                print("%s: %s(%s)" % (str(i+1), mList[i][0], mList[i][1]))
            print("-----------------------------------")
            index = int(input("앨범 정보를 확인하고 싶으시면 번호를 입력해주세요(이전:0): "))-1
            if index == -1:
                return
            self.showAlbumIntroduction(mList[index][2])

    def returnTrackedSongs(self, albumCode):
        sql = "SELECT ICN, Music_Name, Nick_Name, IsTitle, isMain FROM music_artist_album WHERE isMain = 1 AND Album_Code = %s"%(str(albumCode))
        mysql_controller.curs.execute(sql)
        mlist = mysql_controller.curs.fetchall()
        if len(mlist) == 0:
            print("수록곡이 아직 등록되지 않았습니다.")
            return -1
        print("\n수록곡은 다음과 같습니다:")
        return mlist

    def showTrackedSongs(self, albumCode):
        mList = self.returnTrackedSongs(albumCode)
        if mList == -1:
            return
        print("MUSIC------------------------------")
        for i in range(len(mList)):
            if mList[i][3]:
                print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]) + '\033[96m' + '(title)' + '\033[0m')
            else:
                print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]))
        print("-----------------------------------")

    def showAlbumIntroduction(self, albumCode):
        sql = "SELECT * FROM album_intro WHERE Album_Code = %s"%(str(albumCode))
        mysql_controller.curs.execute(sql)
        intro = mysql_controller.curs.fetchone()
        print("ALBUM-INFO-------------------------")
        print("앨범이름: %s"%(intro[0]))
        print("아티스트: %s"%(intro[6]))
        print("앨범타입: %s"%(intro[1]))
        print("레이블: %s"% (intro[2]))
        print("발매일: %s"%(str(intro[3])))
        print("발매국가: %s"%(intro[4]))
        print("앨범소개:\n%s"%(intro[5]))
        print("-----------------------------------")

        self.showTrackedSongs(albumCode)

    def showArtistIntroduction(self, aID):
        sql = "SELECT * FROM Artist WHERE Artist_ID = %s" % (str(aID))
        mysql_controller.curs.execute(sql)
        intro = mysql_controller.curs.fetchone()

        sql = "SELECT * FROM MEMBER_OF WHERE Group_ID = %s" % (str(aID))
        mysql_controller.curs.execute(sql)
        member = mysql_controller.curs.fetchall()

        print("ARTIST-----------------------------")

        if len(member) > 0:
            print("그룹명: %s" % (intro[2]))
            print("멤버: ", end='')
            for i in range(len(member)):
                print(member[i][1], end=' ')
            print()
        else:
            print("예명: %s" % (intro[2]))
            print("실명: %s" % (intro[1]))
        print("소속사: %s" % (intro[3]))
        print("데뷔일: %s" % (str(intro[4])))
        print("-----------------------------------")

    def searchMusic(self):
        name = input("음원 이름을 입력해주세요 : ")
        ICN = self.checkExistMusic(name)
        if ICN == -1:
            print("존재하지 않는 음원입니다. 이전으로 돌아갑니다.")
            return -1
        else:
            return ICN

    def selectMusic(self, mList):
        print("음악의 번호를 선택하세요: ")
        print("MUSIC------------------------------")
        for i in range(len(mList)):
            if mList[i][4] == 1:
                print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]))
            else:
                sql = "SELECT Nick_Name FROM music_artist WHERE isMain = 1 AND ICN = %s" % (str(mList[i][0]))
                mysql_controller.curs.execute(sql)
                mainArtist = mysql_controller.curs.fetchone()[0]
                print("%s: %s(%s)" % (str(i+1), mList[i][1], mainArtist))
        print("-----------------------------------")
        sel = int(input())-1
        return mList[sel][0]

    def searchAlbum(self):
        name = input("앨범 이름을 입력해주세요 : ")
        AlbumId = self.checkExistAlbumWithoutAid(name)
        if AlbumId == -1:
            print("존재하지 않는 앨범입니다. 이전으로 돌아갑니다.")
            return -1
        else:
            print("앨범의 번호를 선택하세요: ")
            print("ALBUM------------------------------")
            for i in range(len(AlbumId)):
                print("%s: %s(%s)" % (str(i), AlbumId[i][1], AlbumId[i][2]))
            print("-----------------------------------")
            sel = int(input())
            return AlbumId[sel][0]

    def searchArtist(self):
        name = input("아티스트 이름을 입력해주세요(예명) : ")
        aId = self.checkExistArtist(name)
        if aId == -1:
            print("존재하지 않는 아티스트입니다. 이전으로 돌아갑니다.")
            return -1
        return aId

class Subscriber(Search):
    def __init__(self, id):
        self.myList = []
        sql = "select * from STREAMING_SUBSCRIBER where S_ID = '%s'"%(id)
        mysql_controller.curs.execute(sql)
        rows = mysql_controller.curs.fetchone()
        self.id = rows[0]
        self.pw = rows[1]
        self.name = rows[2]
        self.ssn = rows[3]
        self.email = rows[4]
        self.birth = rows[5]
        self.mgr = rows[6]
        self.right = rows[7]

    def greeting(self):
        print("구독자 계정으로 로그인하셨습니다.")
        self.checkSubsInfo()
        return

    def checkSubsInfo(self):
        sql = "select * from SUBSCRIPTION_INFO where Subs_ID = '%s'" % (self.id)
        mysql_controller.curs.execute(sql)
        rows = mysql_controller.curs.fetchall()

        if len(rows) == 0:
            self.right = 0
            mysql_controller.updateTuple("STREAMING_SUBSCRIBER", "S_Right = 0", "S_ID = '%s'"%(self.id))
            return
        else:
            sql = "select MAX(PaymentDate) from SUBSCRIPTION_INFO where Subs_ID = '%s'" % (self.id)
            mysql_controller.curs.execute(sql)
            row = mysql_controller.curs.fetchone()
            limit = datetime.date.today() - datetime.timedelta(days = 30)
            if row[0] < limit:
                self.right = 0
                mysql_controller.updateTuple("STREAMING_SUBSCRIBER", "S_Right = 0", "S_ID = '%s'"%(self.id))

    def getSubsRight(self):
        if self.right:
            print('\033[95m' + "이미 이용권을 구입하셨습니다." + '\033[0m')
            return
        print('\n' + '\033[93m' + "구독관리-----------------------------------" + '\033[0m')
        card = input("카드 번호를 입력해주세요: ")
        print("30일 이용권: 6000원")
        if int(input("결제하시겠습니까?(0/1): ")):
            price = 6000
            date = datetime.date.today()

            sql = "select MAX(Payment_No) from SUBSCRIPTION_INFO where Subs_ID = '%s'" % (self.id)
            mysql_controller.curs.execute(sql)
            maxNo = mysql_controller.curs.fetchone()[0]

            if maxNo == None:
                maxNo = 0
            else:
                maxNo+=1
            data = '"' + self.id + '", ' + str(maxNo) + ', "' + card + '", ' + str(price) + ', "' + str(date) + '"'
            mysql_controller.insert_total("SUBSCRIPTION_INFO", data)

            self.right = 1
            mysql_controller.updateTuple("STREAMING_SUBSCRIBER", "S_Right = 1", "S_ID = '%s'"%(self.id))
        print("-----------------------------------")

    def myPage(self):
        editPw = False
        while(True):
            print('\n' + "menu : 0.이전  1.회원정보 열람  2.회원정보 수정  3.탈퇴")
            menu = int(input())
            if (menu == 0):
                break
            elif(menu == 1):
                self.showInfo()
            elif(menu == 2):
                editPw = self.editInfo()
            elif (menu == 3):
                if self.deleteAccount():
                    return -1
        return editPw

    def deleteAccount(self):
        npw = input("비밀번호를 입력해주세요: ")
        if (npw != self.pw):
            print('\033[91m' + "비밀번호가 잘못되었습니다. 이전으로 돌아갑니다." + '\033[0m')
            return False
        menu = int(input("정말 삭제하시겠습니까?(0/1): "))
        if not menu:
            return False
        table = "STREAMING_SUBSCRIBER"
        where = "S_ID = '%s'" % (self.id)
        mysql_controller.deleteTuple(table, where)
        return True

    def showInfo(self):
        npw = input("비밀번호를 입력해주세요: ")
        if (npw != self.pw):
            print('\033[91m' + "비밀번호가 잘못되었습니다. 이전으로 돌아갑니다." + '\033[0m')
            return True
        print('\n' + '\033[93m' + "%s님의 개인정보-------" % (self.id) + '\033[0m')
        print("이름: " + self.name)
        print("이메일: " + self.email)
        print("생년월일: " + str(self.birth))
        print("Ssn: " + self.ssn)
        print("-----------------------------------")
        return False

    def editInfo(self):
        if self.showInfo():
            return
        print('\n' + "수정 menu : 0.이전  1.이름  2.비밀번호  3.이메일 :")
        menu = int(input())
        table = "STREAMING_SUBSCRIBER"
        where = "S_ID = '%s'"%(self.id)
        if menu == 1:
            self.name = input("새 이름을 입력해주세요 : ")
            mysql_controller.updateTuple(table, "S_Name = '%s'"%(self.name), where)
        elif menu == 2:
            self.pw = input("새 비밀번호를 입력해주세요 : ")
            mysql_controller.updateTuple(table, "S_Pw = '%s'" % (self.pw), where)
            return True
        elif menu == 3:
            self.email = input("새 이메일을 입력해주세요 : ")
            mysql_controller.updateTuple(table, "Email = '%s'" % (self.email), where)
        return False

    def selectPlaylist(self):
        sql = "select * from PLAYLIST where Constructor_ID = '%s'" % (self.id)
        mysql_controller.curs.execute(sql)
        mylist = mysql_controller.curs.fetchall()
        if (len(mylist) == 0):
            print('\033[95m' + "플레이리스트가 없습니다." + '\033[0m')
            return -1, -1
        print("플레이리스트 선택 : ")
        print("PLAYLIST---------------------------")
        for i in range(len(mylist)):
            print(str(i) + ": " + mylist[i][2])
        print("-----------------------------------")
        sel = mylist[int(input())][1]
        return self.bringPlaylistFromDB(sel)

    def bringPlaylistFromDB(self, sel):
        sql = "select * from playlist_inst where Constructor_ID = '%s' AND L_No = %s ORDER BY Music_No DESC" % (login.id, str(sel))
        mysql_controller.curs.execute(sql)
        playlist = mysql_controller.curs.fetchall()
        return playlist, sel

    def playMusic(self):
        playlist, lno = self.selectPlaylist()
        if playlist == -1:
            return
        for i in range(len(playlist)):
            if playlist[i][4]:
                if self.ageLimit():
                    continue
            music = Music(playlist[i][0], playlist[i][1], playlist[i][2], playlist[i][3], playlist[i][4],
                          playlist[i][5], playlist[i][6], playlist[i][7], playlist[i][8])
            print('\n' + '\033[96m' + music.title + " - %s"%(playlist[i][11]) + '\033[0m')
            end = music.Play()
            if(end):
                break
        return

    def showChart(self):
        menu = int(input("menu : 0.이전  1.HOT10  2.장르별: "))
        if menu == 1:
            sql = "SELECT * FROM music_artist WHERE isMain = 1 ORDER BY Times_Of_Played DESC"
        elif menu == 2:
            genre = ["발라드", "댄스", "록/메탈", "R&B/Soul", "랩/힙합", "인디음악"]
            menu = int(input("menu : 0.이전  1.발라드  2.댄스  3.록/메탈  4.R&B/Soul  5.랩/힙합  6.인디음악  7.해외음악: "))
            if menu > 0 and menu < 7:
                sql = "SELECT * FROM music_artist WHERE GENRE = '%s' AND isMain = 1 ORDER BY Times_Of_Played DESC"%(genre[menu-1])
            elif menu == 7:
                sql = "SELECT * FROM music_artist_album WHERE Nation != '%s' AND isMain = 1 ORDER BY Times_Of_Played DESC" %("대한민국")
            else:
                return -1
        else:
            return -1
        mysql_controller.curs.execute(sql)
        chart = mysql_controller.curs.fetchmany(10)
        print("CHART------------------------------")
        for i in range(len(chart)):
            print(str(i+1) + ": " + chart[i][1] + " (" + chart[i][4] + ")")
        print("-----------------------------------")
        return chart

    def makeMusicInstance(self, ICN):
        if self.checkRights():
            sql = "SELECT * FROM MUSIC WHERE ICN = %s" % (ICN)
            mysql_controller.curs.execute(sql)
            music = mysql_controller.curs.fetchone()
            if music[4]:
                if self.ageLimit():
                    return
            play = Music(music[0], music[1], music[2], music[3], music[4],
                         music[5], music[6], music[7], music[8])
            play.Play()

    def searchAndPlay(self, mlist):
        print("음악 리스트: ")
        print("MUSIC------------------------------")
        for i in range(len(mlist)):
            print(str(i+1) + ": " + mlist[i][1] + " (" + mlist[i][2] + ")")
        print("-----------------------------------")
        while(True):
            if self.wannaPlay(mlist) == -1:
                return

    def wannaPlay(self, mList):
        index = int(input("음악을 플레이하고 싶으시면 번호를 입력해주세요(이전:0): ")) - 1
        if index == -1:
            return -1
        self.makeMusicInstance(mList[index][0])
        return 0

    def getLimitDate(self):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        year = str(int(nowDate[0:4]) - 19)
        return datetime.date.fromisoformat(year + nowDate[4:])

    def ageLimit(self):
        if self.birth > self.getLimitDate():
            print('\033[91m' + "청취 가능한 나이가 아닙니다." + '\033[0m')
            return True
        return False

    def showArtistsSongs(self, aId):
        mList = self.returnArtistsSongs(aId)
        if mList == -1:
            return
        while (True):
            print("MUSIC------------------------------")
            for i in range(len(mList)):
                if mList[i][4] == 1:
                    print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]))
                else:
                    sql = "SELECT Nick_Name FROM music_artist WHERE isMain = 1 AND ICN = %s" % (str(mList[i][0]))
                    mysql_controller.curs.execute(sql)
                    mainArtist = mysql_controller.curs.fetchone()[0]
                    print("%s: %s(%s)" % (str(i + 1), mList[i][1], mainArtist))
            print("-----------------------------------")

            if self.wannaPlay(mList) == -1:
                return

    def showTrackedSongs(self, albumCode):
        mList = self.returnTrackedSongs(albumCode)
        if mList == -1:
            return
        while (True):
            print("MUSIC------------------------------")
            for i in range(len(mList)):
                if mList[i][3]:
                    print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]) + '\033[96m' + '(title)' + '\033[0m')
                else:
                    print("%s: %s(%s)" % (str(i + 1), mList[i][1], mList[i][2]))
            print("-----------------------------------")
            if self.wannaPlay(mList) == -1:
                return

    def managePlaylist(self):
        menu = int(input("menu : 0.이전  1.플레이리스트 생성  2.플레이리스트 수정  3.플레이리스트 보기 : "))
        if menu == 1:
            self.createList()
        elif menu == 2:
            self.editPlaylist()
        elif menu == 3:
            playlist, lno = self.selectPlaylist()
            if playlist == -1:
                return
            self.showPlayList(playlist)
        else:
            return

    def editPlaylist(self):
        playlist, lno = self.selectPlaylist()
        if playlist == -1:
            return
        while(True):
            print("menu : 0.이전  1.곡 추가  2.곡 삭제  3.플레이리스트 삭제 : ")
            menu = int(input())
            if(menu == 1):
                self.addMusic(lno)
            elif(menu == 2):
                playlist, lno = self.bringPlaylistFromDB(lno)
                self.deleteMusic(playlist)
            elif(menu == 3):
                self.deleteList(lno)
                return
            else:
                break
        return

    def addMusic(self, l_no):
        menu = int(input("menu : 0.이전  1.음원차트에서 추가  2.검색으로 추가 : "))
        if menu == 1:
            chart = self.showChart()
            if chart == -1:
                return
            index = int(input("삽입할 곡의 번호(순위)를 선택하세요: "))
            ICN = chart[index-1][0]
        elif menu == 2:
            ICN = self.searchForPlaylist()
            if ICN == -1:
                return

        sql = "select MAX(Music_No) from CONTAIN where Constructor_ID = '%s' AND L_No = %s" % (self.id, str(l_no))
        mysql_controller.curs.execute(sql)
        mysql_controller.curs.execute(sql)
        maxNo = mysql_controller.curs.fetchone()[0]

        if maxNo == None:
            maxNo = 0
        else:
            maxNo += 1

        mysql_controller.insert_total("CONTAIN", '"' + self.id + '", ' + str(l_no) + ', ' + str(ICN) + ', ' + str(maxNo))

    def deleteMusic(self, playlist):
        if len(playlist) < 1:
            print("플레이리스트에 곡이 없습니다.")
            return
        print("몇 번 곡을 삭제하시겠습니까?")
        self.showPlayList(playlist)
        sel = int(input())
        where = "Music_No = %s"%(int(playlist[sel][12]))
        mysql_controller.deleteTuple("CONTAIN", where)

    def showPlayList(self, playlist):
        print("MUSIC-LIST-------------------------")
        for i in range(len(playlist)):
            print(str(i) + ": " + playlist[i][1] + " - %s" % (playlist[i][11]))
        print("-----------------------------------")

    def deleteList(self, lno):
        where = "Constructor_ID = '%s' AND List_No = %s"%(self.id, str(lno))
        mysql_controller.deleteTuple("PLAYLIST", where)
        print('\033[95m' + "삭제되었습니다." + '\033[0m')

    def createList(self):
        name = input("플레이리스트 이름 : ")
        sql = "select MAX(List_No) from PLAYLIST where Constructor_ID = '%s'" % (self.id)
        mysql_controller.curs.execute(sql)
        list_no = mysql_controller.curs.fetchone()[0]
        if list_no == None:
            list_no = 0
        else:
            list_no = list_no + 1

        mysql_controller.insert_total("PLAYLIST", '"' + self.id + '", ' + str(list_no) + ', "' + name + '"')

    def checkRights(self):
        if self.right == 0:
            if int(input('\033[91m' + "사용 가능한 이용권이 없습니다. 이용권을 구매하시겠습니까?(0/1): " + '\033[0m')):
                self.getSubsRight()
            return self.right
        return self.right

class Manager(Search):
    def __init__(self, id):
        sql = "select * from MUSIC_MANAGER where M_ID = '%s'"%(id)
        mysql_controller.curs.execute(sql)
        rows = mysql_controller.curs.fetchone()
        self.id = rows[0]
        self.pw = rows[1]
        self.name = rows[2]
        self.ssn = rows[3]
        self.right = rows[4]

    def greeting(self):
        print("관리자 계정으로 로그인하셨습니다.")

    def upload(self):
        print("menu : 0.이전  1.음원  2.앨범  3.아티스트")
        menu = int(input())
        if menu == 0:
            return
        elif menu == 1:
            self.uploadMusic()
        elif menu == 2:
            self.uploadAlbum(-1)
        elif menu == 3:
            self.uploadArtist()

    def checkDuplicateMusic(self, musicName, aID, albumID):
        sql = "select ICN from music_artist_album where Artist_ID = %s AND Album_Code = %s AND Music_Name = '%s'" % (
        str(aID), str(albumID), musicName)
        mysql_controller.curs.execute(sql)
        musicList = mysql_controller.curs.fetchall()
        if(len(musicList) > 0):
            return True
        return False

    def notExistAlbum(self, aID):
        print('\033[95m' + "존재하지 않는 앨범입니다. 앨범 정보를 먼저 입력해주세요."+ '\033[0m')
        albumId = self.uploadAlbum(aID)
        return albumId

    def notExistArtist(self):
        print('\033[95m' + "존재하지 않는 아티스트입니다. 아티스트 정보를 먼저 입력해주세요."+ '\033[0m')
        aID = self.uploadArtist()
        return aID

    def uploadMusic(self):
        print("음원 정보를 입력하세요 (곡 이름, 앨범 이름, Track 번호, 연령제한, mp3경로, title 여부(0/1), 메인아티스트(예명), 장르): ")
        input_data = input()
        title, albumName, trackNo, ageLimit, link, isTitle, artist ,genre = input_data.split(", ")

        # 임의의 겹치지 않는 ICN 부여
        sql = "select MAX(ICN) FROM MUSIC"
        mysql_controller.curs.execute(sql)
        ICN = mysql_controller.curs.fetchone()[0]

        if ICN == None:
            ICN = 0
        else:
            ICN += 1

        # 존재하는 아티스트인지?
        aID = self.checkExistArtist(artist)
        if aID < 0:
            aID = self.notExistArtist()

        # 존재하는 앨범인지?
        albumId = self.checkExistAlbum(albumName, aID)
        if albumId < 0:
            albumId = self.notExistAlbum(aID)

        # 겹치는 음악 (ID는 다르지만 아티스트 - 앨범 - 이름 다 겹침. -> 잘못된 입력)
        check = self.checkDuplicateMusic(title, aID, albumId)
        if check:
            print('\033[95m' +"이미 동명의 곡이 존재합니다."+ '\033[0m')
            return

        music = Music(ICN, title, albumId, trackNo, ageLimit, link, isTitle, 0, genre)
        data1 = str(ICN) + ', "' + title + '", ' + str(albumId) + ', ' + trackNo + ', ' + ageLimit + ', "' + link + '", ' + isTitle + ', ' + str(0) + ', "' + genre + '"'
        data2 = str(aID) + ', ' + str(ICN)
        music.newMusic(data1, data2)

        self.addFeatArtist(ICN, music)

    def addFeatArtist(self, ICN, music):
        menu = int(input("피쳐링한 가수가 있습니까?(0/1): "))
        if menu == 1:
            feat = input("피쳐링한 가수 목록을 입력하세요(, 로 구분): ").split(', ')
            for i in range(len(feat)):
                # 존재하는 아티스트인지?
                aID = self.checkExistArtist(feat[i])
                if aID < 0:
                    aID = self.notExistArtist()
                data = str(aID) + ', ' + str(ICN)
                music.addFeatArtist(data)

    def uploadArtist(self):
        print("아티스트 정보를 입력하세요 (본명, 예명, 소속사, 데뷔일):")
        input_data = input()
        realName, nickName, agency, debut = input_data.split(", ")

        #임의의 겹치지 않는 ID 부여
        sql = "select MAX(Artist_ID) FROM Artist"
        mysql_controller.curs.execute(sql)
        aID = mysql_controller.curs.fetchone()[0]

        if aID == None:
            aID = 0
        else:
            aID += 1

        artist = Artist(aID, realName, nickName, agency, debut)
        data = str(aID) + ', "' + realName + '", "' + nickName + '", "' + agency + '", "' + debut + '"'
        artist.newArtist(data)

        menu = int(input("그룹 아티스트입니까?(0/1): "))
        if menu:
            memberList = input("그룹 멤버를 입력하세요.(, 로 구분): ").split(', ')
            artist.insertMember(aID, memberList)

        return aID

    def uploadAlbum(self, aID):
        # 임의의 겹치지 않는 ID 부여
        sql = "select MAX(Album_Code) FROM ALBUM"
        mysql_controller.curs.execute(sql)
        albumId = mysql_controller.curs.fetchone()[0]

        if albumId == None:
            albumId = 0
        else:
            albumId += 1

        if aID == -1: # album 바로 입력
            print("앨범 정보를 입력하세요 (앨범이름, 레이블, 앨범타입, 발매일, 발매국가, 아티스트 이름(예명)): ")
            input_data = input()
            albumName, lable, albumtype, release, nation, artist = input_data.split(", ")

            aID = self.checkExistArtist(artist)
            duplicate = self.checkExistAlbum(albumName, aID)
            if duplicate != -1:
                print('\033[95m' + "이미 동명의 앨범이 존재합니다."+ '\033[0m')
                return

        else:
            print("앨범 정보를 입력하세요 (앨범이름, 레이블, 앨범타입, 발매일, 발매국가): ")
            input_data = input()
            albumName, lable, albumtype, release, nation = input_data.split(", ")

        print("앨범 소개 문구를 입력하세요: ")
        intro = input()

        album = Album(albumId, albumName, lable, albumtype, intro, release, nation)
        data1 = str(albumId) + ', "' + albumName + '", "' + lable + '", "' + albumtype + '", "' + intro + '", "' + release + '", "' + nation + '"'
        data2 = str(aID) + ', ' + str(albumId)
        album.newAlbum(data1, data2)
        return albumId

    def delete(self):
        print("menu : 0.이전  1.음원  2.앨범  3.아티스트")
        menu = int(input())
        if menu == 0:
            return
        elif menu == 1:
            self.deleteMusic()
        elif menu == 2:
            print('\033[95m' + "notice: 앨범 내의 모든 음원도 함께 사라집니다." + '\033[0m')
            self.deleteAlbum()
        elif menu == 3:
            print('\033[95m' + "notice: 해당 아티스트가 메인 아티스트인 모든 앨범과, 앨범의 수록곡도 함께 사라집니다." + '\033[0m')
            self.deleteArtist()

    def deleteMusic(self):
        musicName = input("삭제하려는 음악의 제목을 입력하세요: ")
        ICN = self.checkExistMusic(musicName)
        if ICN == -1:
            print('\033[95m' + "'%s' 제목의 음악은 존재하지 않습니다." %(musicName)+ '\033[0m')
            return
        elif len(ICN) > 1:  # 같은 이름의 음악 여러 개
            print("삭제하려는 음악의 번호를 선택하세요: ")
            print("MUSIC-LIST-------------------------")
            for i in range(len(ICN)):
                print("%s: %s(%s)" % (str(i), ICN[i][1], ICN[i][2]))
            print("-----------------------------------")
            sel = int(input())
            resICN = ICN[sel][0]
            data = 'ICN = %s' % (str(resICN))
            mysql_controller.deleteTuple("MUSIC", data)
        else:  # 같은 이름의 음악 1개
            print("'%s(%s)'를 정말 삭제하시겠습니까? (1/0): " % (ICN[0][1], ICN[0][2]))
            sel = int(input())
            if sel:
                resICN = ICN[0][0]
                data = 'ICN = %s'%(str(resICN))
                mysql_controller.deleteTuple("MUSIC", data)

    def deleteAlbum(self):
        albumName, nickName = input("삭제하려는 앨범의 이름과 아티스트 이름을 입력하세요(앨범이름, 아티스트예명): ").split(', ')
        aID = self.checkExistArtist(nickName)
        albumCode = self.checkExistAlbum(albumName, aID)
        if albumCode == -1:
            print('"%s(%s)" 는 존재하지 않는 앨범입니다.'%(albumName, nickName))
            return
        else:  # 같은 이름의 앨범 존재
            print("'%s(%s)'를 정말 삭제하시겠습니까? (1/0): "%(albumName, nickName))
            sel = int(input())
            if sel:
                data = "Album_Code = %s"%(str(albumCode))
                mysql_controller.deleteTuple('ALBUM', data)

    def deleteArtist(self):
        nickName = input("삭제하려는 아티스트의 예명을 입력하세요: ")
        aID = self.checkExistArtist(nickName)
        if aID == -1:
            print('"%s" 는 존재하지 않는 아티스트입니다.' % (nickName))
            return
        else:  # 같은 이름의 아티스트 존재
            print("'%s'를 정말 삭제하시겠습니까? (1/0): "%(nickName))
            sel = int(input())
            if sel:
                # 해당 아티스트가 대표 아티스트인 앨범 지우기
                sql = "select Album_Code from artist_album where Artist_ID = %s"
                mysql_controller.curs.execute(sql%(str(aID)))
                albumList = mysql_controller.curs.fetchall()
                for i in range(len(albumList)):
                    data = "Album_Code = %s" % (str(albumList[i][0]))
                    mysql_controller.deleteTuple('ALBUM', data)

                data = "Artist_ID = %s"%(str(aID))
                mysql_controller.deleteTuple('Artist', data)

    def modify(self):
        print("menu : 0.이전  1.음원  2.앨범  3.아티스트")
        menu = int(input())
        if menu == 0:
            return
        elif menu == 1:
            self.modifyMusic()
        elif menu == 2:
            self.modifyAlbum()
        elif menu == 3:
            self.modifyArtist()

    def modifyMusic(self):
        musicName = input("수정하려는 음악의 제목을 입력하세요: ")
        ICN = self.checkExistMusic(musicName)
        if ICN == -1:
            print('\033[95m' + "'%s' 제목의 음악은 존재하지 않습니다." % (musicName) + '\033[0m')
            return
        elif len(ICN) > 0:  # 같은 이름의 음악 여러 개
            print("수정하려는 음악의 번호를 선택하세요: ")
            print("MUSIC-LIST-------------------------")
            for i in range(len(ICN)):
                print("%s: %s(%s)" % (str(i), ICN[i][1], ICN[i][2]))
            print("-----------------------------------")
            sel = int(input())
            resICN = ICN[sel][0]
            self.showMusicIntroduction(resICN)
            where = 'ICN = %s' % (str(resICN))

            menu = int(input("수정 menu: 0.이전  1.음원이름  2.메인아티스트  3.피쳐링  4.수록앨범  5.경로: "))
            if menu == 1:
                name = input("음원이름: ")
                data = "Music_Name = '%s'" % (name)
                mysql_controller.updateTuple("MUSIC", data, where)
            elif menu == 2:
                name = input("메인아티스트(예명): ")
                aID = self.checkExistArtist(name)
                if aID == -1:
                    print('"%s" 는 존재하지 않는 아티스트입니다.' % (name))
                    return
                else:
                    # 기존 메인 아티스트 삭제
                    data = "isMain = 1 AND M_ICN = %s" % (str(resICN))
                    mysql_controller.deleteTuple("MUSIC_OF", data)
                    # 새 메인 아티스트 입력
                    data = "%s, %s, 1" % (str(aID),str(resICN))
                    mysql_controller.insert_total("MUSIC_OF", data)

            elif menu == 3:
                menu = int(input("기존 피쳐링 가수 목록은 모두 초기화됩니다. 수정하시겠습니까?(0/1) : "))
                if not menu:
                    return
                # 기존 피쳐링 가수 삭제
                data = "isMain = 0 AND M_ICN = %s" % (str(resICN))
                mysql_controller.deleteTuple("MUSIC_OF", data)
                # 새 피쳐링 가수 추가
                feat = input("피쳐링 가수 목록(, 로 구분): ").split(', ')
                for i in range(len(feat)):
                    # 존재하는 아티스트인지?
                    aID = self.checkExistArtist(feat[i])
                    if aID < 0:
                        print('"%s" 는 존재하지 않는 아티스트입니다. 제외하고 입력합니다!' % (feat[i]))
                        continue
                    data = "%s, %s, 0"%(aID, resICN)
                    mysql_controller.insert_total("MUSIC_OF", data)
            elif menu == 4:
                name = input("앨범이름: ")
                albumID = self.checkExistAlbumWithoutAid(name)
                if albumID == -1:
                    print('"%s" 는 존재하지 않는 앨범입니다.' % (name))
                    return
                else:
                    print("앨범의 번호를 선택하세요: ")
                    print("ALBUM------------------------------")
                    for i in range(len(albumID)):
                        print("%s: %s(%s)" % (str(i), albumID[i][1], albumID[i][2]))
                    print("-----------------------------------")
                    sel = int(input())
                    alID = albumID[sel][0]
                    data = "Album_ID = '%s'" % (alID)
                    mysql_controller.updateTuple("MUSIC", data, where)
            elif menu == 5:
                name = input("경로: ")
                data = "Link = '%s'" % (name)
                mysql_controller.updateTuple("MUSIC", data, where)

    def modifyAlbum(self):
        albumName, nickName = input("수정하려는 앨범의 이름과 아티스트 이름을 입력하세요(앨범이름, 아티스트예명): ").split(', ')
        aID = self.checkExistArtist(nickName)
        albumCode = self.checkExistAlbum(albumName, aID)
        if albumCode == -1:
            print('"%s(%s)" 는 존재하지 않는 앨범입니다.' % (albumName, nickName))
            return
        else:  # 같은 이름의 앨범 존재
            self.showAlbumIntroduction(albumCode)
            where = "Album_Code = %s" % (str(albumCode))
            menu = int(input("수정 menu: 0.이전  1.앨범이름  2.레이블  3.앨범타입  4.앨범소개  5.발매일  6.국가  7.아티스트: "))
            if menu == 1:
                name = input("앨범이름: ")
                data = "Album_Name = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 2:
                name = input("레이블: ")
                data = "Lable = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 3:
                name = input("앨범타입: ")
                data = "Album_Type = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 4:
                name = input("앨범소개: ")
                data = "Introduction = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 5:
                name = input("발매일(yyyy-mm-dd): ")
                data = "Release_Date = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 6:
                name = input("국가: ")
                data = "Nation = '%s'" % (name)
                mysql_controller.updateTuple("ALBUM", data, where)
            elif menu == 7:
                name = input("아티스트 예명: ")
                aID = self.checkExistArtist(name)
                if aID == -1:
                    print('"%s" 는 존재하지 않는 아티스트입니다.' % (name))
                    return
                else:
                    where = "Album_ID = %s" % (str(albumCode))
                    data = "A_ID = %s" % (str(aID))
                    mysql_controller.updateTuple("ALBUM_OF", data, where)

    def modifyArtist(self):
        nickName = input("수정하려는 아티스트의 예명을 입력하세요: ")
        aID = self.checkExistArtist(nickName)
        if aID == -1:
            print('"%s" 는 존재하지 않는 아티스트입니다.' % (nickName))
            return
        else:  # 같은 이름의 아티스트 존재
            self.showArtistIntroduction(aID)
            where = "Artist_ID = '%s'"%(str(aID))
            menu = int(input("수정 menu: 0.이전  1.본명  2.예명  3.소속사  4.멤버 : "))
            if menu == 1:
                name = input("본명: ")
                data = "Real_Name = '%s'"%(name)
                mysql_controller.updateTuple("Artist", data, where)
            elif menu == 2:
                name = input("예명: ")
                data = "Nick_Name = '%s'" %(name)
                mysql_controller.updateTuple("Artist", data, where)
            elif menu == 3:
                name = input("소속사: ")
                data = "Agency = '%s'" %(name)
                mysql_controller.updateTuple("Artist", data, where)
            elif menu == 4:
                sql = "select Member_Name from member_list where Artist_ID = %s"%(str(aID))
                mysql_controller.curs.execute(sql)
                member = mysql_controller.curs.fetchall()
                # 기존 멤버 리스트 지우기
                for i in range(len(member)):
                    mysql_controller.deleteTuple("MEMBER_OF", "Member_Name = '%s' AND Group_ID = %s"%(member[i][0], str(aID)))
                # 새 멤버 리스트 받기
                member = input("모든 멤버를 입력하세요(, 로 구분): ").split(', ')
                for i in range(len(member)):
                    mysql_controller.insert_total("MEMBER_OF", str(aID) + ', "' + member[i] + '"')

    def showAlbumIntroduction(self, albumCode):
        sql = "SELECT * FROM album_intro WHERE Album_Code = %s"%(str(albumCode))
        mysql_controller.curs.execute(sql)
        intro = mysql_controller.curs.fetchone()
        print("ALBUM-INFO-------------------------")
        print("앨범이름: %s"%(intro[0]))
        print("아티스트: %s"%(intro[6]))
        print("앨범타입: %s"%(intro[1]))
        print("레이블: %s"% (intro[2]))
        print("발매일: %s"%(str(intro[3])))
        print("발매국가: %s"%(intro[4]))
        print("앨범소개:\n%s"%(intro[5]))
        print("-----------------------------------")

    def showMusicIntroduction(self, ICN):
        sql = "SELECT * FROM music_artist_album WHERE ICN = %s" % (str(ICN))
        mysql_controller.curs.execute(sql)
        intro = mysql_controller.curs.fetchall()
        print("MUSIC-INFO-------------------------")
        print("음원이름: %s" % (intro[0][1]))
        if len(intro) > 1:
            for i in range(len(intro)):
                if intro[i][9]:
                    print("메인아티스트: %s" % (intro[i][4]))
            print("피처링:", end='')
            for i in range(len(intro)):
                if not intro[i][9]:
                    print(" %s" % (intro[i][4]), end='')
            print()
        else:
            print("메인아티스트: %s" % (intro[0][4]))
        print("수록앨범: %s" % (intro[0][6]))
        print("경로: %s" % (intro[0][10]))
        print("-----------------------------------")

    def showMusicStatistics(self):
        menu = int(input("menu: 0.이전  1.전체음원 통계  2.장르별 음원 통계 : "))
        if not menu:
            return

        if menu == 1:
            print("MUSIC-STATISTICS-------------------")
            sql = "SELECT Music_Name, Nick_Name, Times_Of_Played FROM STATISTICS ORDER BY Times_Of_Played DESC"
            mysql_controller.curs.execute(sql)
            musics = mysql_controller.curs.fetchall()
            for i in range(len(musics)):
                print("%s: %s -%s (%s회)"%(str(i+1), musics[i][0], musics[i][1], str(musics[i][2])))
            sql = "SELECT SUM(Times_Of_Played), AVG(Times_Of_Played) FROM STATISTICS"
            mysql_controller.curs.execute(sql)
            stat = mysql_controller.curs.fetchone()
            print("총 플레이 횟수: %s"%(stat[0]))
            print("총 플레이 평균: %s" % (stat[1]))
        elif menu == 2:
            genre = ["발라드", "댄스", "록/메탈", "R&B/Soul", "랩/힙합", "인디음악"]
            index = int(input("menu : 0.이전  1.발라드  2.댄스  3.록/메탈  4.R&B/Soul  5.랩/힙합  6.인디음악 : ")) -1
            if index == -1:
                return
            print("MUSIC-STATISTICS-------------------")
            sql = "SELECT Music_Name, Nick_Name, Times_Of_Played FROM STATISTICS WHERE Genre = '%s' ORDER BY Times_Of_Played DESC"%(genre[index])
            mysql_controller.curs.execute(sql)
            musics = mysql_controller.curs.fetchall()
            for i in range(len(musics)):
                print("%s: %s -%s (%s회)"%(str(i+1), musics[i][0], musics[i][1], str(musics[i][2])))
            sql = "SELECT SUM(Times_Of_Played), AVG(Times_Of_Played) FROM STATISTICS WHERE Genre = '%s'"%(genre[index])
            mysql_controller.curs.execute(sql)
            stat = mysql_controller.curs.fetchone()
            print("총 플레이 횟수: %s" % (stat[0]))
            print("총 플레이 평균: %s" % (stat[1]))
        print("-----------------------------------")

class Music:
    def __init__(self, ICN, title, albumId, trackNo, ageLimit, link, isTitle, times, genre):
        self.ICN = ICN
        self.title = title
        self.albumId = albumId
        self.trackNo = int(trackNo)
        self.ageLimit = int(ageLimit)
        self.link = link
        self.isTitle = int(isTitle)
        self.times = times
        self.genre = genre

    def newMusic(self, data1, data2):
        mysql_controller.insert_total("MUSIC", data1)
        mysql_controller.insert_total("MUSIC_OF", data2 + ', 1')

    def addFeatArtist(self, data):
        mysql_controller.insert_total("MUSIC_OF", data + ', 0')

    def Play(self):
        freq = 16000  # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
        bitsize = -16  # signed 16 bit. support 8,-8,16,-16
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples (experiment to get right sound)
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.load(self.link)
        pygame.mixer.music.play()
        clock = pygame.time.Clock()

        self.times += 1
        mysql_controller.updateTuple("MUSIC", "Times_Of_Played = Times_Of_Played+1", "ICN = %s" % (str(self.ICN)))
        print("menu : 0.stop  1.next  2.pause  3.play  4.replay")
        while pygame.mixer.music.get_busy():
            control = int(input())
            if(control == 0):
                pygame.mixer.music.stop()
                print("-----------------------------------")
                return 1
            elif(control == 1):
                pygame.mixer.music.stop()
            elif (control == 2):
                pygame.mixer.music.pause()
            elif(control == 3):
                pygame.mixer.music.unpause()
            elif(control == 4):
                pygame.mixer.music.rewind()
                self.times += 1
                mysql_controller.updateTuple("MUSIC", "Times_Of_Played = Times_Of_Played+1",
                                             "ICN = %s" % (str(self.ICN)))
            clock.tick(30)
        pygame.mixer.quit()
        print("-----------------------------------")
        return 0

class Album:
    def __init__(self, albumId, albumName, lable, albumtype, intro, release, nation):
        self.code = albumId
        self.name = albumName
        self.lable = lable
        self.albumtype = albumtype
        self.intro = intro
        self.release = release
        self.nation = nation

    def newAlbum(self, data1, data2):
        mysql_controller.insert_total("ALBUM", data1)
        mysql_controller.insert_total("ALBUM_OF", data2)

class Artist:
    def __init__(self, aID, realName, nickName, agency, debut):
        self.ID = aID
        self.realName = realName
        self.nickName = nickName
        self.agency = agency
        self.debut = debut

    def newArtist(self, data):
        mysql_controller.insert_total("Artist", data)

    def insertMember(self, aID, memList):
        for i in range(len(memList)):
            data = str(aID) + ', "' + memList[i] + '"'
            mysql_controller.insert_total("MEMBER_OF", data)

def getIdPw():
    sql = "select M_ID, M_Pw from MUSIC_MANAGER"
    mysql_controller.curs.execute(sql)
    m_id_pw = mysql_controller.curs.fetchall()

    sql = "select S_ID, S_Pw from STREAMING_SUBSCRIBER"
    mysql_controller.curs.execute(sql)
    s_id_pw = mysql_controller.curs.fetchall()

    return m_id_pw, s_id_pw

if __name__ == '__main__':
    mysql_controller = MysqlController('localhost', 'root', 'gdgs1207', 'MUSIC')

    m_id_pw, s_id_pw = getIdPw()

    while(True):
        flag = False
        print('\n' + '\033[93m' + "LOGIN-----------------------------------"+ '\033[0m')
        id = input("ID : ")
        pw = input("PW : ")
        for i in range(len(m_id_pw)):
            if ((id == m_id_pw[i][0] and pw == m_id_pw[i][1])):
                flag = True
                login = Manager(id)
                login.greeting()
                while(True):
                    print('\n' + "menu : 0.로그아웃  1.음원관리  2.계정관리  3.관리자계정 삭제  4.종료")
                    menu = int(input())
                    if(menu == 1):
                        print("menu : 0.이전  1.등록  2.삭제  3.수정  4.통계")
                        menu1 = int(input())
                        if menu1 == 0:
                            pass
                        elif menu1 == 1:
                            login.upload()
                        elif menu1 == 2:
                            login.delete()
                        elif menu1 == 3:
                            login.modify()
                        elif menu1 == 4:
                            login.showMusicStatistics()
                    elif(menu == 2):
                        print("menu : 0.이전  1.계정삭제  2.계정정보 열람  3.QnA 답변")
                        menu1 = int(input())
                        if menu1 == 0:
                            pass
                        elif menu1 == 1:
                            ManageUser(login.id, login.pw).deleteUser()
                        elif menu1 == 2:
                            ManageUser(login.id, login.pw).showUserInfo()
                        elif menu1 == 3:
                            QnA(login.id).solveAsk()
                    elif(menu == 3):
                        if ManageUser(login.id, login.pw).deleteManager():
                            break
                    elif(menu == 4):
                        mysql_controller.curs.close()
                        exit(0)
                    else:
                        break
        for i in range(len(s_id_pw)):
            if ((id == s_id_pw[i][0] and pw == s_id_pw[i][1])):
                flag = True
                login = Subscriber(id)
                login.greeting()
                while(True):
                    print('\n' + "menu : 0.로그아웃  1.음원재생  2.플레이리스트 관리  3.음원차트  4.검색  5.구독관리  6.회원정보  7.문의  8.종료")
                    menu = int(input())
                    if (menu == 1):
                        if login.checkRights():
                            login.playMusic()
                    elif (menu == 2):
                        login.managePlaylist()
                    elif (menu == 3):
                        chart = login.showChart()
                        while(True):
                            if login.wannaPlay(chart) == -1:
                                break
                    elif (menu == 4):
                        login.search()
                    elif (menu == 5):
                        login.getSubsRight()
                    elif (menu == 6):
                        edited = login.myPage()
                        if edited == -1:
                            break
                        if edited:
                           m_id_pw, s_id_pw = getIdPw() # 비밀번호 변경되었으면..
                    elif (menu == 7):
                        ask = int(input("menu: 0.이전  1.질문하기  2.질문보기: "))
                        if ask == 1:
                            QnA(login.mgr).uploadAsk(login.id)
                        elif ask == 2:
                            QnA(login.mgr).showMyQuestion(login.id)
                    elif (menu == 8):
                        mysql_controller.curs.close()
                        exit(0)
                    elif (menu == 0):
                        break

        if flag == False:
            print('\033[91m' + "계정 정보가 일치하지 않습니다." + '\033[0m')
            print('\n' + "menu: 0.돌아가기  1.회원가입  2.아이디 찾기  3.비밀번호 찾기  4.종료")
            menu = int(input())
            if (menu == 1):
                SignUp()
                m_id_pw, s_id_pw = getIdPw()
            elif (menu == 2):
                find = Find()
                find.findId()
            elif(menu == 3):
                find = Find()
                find.findPw()
            elif (menu == 4):
                mysql_controller.curs.close()
                exit(0)