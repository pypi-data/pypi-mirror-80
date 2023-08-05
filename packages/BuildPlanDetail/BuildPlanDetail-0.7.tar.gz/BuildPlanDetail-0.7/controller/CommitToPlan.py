
from pygerrit2 import GerritRestAPI, HTTPBasicAuth,HTTPDigestAuth

from controller.DB import DB
import requests


__author__ = "houyan"

class CommitToPlan:


    @staticmethod
    def codeCommitWay(partnerId, client, platform):
        codeType = DB.getCodeType(partnerId, client, platform)
        return codeType

    @staticmethod
    def updateGitCommitId(token, projectList, branch, datetext, endDateText):
        commitlist=[]
        for project in projectList:
           # gitUrl = "http://gitlab.qiyi.domain/api/v4/projects/{}/repository/commits?private_token={}&since={}&until={}&per_page=100&page=1&ref_name={}".format(project, token, datetext, endDateText, branch)
            for page in range(1,10):
               gitUrl = "http://gitlab.qiyi.domain/api/v4/projects/{}/repository/commits?private_token={}&since={}&until={}&per_page=100&page={}&ref_name={}".format(
                      project, token, datetext, endDateText,page, branch)
               res = requests.get(gitUrl)
               data2 = res.json()
               if data2==[]:
                   break
               for str_new in data2:
                   commit = [2]
                   commit[0] = str_new['id']
                   commit.append(project)
                   commitlist.append(commit)
               page+=1
        return commitlist


    @staticmethod
    def updateGitCommit(client,commitList,token):
        git_fileList = []
        for cmt in commitList:
            pathurl = "http://gitlab.qiyi.domain/api/v3/projects/{}/repository/commits/{}/diff?private_token={}".format(
                cmt[1], cmt[0], token)
            r2 = requests.get(pathurl)
            data3 = r2.json()
            for str_new in data3:
                file_path = str_new['old_path']
                if client.lower() == "android" :
                    file_path=file_path.split(".")[0]
                   #print(file_path)
                git_fileList.append(file_path)
        git_fileList = list(set(git_fileList))
       # print(git_fileList)
        return git_fileList

    @staticmethod
    def updateGerritRest(gerritUrl, user, password):
        if "https" in gerritUrl:
            auth = HTTPDigestAuth(user, password)
        else:
            auth = HTTPBasicAuth(user, password)
        requests.packages.urllib3.disable_warnings()
        rest = GerritRestAPI(url=gerritUrl, auth=auth, verify=False)
        return rest

    @staticmethod
    def updateGerritId(rest,projectValue, barnchValue, sinceTime, untilTime):
        sinceTime=sinceTime.split(" ")[0]
        untilTime=untilTime.split(" ")[0]
        GERRITE_URL_CHANGE = "/changes/?q=project:%s+status:%s+branch:%s+since:%s+until:%s" % (
            projectValue, 'merged', barnchValue, sinceTime, untilTime)
        #changes = rest.get("/changes/?q=project:paopao_android branch:v11.2.5 status:merged since:2020-03-04 08:04:40.000000000 until:2020-03-05 08:04:40.000000000")
        changes = rest.get(GERRITE_URL_CHANGE)
        changeId = []
        for change in changes:
            change_id = change['id']
            changeId.append(change_id)
        return changeId

    @staticmethod
    def getCaseList(tableName, File):
        caseIDStr = ''
        for file_path in File:
            case_db_id = DB.read(tableName, file_path)
            if len(case_db_id) > 1:
                if len(caseIDStr) == 0:
                    caseIDStr = case_db_id
                else:
                    caseIDStr = caseIDStr + "," + case_db_id
        caseList = caseIDStr.split(",")
        caseList = list(set(caseList))
        #print(caseList)
        return caseList

    @staticmethod
    def getMethodCaseList(tableName, file_method,plan_mapping):
        caseList=[]
        for method_item in file_method:
            file=method_item[0]
            method=method_item[1]
            cmtId=method_item[2]
            cmtId_link=method_item[3]
            case_db_id=""
            file_id = DB.getMethodFileid(tableName,file,method)
            if len(str(file_id))>0:
                case_db_id=DB.getMethodCaseid(tableName, file_id)
            if len(case_db_id) > 0:
                for i in range(len(case_db_id)):
                    case_id=case_db_id[i]
                    case_id_str=str(case_id[0])
                    plan_file_case=[4]
                    plan_file_case[0]=cmtId
                    plan_file_case.append(cmtId_link)
                    plan_file_case.append(file_id)
                    plan_file_case.append(case_id_str)
                    plan_mapping.append(plan_file_case)
                    caseList.append(case_id_str)
        caseList = list(set(caseList))
        return caseList

    @staticmethod
    def caseImportPlan(userName, pasWord,planIdValue,caselist):
        shitu_url = "http://icase.qiyi.domain/caseinplans/caseimport/?planId={}".format(planIdValue)
        #shitu_url = "http://10.16.189.201/caseinplans/caseimport/?planId={}".format(planIdValue)
        user = "user_name=" + userName
        mima = "JSESSIONID=" + pasWord
        headers = {
            "Cookie": user,
            "Cookie": mima,

        }
        suit = []
        pyload = \
            {
                "suites": suit,
                "cases": caselist
            }
        response = requests.post(shitu_url, headers=headers, json=pyload).text
       # print(response)
        return response

    @staticmethod
    def writeDBPlan(tableName,planId,plan_mapping,case_size):
        plan_table=tableName+"_plan"
        DB.deletePlan(plan_table, planId)
        for plan in plan_mapping:
            commit_id=plan[0]
            commit_id_link=plan[1]
            file_id=plan[2]
            case_id=plan[3]
            DB.write_plan_mapping(plan_table, planId, commit_id,commit_id_link,file_id,case_id,case_size)




