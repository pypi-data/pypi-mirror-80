import base64
import hashlib
import requests
__author__ = "houyan"

from multiprocessing import Pool

from pygerrit2 import GerritRestAPI
from requests.auth import HTTPDigestAuth, HTTPBasicAuth


class GetMethod:

    @staticmethod
    def getParaGitMethod(cmt,client,token,gitLink,partnerId,platform):
        new_method_change = []
        project = cmt[1]
        pathurl = "http://gitlab.qiyi.domain/api/v3/projects/{}/repository/commits/{}/diff?private_token={}".format(
            cmt[1], cmt[0], token)
        r2 = requests.get(pathurl)
        data3 = r2.json()
        #print('dnagqianid' + cmt[0])
        previous_id = GetMethod.getPreviousId(project, cmt[0], token)
        #git_diiff_url="http://gitlab.qiyi.domain/"+gitLink+"/commit/"+cmt[0]
        git_diiff_url = "http://gitlab.qiyi.domain/" + gitLink + "/commit/" + cmt[0]
        #print(git_diiff_url)
        #print("前一个id"+previous_id)
        cmtId=cmt[0]

        for str_new in data3:
            newPath = str_new['new_path']
            if "." in newPath:
                file_path_sufffix = newPath.split(".")[1]
                file_path_name = newPath.split(".")[0]
                if client.lower() == "android":
                    if file_path_sufffix == "java":
                        #print('文件名称')
                        #print(file_path_name)
                        new_str = GetMethod.getFileStr(project, token, cmt[0], newPath)
                        pre_str = GetMethod.getFileStr(project, token, previous_id, newPath)
                        if pre_str != "":
                            new_method = GetMethod.getAndroidMethodMd5(new_str)  # 新提交的文件方法
                            old_method = GetMethod.getAndroidMethodMd5(pre_str)  # 老的
                            if partnerId=='knowledge' and platform=='plugin':
                                file_path=file_path_name
                            else:
                                file_path=GetMethod.filePathRevert(file_path_name)
                            new_method_change = GetMethod.methodDiff(new_method_change, new_method, old_method,
                                                                     file_path,new_str,pre_str,cmtId,git_diiff_url)
                elif client.lower() == "iphone":
                    if file_path_sufffix=="m" or file_path_sufffix=="h":
                       new_str = GetMethod.getFileStr(project, token, cmt[0], newPath)
                       pre_str = GetMethod.getFileStr(project, token, previous_id, newPath)
                       if pre_str != "":
                          if file_path_sufffix=="m":
                             new_method = GetMethod.getIosMethodMd5(new_str)  # 新提交的文件方法
                             old_method = GetMethod.getIosMethodMd5(pre_str)  # 老的
                          elif file_path_sufffix=="h":
                              new_method = GetMethod.getIosHeadMethodMd5(new_str)  # 新提交的文件方法
                              old_method = GetMethod.getIosHeadMethodMd5(pre_str)  # 老的
                          new_method_change = GetMethod.methodDiff(new_method_change, new_method, old_method,newPath,cmtId,git_diiff_url)
        if len(new_method_change)!=0:
           return new_method_change


    @staticmethod
    def getParallelRun(client,commitList,token,gitLink,partnerId,platform):
        items=commitList
        results=[]
        p=Pool(10)
        for item in items:
            b = p.apply_async(GetMethod.getParaGitMethod, (item, client, token, gitLink,partnerId,platform))
            results.append(b)
        b_result=[item.get() for item in results]
        p.close()
        p.join()
        return b_result

    @staticmethod
    def getParaGerritMethod(gerritId,client,gerritUrl,user,password,gerritProject):
        if "https" in gerritUrl:
            auth = HTTPDigestAuth(user, password)
        else:
            auth = HTTPBasicAuth(user, password)
        requests.packages.urllib3.disable_warnings()
        rest = GerritRestAPI(url=gerritUrl, auth=auth, verify=False)
        new_method_change=[]
        urlId = "/changes/%s/?o=CURRENT_REVISION&o=CURRENT_FILES" % (gerritId)
        changeInfo = rest.get(urlId, verify=False)
        #print(changeInfo)
        changeId=changeInfo['change_id']
        submission_id=changeInfo['submission_id']
        reversion = changeInfo['revisions']
        reversionId = changeInfo['current_revision']
        files_json_string = reversion[reversionId]['files']
        for (fileName, codeInfo) in files_json_string.items():
            cmitid_url=gerritUrl+"/c/"+gerritProject+"/+/"+submission_id+"/1/"+fileName
            if "." in fileName:
                file_path_sufffix = fileName.split(".")[1]
                file_path_name = fileName.split(".")[0]
                if client.lower() == "android":
                    #if file_path_sufffix == "java" or file_path_sufffix == "kt":
                    if file_path_sufffix == "java":
                        file_path=fileName.replace("/","%2F")
                        pre_result = GetMethod.getGerritOldStr(rest, gerritId, reversionId, file_path)
                        change_type=pre_result[0]
                        pre_str=pre_result[1]
                        if pre_str != "":
                            if file_path_sufffix=="java":
                                old_method = GetMethod.getAndroidMethodMd5(pre_str)
                                if change_type == "DELETED":
                                    new_method = {}
                                    new_str=''
                                else:
                                    new_str = GetMethod.getGerritNewStr(rest, gerritId, reversionId, file_path)
                                    new_method = GetMethod.getAndroidMethodMd5(new_str)  # 新提交的文件方法
                            '''elif file_path_sufffix=="kt":
                                old_method = GetMethod.getKtMethodMd5(pre_str)
                                if change_type == "DELETED":
                                    new_method = {}
                                else:
                                    new_str = GetMethod.getGerritNewStr(rest, gerritId, reversionId, file_path)
                                    new_method = GetMethod.getKtMethodMd5(new_str)  # 新提交的文件方法'''
                              # 老的
                            fileRevertName=GetMethod.filePathRevert(file_path_name)
                            new_method_change = GetMethod.methodDiff(new_method_change, new_method, old_method,
                                                                fileRevertName,new_str,pre_str,changeId,cmitid_url)
                elif client.lower() == "iphone":
                    if file_path_sufffix == "m" or file_path_sufffix == "h":
                        file_path = fileName.replace("/", "%2F")
                        pre_result = GetMethod.getGerritOldStr(rest, gerritId, reversionId, file_path)
                        change_type = pre_result[0]
                        pre_str = pre_result[1]
                        if pre_str != "":
                            if file_path_sufffix == "m":
                                old_method = GetMethod.getIosMethodMd5(pre_str)  # 老的
                                if change_type == "DELETED":
                                    new_method = {}
                                else:
                                    new_str = GetMethod.getGerritNewStr(rest, gerritId, reversionId, file_path)
                                    new_method = GetMethod.getIosMethodMd5(new_str)  # 新提交的文件方法
                            elif file_path_sufffix == "h":
                                old_method = GetMethod.getIosHeadMethodMd5(pre_str)  # 老的
                                if change_type == "DELETED":
                                    new_method = {}
                                else:
                                    new_str = GetMethod.getGerritNewStr(rest, gerritId, reversionId, file_path)
                                    new_method = GetMethod.getIosHeadMethodMd5(new_str)  # 新提交的文件方法
                            new_method_change = GetMethod.methodDiff(new_method_change, new_method, old_method,
                                                                     fileName,new_str,pre_str,changeId,cmitid_url)
        return new_method_change

    @staticmethod
    def getGerritParallelRun(gerritIdList,client,gerritUrl,user,password,gerritProject):
        items = gerritIdList
        results = []
        p = Pool(10)
        for item in items:
            b = p.apply_async(GetMethod.getParaGerritMethod, (item, client,gerritUrl,user,password,gerritProject,))
            results.append(b)
        b_result = [item.get() for item in results]
        p.close()
        p.join()
        return b_result


    @staticmethod
    def getPreviousId(project, cmtId, token):
        cmtid_url = "http://gitlab.qiyi.domain/api/v3/projects/{}/repository/commits/{}?private_token={}".format(
            project, cmtId, token)
        cmt_detaial_res = requests.get(cmtid_url)
        cmt_detaial_js = cmt_detaial_res.json()
        parent_ids = cmt_detaial_js['parent_ids']
        previous_id = parent_ids[len(parent_ids) - 1]
        return previous_id

    @staticmethod
    def getFileStr(project, token, cmtId,newPath):
        file_str=""
        fileurl = "http://gitlab.qiyi.domain/api/v3/projects/{}/repository/files?private_token={}&ref={}&file_path={}".format(
            project, token, cmtId, newPath)
        file_res = requests.get(fileurl)
        file_json = file_res.json()
        if "content" in file_json.keys():
            file_content = file_json["content"]
            file_decodestr = base64.b64decode(file_content)
            file_str = str(file_decodestr, encoding="utf8")
        return file_str

    @staticmethod
    def getGerritOldStr(rest,gerritId,revisions,path_str):
        result=[]
        file_str=""
        urlId = "/changes/%s/revisions/%s/files/%s/diff/?" % (gerritId,revisions , path_str)
        file_res = rest.get(urlId, verify=False)
        file_content = file_res['content']
        change_type = file_res['change_type']
        result.append(change_type)
        file_list = []
        for item in file_content:
            if 'ab' in item.keys():
                r_ab = item['ab']
                for item_ab in r_ab:
                    file_list.append(item_ab)
            elif 'a' in item.keys():
                r_a = item['a']
                for item_a in r_a:
                    file_list.append(item_a)
        for old in file_list:
            file_str = file_str + "\n" + old
        result.append(file_str)
        return result

    @staticmethod
    def getGerritNewStr(rest, gerritId, revisions, path_str):
        urlId_new = "/changes/%s/revisions/%s/files/%s/content/?" % (gerritId, revisions, path_str)
        file_str = rest.get(urlId_new, verify=False)
       # print(file_str)
        return file_str
    @staticmethod
    def getIosMethodMd5(file):
        file_list = file.split("\n")
        cnt = 0
        dic = {}
        for file_hang in file_list:
            if "- (" in file_hang or "+ (" in file_hang:
                 if ";" not in file_hang and "//" not in file_hang:
                   # print("方法")
                   # print(file_hang)
                    md5_result = GetMethod.getIosMd5(file, cnt)
                    method_md5 = md5_result[1]
                    menthod_hang = file_hang.split(")")
                    methodStr=menthod_hang[1]
                    if ":" in methodStr:
                        method2=methodStr.split(":")
                        method= method2[0]
                    elif " {" in methodStr:
                        method3=methodStr.split(" {")
                        method=method3[0]
                    else:
                        method=methodStr

                    dic[method] = method_md5
            cnt += 1
        return dic

    @staticmethod
    def getIosHeadMethodMd5(file):
        file_list = file.split("\n")
        dic = {}
        for file_hang in file_list:
            if "- (" in file_hang or "+ (" in file_hang:
                if ";" in file_hang:
                    m = hashlib.md5()
                    m.update(file_hang.encode("utf8"))
                    method_md5 = m.hexdigest()
                    menthod_hang = file_hang.split(")")
                    methodStr = menthod_hang[1]
                    if ":" in methodStr:
                        method2 = methodStr.split(":")
                        method=method2[0]
                    else:
                        method = methodStr

                    dic[method] = method_md5
        return dic

    @staticmethod
    def getIosMd5(file2, start):
        file_list = file2.split("\n")
        result = {}
        method_str = ""
        cb = 0  # 花括号个数
        for i, val in enumerate(file_list, start):
            val = file_list[i]
           # print(val)
            if "//" not in val:
                if "{}" in val:
                    val = val.replace("{}", "")
                if "{" in val:
                    cb = cb + 1
                if "}}" in val:
                    cb=cb-2
                elif "}" in val:
                    cb = cb - 1
                if "}" in val and cb == 0:
                    result[0] = i
                    m = hashlib.md5()
                    method_str = method_str + val
                    m.update(method_str.encode("utf8"))
                    method_md5 = m.hexdigest()
                    result[1] = method_md5
                    break
            method_str = method_str + val
        return result

    @staticmethod
    def getKtMethodMd5(file):
        file_list = file.split("\n")
        cnt = 0
        dic = {}
        for file_hang in file_list:
            if "fun" in file_hang and "{" in file_hang:
                    md5_result = GetMethod.getKtMd5(file, cnt, file_hang)
                    method_md5 = md5_result[1]
                    menthod_hang = file_hang.split(" ")
                    for methodStr in menthod_hang:
                        if "(" in methodStr:
                            end = methodStr.find('(')
                            method = methodStr[0:end]
                    dic[method] = method_md5
            cnt += 1
        return dic

    @staticmethod
    def getKtMd5(file2, start, method_name):
        file_list = file2.split("\n")
        result = {}
        method_str = ""
        cb = 0  # 花括号个数
        qiantao_cb = 0
        for i, val in enumerate(file_list, start):
            val = file_list[i]
            if qiantao_cb != 0:
                qiantao_cb = qiantao_cb - 1
            if "fun" in val and method_name not in val:
                    qiantao_cb = GetMethod.getKtQtLineNum(file2, i)
            if qiantao_cb == 0:
                if "{" in val:
                    if "//" in val:
                        cb=cb
                    else:
                       cb = cb + 1
                if "}" in val:
                    if "//" in val:
                        cb=cb
                    else:
                        cb = cb - 1
                if "}" in val and cb == 0:
                    result[0] = i
                    m = hashlib.md5()
                    method_str = method_str + val
                    m.update(method_str.encode("utf8"))
                    method_md5 = m.hexdigest()
                    result[1] = method_md5
                    break
                method_str = method_str + val
        return result

    @staticmethod
    def getKtQtLineNum(file3, qt_start):
        file_list3 = file3.split("\n")
        qiantao_cb = 0
        qt_cnt = 0
        for i, qt_val in enumerate(file_list3, qt_start):
            qt_val = file_list3[i]
            qt_cnt = qt_cnt + 1
            # print(qt_val)
            if "{}" in qt_val:
                qiantao_cb = 0
                break;
            if "{" in qt_val:
                qiantao_cb = qiantao_cb + 1
            if "}" in qt_val:
                qiantao_cb = qiantao_cb - 1
            if "}" in qt_val and qiantao_cb == 0:
                break
        return qt_cnt

    @staticmethod
    def getAndroidNotMethodMd5(file):
        file_list = file.split("\n")
        dic = {}
        method_str=""
        cnt_satrt=0
        for cnt, file_hang in enumerate(file_list,cnt_satrt):
            if "public" in file_hang or "private" in file_hang or "protected" in file_hang:
                if "class" not in file_hang  and ";" in file_hang:
                    method_str=method_str+file_hang
                    cnt_satrt+=1
                elif "{" in file_hang and "class" not in file_hang and "(" in file_hang:
                    cb=0
                    start=cnt
                    for mcnt, val in enumerate(file_list,start):
                        if "{" in val:
                            cb+=1
                        if "}" in val:
                            cb-=1
                        if "}" in val and cb == 0:
                            cnt+=1
                            break
                        cnt_satrt+=1
        #print(method_str)
        m = hashlib.md5()
        m.update(method_str.encode("utf8"))
        method_md5 = m.hexdigest()
        method="NONE"
        dic[method]=method_md5;
        return dic

    @staticmethod
    def getAndroidMethodMd5(file):
        file_list = file.split("\n")
        cnt = 0
        dic = {}
        for file_hang in file_list:
            if "public" in file_hang or "private" in file_hang or "protected" in file_hang:
                if "{" in file_hang and "class" not in file_hang and "(" in file_hang:
                    #print("方法")
                    md5_result = GetMethod.getAndroidMd5(file, cnt,file_hang)
                    method_md5 = md5_result[1]
                    menthod_hang = file_hang.split(" ")
                    for methodStr in menthod_hang:
                        if "(" in methodStr:
                            end = methodStr.find('(')
                            method = methodStr[0:end]
                    dic[method] = method_md5
            cnt += 1
        return dic


    @staticmethod
    def getAndroidMd5(file2, start,method_name):
        file_list = file2.split("\n")
        result = {}
        method_str = ""
        cb=0#花括号个数
        qiantao_cb=0
        for i, val in enumerate(file_list, start):
            val = file_list[i]
            if qiantao_cb!=0:
                qiantao_cb=qiantao_cb-1
            if "public" in val or "private" in val or "protected" in val:
                if "{" in val and "class" not in val and "(" in val and method_name not in val:
                    #print('嵌套')
                    #print(val)
                    qiantao_cb= GetMethod.getAndroidQtLineNum(file2,i)
            if qiantao_cb==0:
                if "{" in val:
                    cb = cb + 1
                if "}" in val:
                    cb = cb - 1
                if "=======" in val:
                    result[0] = i
                    m = hashlib.md5()
                    method_str = method_str + val
                    m.update(method_str.encode("utf8"))
                    method_md5 = m.hexdigest()
                    result[1] = method_md5
                    break
                if "}" in val and cb == 0:
                    result[0] = i
                    m = hashlib.md5()
                    method_str = method_str + val
                    m.update(method_str.encode("utf8"))
                    method_md5 = m.hexdigest()
                    result[1] = method_md5
                    break
                method_str = method_str + val
        return result

    @staticmethod
    def getAndroidQtLineNum(file3, qt_start):
        file_list3 = file3.split("\n")
        qiantao_cb = 0
        qt_cnt = 0
        for i, qt_val in enumerate(file_list3, qt_start):
            qt_val = file_list3[i]
            qt_cnt = qt_cnt + 1
           # print(qt_val)
            if "{" in qt_val and "\\" not in qt_val:
                qiantao_cb = qiantao_cb + 1
            if "}" in qt_val and "\\" not in qt_val:
                qiantao_cb = qiantao_cb - 1
            if "}" in qt_val and qiantao_cb == 0 and"\\" not in qt_val:
                break
        return qt_cnt

    @staticmethod
    def methodDiff(new_method_change,new_method,old_method,file_path_name,new_str,pre_str,cmtId,git_diiff_url):
        method_Change_bol=False
        for key in new_method.keys():
            new_value = new_method[key]
            if key in old_method.keys():
                old_value = old_method[key]
                if new_value != old_value:
                    change_item = str(key)
                    method_change = [4]
                    method_change[0] = file_path_name
                    method_change.append(change_item)
                    method_change.append(cmtId)
                    method_change.append(git_diiff_url)
                    new_method_change.append(method_change)
                    method_Change_bol=True
            else:
                method_add = [4]
                method_add[0] = file_path_name
                method_add.append(str(key))
                method_add.append(cmtId)
                method_add.append(git_diiff_url)
                new_method_change.append(method_add)
        for old_key in old_method.keys():
            if old_key not in new_method.keys():
                method_delete = [4]
                method_delete[0] = file_path_name
                method_delete.append(str(old_key))
                method_delete.append(cmtId)
                method_delete.append(git_diiff_url)
                method_Change_bol = True
                new_method_change.append(method_delete)
        if method_Change_bol==False:
            new_not_method=GetMethod.getAndroidNotMethodMd5(new_str)
            old_not_method=GetMethod.getAndroidNotMethodMd5(pre_str)
            if new_not_method["NONE"] != old_not_method["NONE"]:
                method_not=[4]
                method_not[0]=file_path_name
                method_not.append("NONE")
                method_not.append(cmtId)
                method_not.append(git_diiff_url)
                new_method_change.append(method_not)
        return new_method_change
    @staticmethod
    def methodDeal(method):
        while None in method:
            method.remove(None)
        method_list=[]
        for sub in method:
            for sub_item in sub:
                 method_list.append(sub_item)
        method_str=[]
        file_method_list=[]
        for path_method in method_list:
            path_item=path_method[0]
            method_item=path_method[1]
            cmt_id=path_method[2]
            cmt_id_url=path_method[3]
            methd_add=path_item+method_item
            if methd_add not in method_str:
                file_method = [4]
                method_str.append(methd_add)
                file_method[0] = path_item
                file_method.append(method_item)
                file_method.append(cmt_id)
                file_method.append(cmt_id_url)
                #print(file_method)
                file_method_list.append(file_method)
               # print(file_method_list)
        return file_method_list

    @staticmethod
    def filePathRevert(file_path):
        #print(file_path)
        if '/source' in file_path:
            file = file_path.split('/source')
        elif '/src' in file_path:
            file = file_path.split('/src')
        file_qian = file[0]
        fileQ = file_qian.split('/')
        index = len(fileQ) - 1
        file_src_qian = fileQ[index]
        file_hou = file[1]
        if '/main/java' in file_hou:
            fileH = file_hou.split('/main/java')
            file_src_hou = fileH[1]

        elif '/org/' in file_hou:
            fileH = file_hou.split('/org')
            file_src_hou = '/org' + fileH[1]

        elif '/com/' in file_hou:
            fileH = file_hou.split('/com')
            file_src_hou = '/com' + fileH[1]

        else:
            file_src_hou = file_hou
        file_path_sdk = file_src_qian + file_src_hou


        return file_path_sdk
