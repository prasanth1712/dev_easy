import os
import subprocess as sp
from conf import get_conf

if 'nt' in os.name:
    cnf = get_conf('BITBUCKET')
else:
    cnf = get_conf('BITBUCKET_POSIX')

def get_files(search_key):
    old_dir = os.getcwd()

    git_path = cnf['git_dir']
    os.chdir(git_path)
    
    if search_key:
        ot = sp.run(["git","diff-index",'--quiet','master'],stdout=sp.PIPE)
        if int(ot.returncode) != 0:
            bit_username = cnf['username']
            bit_password = cnf['password']
            bit_url = cnf['url']
            tmp = str(bit_url).split('//')
            tmp = str(tmp[0])+'//'+str(bit_username)+':'+str(bit_password).replace('@','%40')+'@'+str(tmp[1])
            ot = sp.run(["git","pull",tmp],stdout=sp.PIPE)
        
        ot = sp.run(["git","log",'--all','--grep',search_key,'--pretty=format:','--name-only'],stdout=sp.PIPE)
        lst = str(ot.stdout.decode('UTF-8')).splitlines()
        lst = list(set(lst))
        if '' in lst:
            lst.remove('')
    os.chdir(old_dir)
    return lst


#print(get_files('CQ2C-708',"C:\\SD-Oracle-Practice\\ebiz_q2c"))