import logging

import pymysql
import requests
import json


class DB():

    def __init__(self):
        try:
            # 打开数据库连接
            # 连接数据库所需的值，可以在__init__()中传入
            self.conn = pymysql.connect(
                host='bj.mbdtest.w.qiyi.db',
                port=9009,
                user="pingback",
                passwd='PingBack123',
                db="casebycode",
                charset='utf8'
            )
        except Exception as e:
            logging.error(e)
        else:
            logging.info("connect successfully")
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()
        logging.info("close database success")

    def select(self, sql):
        try:
            logging.info(sql)
            self.cur.execute(sql)
            #fetchall()返回的结果是list，list里面再嵌套list
            res = self.cur.fetchone()
            return res
        except Exception as e:
            logging.error(e + "select data fail")

    def select_all(self, sql):
        try:
            logging.info(sql)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            return res
        except Exception as e:
            logging.error(e + "select data fail")
    def update(self, sql):
        logging.info(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            logging.info("update success")
        except Exception as e:
            logging.error(e)
        else:
            logging.info("update success")

    def in_file(self, table, path, method):
        cmd = "select fileid,ispublic from %s where path= '%s' and method= '%s'" % (
        table, path, method)
        result = self.select(cmd)
        return result

    def insert_file(self, table, path, method, ispublic):
        cmd = "insert into %s(path,method,ispublic, isignore) values('%s','%s',%s,1)" % (
        table, path, method, ispublic)
        self.update(cmd)
        cmd1 = "select fileid from %s where path= '%s' and method= '%s'" % (
            table, path, method)
        re = self.select(cmd1)
        return re[0]

    def get_fileid(self, table, path, method):
        cmd = "select fileid from %s where path= '%s' and method= '%s'" % (
            table, path, method)
        re = self.select(cmd)
        return re[0]

    def insert_relation(self, table, fileid, caseid, inuse):
        cmd = "insert into %s(fileid,caseid,inuse) values('%s','%s',%s)" % (table, fileid, caseid, inuse)
        self.update(cmd)

    def get_relation_table(self, file_table, file_id):
        num = int(file_id) % 5
        return file_table+"_0"+str(num)

    @staticmethod
    def write(file_table, basic_case, caseid, cases):
        is_basic = 1
        if int(basic_case) == int(caseid):
            is_basic = 0
        mysql = DB()
        for num in range(0, 5):
            sql = "delete from %s where caseid=%s" % (file_table+"_0"+str(num), caseid)
            mysql.update(sql)
        if is_basic == 1:
            for case in cases:
                result = mysql.in_file(file_table, case.path, case.method)
                if result:
                    relation_table = mysql.get_relation_table(file_table, result[0])
                    if result[1] == 0:
                        mysql.insert_relation(relation_table, result[0], caseid, 1)
                    else:
                        mysql.insert_relation(relation_table, result[0], caseid, 0)
                else:
                    file_id = mysql.insert_file(file_table, case.path, case.method, 1)
                    relation_table = mysql.get_relation_table(file_table, file_id)
                    mysql.insert_relation(relation_table, file_id, caseid, 0)
        else:
            #刷存量数据
            cmd = "update %s set ispublic = 1" % (file_table)
            mysql.update(cmd)
            for num in range(0, 5):
                cmd1 = "update %s set inuse = 0" % (file_table + "_0" + str(num))
                mysql.update(cmd1)
            for case in cases:
                result = mysql.in_file(file_table, case.path, case.method)
                if result:
                    #初始化数据，如以前A文件是公共文件，现不为公共的情况下，需将A映射的关系恢复为非基础数据
                    cmd2 = "update %s set ispublic = 0 where path ='%s' and method ='%s'" % (file_table, case.path, case.method)
                    relation_table = mysql.get_relation_table(file_table, result[0])
                    cmd3 = "update %s set inuse = 1 where fileid =%s" % (relation_table, result[0])
                    mysql.update(cmd2)
                    mysql.update(cmd3)
                    mysql.insert_relation(relation_table, result[0], caseid, 0)
                else:
                    file_id = mysql.insert_file(file_table, case.path, case.method, 0)
                    relation_table = mysql.get_relation_table(file_table, file_id)
                    mysql.insert_relation(relation_table, file_id, caseid, 0)

        mysql.close()

    @staticmethod
    def get_updatetime(case_table, caseid):
        mysql = DB()
        sql ="select updateTime from %s where caseid = %s" %(case_table,caseid)
        result = mysql.select(sql)
        str = 0
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def write_updatetime(case_table,caseid,dtime):
        mysql = DB()
        cmd = "INSERT %s (caseid, updatetime) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE updateTime = %s" % (case_table, caseid, dtime, dtime)
        mysql.update(cmd)
        mysql.close()

    @staticmethod
    def write_plan_mapping(plan_table, plan_id, commit_id,commit_id_link,file_id,case_id,case_size):
        mysql = DB()
        cmd = "insert into %s(plan_id,commit_id,commit_id_link,fileid,case_id,case_totalnum) values('%s','%s','%s' ,'%s' ,'%s','%s')" % (plan_table, plan_id,commit_id,commit_id_link,file_id,case_id,case_size)
        mysql.update(cmd)
        mysql.close()

    @staticmethod
    def read(table, path):
        mysql = DB()
        sql = "select case_id from %s WHERE path like '%s'" % (table, path)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getMethodCase(table, path,method):
        mysql = DB()
        sql = "select case_id from %s WHERE path like '%s' AND  method like '%s'" % (table, path,method)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getMethodCaseXin(table, path, method):
        mysql = DB()
        str = ""
        sql = "select fileid from %s WHERE path like '%s' AND  method like '%s' AND isignore=1" % (table, path, method)
        result = mysql.select(sql)
        if result:
            file_id=result[0]
            table2 = mysql.get_relation_table(table, file_id)
            sql2="select caseid from %s WHERE fileid = '%s' AND inuse=0" % (table2, file_id)
            result2 = mysql.select_all(sql2)
            if result2:
                str=result2
                #print(str)
        mysql.close()
        return str

    '''@staticmethod
    def getMethodCaseXin(table, path, method):
        mysql = DB()
        str = ""
        sql = "select fileid from %s WHERE path like '%s' AND  method like '%s' AND isignore=1" % (table, path, method)
        result = mysql.select(sql)
        if result:
            file_id = result[0]
            table2 = mysql.get_relation_table(table, file_id)
            sql2 = "select caseid from %s WHERE fileid = '%s' AND inuse=0" % (table2, file_id)
            result2 = mysql.select_all(sql2)
            if result2:
                str = result2
                # print(str)
        mysql.close()
        return str'''
    @staticmethod
    def getMethodFileid(table, path, method):
        mysql = DB()
        str = ""
        sql = "select fileid from %s WHERE path like '%s' AND  method like '%s' AND isignore=1" % (table, path, method)
        result = mysql.select(sql)
        if result:
            str=result[0]
        mysql.close()
        return str

    @staticmethod
    def getMethodCaseid(table, file_id):
        mysql = DB()
        str = ""
        table2 = mysql.get_relation_table(table, file_id)
        sql2 = "select caseid from %s WHERE fileid = '%s' AND inuse=0" % (table2, file_id)
        result2 = mysql.select_all(sql2)
        if result2:
            str = result2
        mysql.close()
        return str

    @staticmethod
    def getCodeType(partnerId, client, platform):
        mysql = DB()
        sql = "select codeType from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partnerId, client, platform)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getPartnerName(partnerId):
        mysql = DB()
        sql = "select partnerName from partnerManager WHERE partnerId='%s'" % (partnerId)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getPlatform(partnerId, client):
        mysql = DB()
        sql = "select platform from partnerManager WHERE partnerId='%s'AND client='%s'" % (partnerId, client)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getGitInfo(partnerId, client, platform):
        mysql = DB()
        sql = "select gitId,gitLink from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partnerId, client, platform)
        result = mysql.select(sql)
        mysql.close()
        return result

    @staticmethod
    def getServerGitInfo(partnerId, client, platform):
        mysql = DB()
        sql = "select gitToken,tableName,gitLink from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partnerId, client, platform)
        result = mysql.select(sql)
        mysql.close()
        return result

    @staticmethod
    def getTable(partnerId, client, platform):
        mysql = DB()
        result1 = []
        sql = "select tableName,basicCase from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partnerId, client, platform)
        result = mysql.select(sql)
        if not result:
            logging.error("no matched tableName")
        else:
            result1.append(result[0])
            result1.append(result[0] + "_case")
            if result[1] is None:
                result1.append("0")
            else:
                result1.append(result[1])
        mysql.close()
        return result1

    @staticmethod
    def getGerritInfo(partnerId, client, platform):
        mysql = DB()
        sql = "select gerritUser,gerritPassword, gerritProject,gerritUrl from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partnerId, client, platform)
        result = mysql.select(sql)
        # str = result[0]
        mysql.close()
        return result

    @staticmethod
    def getJob(partner, client, platform):
        mysql = DB()
        sql = "select job from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (partner, client, platform)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        else:
            logging.error("not found")
        mysql.close()
        return str

    @staticmethod
    def getPackage(partner, client, platform):
        mysql = DB()
        sql = "select packageName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (partner, client, platform)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        else:
            logging.error("not found")
        mysql.close()
        return str

    @staticmethod
    def checkPartner(partner):
        mysql = DB()
        sql = "select COUNT(partnerId) as amount from partnerManager WHERE partnerId='%s'" % (partner)
        result = mysql.select(sql)
        mysql.close()
        if result[0] > 0:
            return True
        else:
            return False

    @staticmethod
    def get_ip(partner):
        mysql = DB()
        sql = "select ip from partnerManager WHERE partnerId='%s'" % (partner)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        else:
            logging.error("not found")
        mysql.close()
        return str

    @staticmethod
    def getCaseAutoTable(partner, client, platform):
        mysql = DB()
        sql = "select caseAutoTable from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (partner, client, platform)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getCaseAutoName(partner, client, platform):
        mysql = DB()
        sql = "select caseAutoName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
        partner, client, platform)
        result = mysql.select(sql)
        str = ""
        if result:
            str = result[0]
        mysql.close()
        return str

    @staticmethod
    def getCaseAuto(table,partner, client, platform):
        mysql = DB()
        sql = "select apkJobUser_id,apkJobApi_token,apkJobName,caseJsonUrl,autoTaskId,autoTaskToken,autoTaskName from %s WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
        table,partner, client, platform)
        result = mysql.select(sql)
        mysql.close()
        return result

    @staticmethod
    def updateIgnoreFiles(file_table, rule):
        mysql = DB()
        sql = "update %s set isignore=0 where path like '%s'" % (file_table, rule+"%")
        mysql.update(sql)
        mysql.close()

    @staticmethod
    def updateIgnoreReset(file_table):
        mysql = DB()
        for num in range(0, 5):
            sql = "update %s relation INNER JOIN ( select fileid from %s where isignore=0 AND ispublic=1) file ON relation.fileid = file.fileid set relation.inuse=0 " % (file_table+'_0'+ str(num), file_table)
            mysql.update(sql)

        cmd = "update %s set isignore = 1" % (file_table)
        mysql.update(cmd)

    @staticmethod
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    @staticmethod
    def updateIgnoreRelations(file_table, relation_table, rule):
        mysql = DB()
        sql1 = "update %s relation INNER JOIN ( select fileid from %s where path like " \
               "'%s') file ON relation.fileid = file.fileid set relation.inuse=1 " % (relation_table, file_table, rule+"%")
        mysql.update(sql1)
        mysql.close()

    def select2(self, sql):
        try:
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logging.info(sql)
            # print(sql)
            self.cur.execute(sql)
            #print(sql)
            # fetchall()返回的结果是list，list里面再嵌套list
            res = self.cur.fetchone()
            return res
        except Exception as e:
            logging.error(e + "select data fail")

    def select_all2(self, sql):
        try:
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logging.info(sql)
            # print(sql)
            self.cur.execute(sql)
            # fetchall()返回的结果是list，list里面再嵌套list
            res = self.cur.fetchall()
            return res
        except Exception as e:
            logging.error(e + "select data fail")

    @staticmethod
    def getFiles(caseId, partner, client, platform, ispublic, isignore, offset, limit):
        mysql = DB()
        sql = "select tableName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partner, client, platform)
        tableName = mysql.select(sql)
        if tableName:
            logging.info("table found")
            logging.info(tableName[0])
            sql1 = "select count(*) from %s WHERE caseId='%s' union  all select count(*)  from %s WHERE  " \
                   "caseId='%s'  union  all select count(*) from %s WHERE  caseId='%s' union  all select count(*)  " \
                   "from %s WHERE   caseId='%s' union all  select count(*) from %s WHERE   caseId='%s'" % (
                       tableName[0] + "_00", caseId, tableName[0] + "_01", caseId, tableName[0] + "_02", caseId,
                       tableName[0] + "_03", caseId, tableName[0] + "_04", caseId)
            #print(sql1)
            total = mysql.select_all(sql1)
            totalNum = 0
            for i in total:
                totalNum = totalNum + i[0]

            if limit != '0':
                sql2 = "select fileid  from %s WHERE caseId='%s' union select fileid  from %s WHERE  " \
                   "caseId='%s' union select fileid  from %s WHERE  caseId='%s' union select fileid  " \
                   "from %s WHERE   caseId='%s' union select fileid  from %s WHERE   caseId='%s'  limit %s,%s" % (
                       tableName[0] + "_00", caseId, tableName[0] + "_01", caseId, tableName[0] + "_02", caseId,
                       tableName[0] + "_03", caseId, tableName[0] + "_04", caseId, offset, limit)
            else:
                sql2 = "select fileid  from %s WHERE caseId='%s' union select fileid  from %s WHERE  " \
                       "caseId='%s' union select fileid  from %s WHERE  caseId='%s' union select fileid  " \
                       "from %s WHERE   caseId='%s' union select fileid  from %s WHERE   caseId='%s'" % (
                           tableName[0] + "_00", caseId, tableName[0] + "_01", caseId, tableName[0] + "_02", caseId,
                           tableName[0] + "_03", caseId, tableName[0] + "_04", caseId)
            fileIds = mysql.select_all(sql2)
            #print(len(fileIds))
        else:
            logging.error("not found")
        caseDetails = []

        for fileId in fileIds:
            sql3 = "select path 'filepath', method 'function', IF(isignore = 0,'Y','N') as isignore, IF(ispublic = 0,'Y','N') as ispublic from %s where fileId ='%s'" % (
                tableName[0], fileId[0])
            case = mysql.select2(sql3)
            # print(case)
            caseDetails.append(case)
        #print(caseDetails)
        if isignore!="":
           caseDetails = list(filter(lambda k: (k.get('isignore') == 'Y'), caseDetails))
           totalNum=caseDetails.__len__()
        # print(caseDetails)
        # print(totalNum)
        if ispublic!="":
           caseDetails = list(filter(lambda k: (k.get('ispublic') == 'Y'), caseDetails))
           totalNum = caseDetails.__len__()
        # print(caseDetails)
        # print(totalNum)
        caseDetails = sorted(caseDetails, key=lambda k: (k.get('filepath')), reverse=False)
        # print(caseDetails)
        mysql.close()
        # print(caseDetails)
        # caseDetails = json.dumps(caseDetails, default=caseId.set_default)
        #print(len(caseDetails))
        return caseDetails, totalNum

    @staticmethod
    def getRelations(caseId, partner, client, platform, planid, offset, limit):
        mysql = DB()
        sql = "select tableName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partner, client, platform)
        tableName = mysql.select(sql)
        if tableName:
            logging.info("table found")
            logging.info(tableName[0])
            sql1 = "select fileid  from %s WHERE case_id='%s' and plan_id='%s' limit %s,%s" % (
                tableName[0] + "_plan", caseId, planid, offset, limit)
            allrelation = mysql.select_all(sql1)
            sql3 = "select count(*) from %s WHERE case_id='%s' and plan_id='%s'" % (
                tableName[0] + "_plan", caseId, planid)
            totalNum = mysql.select(sql3)
            sql2 = "select commit_id_link 'commit_id_link'  from %s WHERE case_id='%s' and plan_id='%s' limit %s,%s" % (
                tableName[0] + "_plan", caseId, planid, offset, limit)
            filelinkall = mysql.select_all2(sql2)
            # print(totalNum[0])
            # print(allrelation)
            # print(filelinkall)

        else:
            logging.error("not found")
        caseDetails = []

        for fileid in allrelation:
            sql3 = "select path 'filepath', method 'function', if(isignore=0,'Y','N') as isignore, if(ispublic=0,'Y','N') as ispublic from %s where " \
                   "fileid='%s'" % (
                       tableName[0], fileid[0])
            case = mysql.select2(sql3)
            # print(case)
            caseDetails.append(case)

            # print(caseDetails)

        mysql.close()
        # print(len(caseDetails))
        return caseDetails, totalNum[0], filelinkall

    @staticmethod
    def getCaseNum(partner, client, platform, planid):
        mysql = DB()
        sql = "select tableName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partner, client, platform)
        tableName = mysql.select(sql)
        if tableName:
            logging.info("table found")
            logging.info(tableName[0])
            sql1 = "select count(distinct(case_id)) as caseCount," \
                   "avg(case_totalnum) as casetotalNum from %s WHERE  plan_id='%s'" % (
                       tableName[0] + "_plan", planid)
            caseNum = mysql.select(sql1)
            sql2 = "select DISTINCT case_id  from %s WHERE  plan_id='%s'" % (
                tableName[0] + "_plan", planid)
            caseids = mysql.select_all(sql2)
        #  print(caseNum[0])
        # print(caseids)

        else:
            logging.error("not found")
        mysql.close()
        caseNums = []
        allcaseinfos = []
        for fileid in caseNum:
            caseNums.append(fileid)
        for caseid in caseids:
            caseinfo = {}
            response = requests.get(
                'http://icase.qiyi.domain/case/appFac/5f1666292e77b55888206a4f' + "/" + caseid[0] + "/")
            # print(response.text)
            res = json.loads(response.text)
            casetitle = (res['data']['title'])
            casestep = (res['data']['steps'])
            # print(casetitle)
            caseinfo.update({"caseid": caseid[0]})
            caseinfo.update({"casetitle": casetitle})
            caseinfo.update({"casestep": casestep})
            allcaseinfos.append(caseinfo)
        # print(allcaseinfos)
        return caseNums[0], caseNums[1], allcaseinfos

    @staticmethod
    def getOverviewCase(partner, client, platform, planid, offset, limit):
        mysql = DB()
        sql = "select tableName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partner, client, platform)
        tableName = mysql.select(sql)
        caseNum = 0
        if tableName:
            logging.info("table found")
            logging.info(tableName[0])
            sql1 = "select count(DISTINCT case_id)  from %s WHERE  plan_id='%s'" % (
                tableName[0] + "_plan", planid)
            caseNum = mysql.select(sql1)
           # print(caseNum[0])
            sql2 = "select DISTINCT case_id  from %s WHERE  plan_id='%s' limit %s,%s" % (
                tableName[0] + "_plan", planid, offset, limit)
            caseids = mysql.select_all(sql2)

        else:
            logging.error("not found")
        allresults = []
        for caseid in caseids:
            caseinformation = {}
            caseinformation.update({'caseid': caseid[0]})
            sql = "select fileid as fileids,commit_id_link as commit_id_links from %s where case_id='%s' and plan_id='%s'" % (
                tableName[0] + "_plan", caseid[0], planid)
            allresult = mysql.select_all2(sql)
            # 这是根据 caseid 取文件 id 和提交的记录
            paths = []
            functions = []
            commit_id_link = set()
            fileids = []
            for oneresult in allresult:
                commit_id_link.add(oneresult['commit_id_links'])
                fileids.append(oneresult['fileids'])
                sql = "select path as path,method as function from %s where fileid='%s'" % (
                    tableName[0], oneresult['fileids'])
                fileandfunctions = mysql.select_all2(sql)
                paths.append(fileandfunctions[0]['path'])
                functions.append(fileandfunctions[0]['function'])
            caseinformation.update({'path': paths})
            caseinformation.update({'function': functions})
            caseinformation.update({'len': len(fileids)})
            caseinformation.update({'commit_id_link': commit_id_link})
            allresults.append(caseinformation)
        mysql.close()
        return allresults,caseNum

    @staticmethod
    def getCaseDetail(partner, client, platform, planid, caseid, offset, limit):
        mysql = DB()
        sql = "select tableName from partnerManager WHERE partnerId='%s' AND client='%s' AND platform='%s'" % (
            partner, client, platform)
        tableName = mysql.select(sql)
        caseNum = 0
        if tableName:
            logging.info("table found")
            logging.info(tableName[0])
        else:
            logging.error("not found")

        sql3 = "select count(*) from %s WHERE case_id='%s' and plan_id='%s'" % (
            tableName[0] + "_plan", caseid, planid)
        totalNum = mysql.select(sql3)
        sql = "select fileid as fileids,commit_id_link as commit_id_links from %s where case_id='%s' and plan_id='%s' limit %s,%s" % (
            tableName[0] + "_plan", caseid, planid, offset, limit)
        allresult = mysql.select_all2(sql)
        # 这是根据 caseid 取文件 id 和提交的记录
        allresults = []

        fileids = []
        for oneresult in allresult:
            caseinformation = {}
            caseinformation.update({"filelink": oneresult['commit_id_links']})
            fileids.append(oneresult['fileids'])
            sql = "select path 'path', method  'function' from %s where fileid='%s'" % (
                tableName[0], oneresult['fileids'])
            fileandfunctions = mysql.select_all2(sql)
            caseinformation.update({'filepath': fileandfunctions[0]['path']})
            caseinformation.update({'filefunction': fileandfunctions[0]['function']})
            allresults.append(caseinformation)
        mysql.close()

        #print(allresults)
        return allresults,totalNum[0]


    @staticmethod
    def get_relatedcase_num(partner, client, platform, caseId):
        mysql = DB()
        tableName = mysql.getTable(partner, client, platform)[0]
        if tableName:
            sql2 = "select fileid  from %s WHERE caseId='%s'  union select fileid  from %s WHERE  " \
                   "caseId='%s' union select fileid  from %s WHERE  caseId='%s' union select fileid  " \
                   "from %s WHERE   caseId='%s' union select fileid  from %s WHERE   caseId='%s'" % (
                       tableName + "_00", caseId, tableName + "_01", caseId, tableName + "_02", caseId,
                       tableName + "_03", caseId, tableName + "_04", caseId)
            fileIds = mysql.select_all(sql2)
        else:
            logging.error("not found")

        caseset = set()
        for fileId in fileIds:
            sql = "select isignore from %s WHERE fileId='%s'"% (tableName,  fileId[0])
            isignore = mysql.select(sql)[0]
            if isignore == 1:
                relation_name = mysql.get_relation_table(tableName, fileId[0])
                sql1 = "select caseId from %s WHERE fileId='%s'" % (relation_name,  fileId[0])
                total = mysql.select_all(sql1)
                for i in total:
                    caseset.add(i[0])
        mysql.close()
        totalNum = len(caseset)
        return totalNum

    @staticmethod
    def creat_learning_table(partner, client, platform, caselist):
        mysql = DB()
        tableName = mysql.getTable(partner, client, platform)[0]
        if tableName:
            for caseId in caselist:
                sql2 = "select fileid  from %s WHERE caseId='%s'  union select fileid  from %s WHERE  " \
                       "caseId='%s' union select fileid  from %s WHERE  caseId='%s' union select fileid  " \
                       "from %s WHERE   caseId='%s' union select fileid  from %s WHERE   caseId='%s'" % (
                           tableName + "_00", caseId, tableName + "_01", caseId, tableName + "_02", caseId,
                           tableName + "_03", caseId, tableName + "_04", caseId)
                fileIds = mysql.select_all(sql2)
                for fileId in fileIds:
                    sql = "INSERT INTO mapping13_learn (caseid, fileid) VALUES ('%s','%s') ".format(caseId, fileId[0])
        else:
            logging.error("not found")

        caseset = set()

    @staticmethod
    def getTableCaseCount(table):
        mysql = DB()
        tablename=table+'_case'
        sql = "select count(caseid) from %s " % (
            tablename)
        result = mysql.select(sql)
        str = result[0]
        mysql.close()
        return str

    @staticmethod
    def deletePlan(table,planId):
        mysql = DB()
        #tablename = table + '_plan'
        sql = "delete from %s where plan_id=%s " % (table,planId)
        mysql.update(sql)
        mysql.close()

def traverse_take_field(data, fields, values=[], currentKey=None):
    """遍历嵌套字典列表，取出某些字段的值

    :param data: 嵌套字典列表
    :param fields: 列表，某些字段
    :param values: 返回的值
    :param currentKey: 当前的键值
    :return: 列表
    """
    if isinstance(data, list):
        for i in data:
            traverse_take_field(i, fields, values, currentKey)
    elif isinstance(data, dict):
        for key, value in data.items():
            traverse_take_field(value, fields, values, key)
    else:
        if currentKey in fields:
            values.append(data)
    return values
