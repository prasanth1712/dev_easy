import os
import subprocess as sp


def get_files(search_key,git_path=None):

    old_dir = os.getcwd()
    if not git_path:
        git_path = "C:\\SD-Oracle-Practice\\ebiz_q2c"
    os.chdir(git_path)
    if search_key:
        ot = sp.run(["git","log",'--all','--grep',search_key,'--pretty=format:','--name-only'],capture_output=True)
        lst = str(ot.stdout.decode('UTF-8')).splitlines()
        lst = list(set(lst))
        if '' in lst:
            lst.remove('')
    os.chdir(old_dir)
    return lst


#print(get_files('CQ2C-708',"C:\\SD-Oracle-Practice\\ebiz_q2c"))