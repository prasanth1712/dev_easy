from jira import JIRA,Issue,Project

server = 'http://itjiraapi.bmc.com/' #'https://itjira.bmc.com/'
user_name = 'pr'
pwd = 'Sri@1993'#'ppph@517915'


def get_objects(project,fixver=None,obj_id=None,fields=None):
    objs=[]
    obj={}
    try:
        if obj_id:
            jql_str ='issue = "{}" and issuetype in ("Story","Bug") '.format(obj_id)
        else:
            jql_str ='project = "{}" and issuetype in ("Story","Bug") '.format(project)
        jira = JIRA(server=server,basic_auth=(user_name,pwd))
        if not fields:
            fields='summary,reporter,issuetype,project,fixVersions,customfield_10401,customfield_10402'
        else:
            if fields.find('fixVersions') <0:
                fields+=',fixVersions'
        object_list = jira.search_issues(jql_str=jql_str,fields=fields,maxResults=200)
        for i in range(0,len(object_list)):
            fix_ver = object_list[i].fields.fixVersions
            if (fix_ver and str(fix_ver[0]).strip()==str(fixver).strip()) or (obj_id):
                obj['object_id']=object_list[i].key
                obj['object_desc']=object_list[i].fields.summary
                obj['object_rel']=str(fix_ver[0]).strip()
                if object_list[i].fields.project:
                    obj['object_track']=object_list[i].fields.project.name
                if object_list[i].fields.customfield_10401:
                    lst = object_list[i].fields.customfield_10401
                    tmp = ''
                    for k in lst:
                        tmp+=k.displayName+' | '
                    obj['object_dev'] = tmp
                else:
                    obj['object_dev']=None
                    
                if object_list[i].fields.customfield_10402:
                    lst = object_list[i].fields.customfield_10402
                    tmp = ''
                    for k in lst:
                        tmp+=k.displayName+' | '
                    obj['object_qa'] = tmp
                else:
                    obj['object_qa']=None
                if object_list[i].fields.issuetype:
                    obj['object_type']=object_list[i].fields.issuetype.name
                objs.append(obj.copy())
                obj.clear()
                
    except Exception as e:
        print(e)
    finally:
        jira.close()
        return objs