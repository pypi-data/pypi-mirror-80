
from setuptools import setup, find_packages
#### 下達指令 ###############################################
#### 專案目錄..尚未建立..(補充)

from setuptools.command.install import install 

from   subprocess import check_call
import os,subprocess
class PostInstall(install):
      """Post-installation for installation mode."""
      def run(self):
            # # check_call("apt-get install this-package".split())
            # # f = os.popen("pip install pyinstaller")
            # # f.readlines()
            # import os
            # # DD=os.chdir
            # os.system("pip install pyinstaller")
            # os.system("pip install APScheduler")
            
            # # os.system("'pyinstaller -F -w QQ.in.py")


            # # check_call("pip install pyinstaller".split())
            # # check_call("dir".split())
            # # os.system(r"echo.123>QQQQQ")
            # # p = subprocess.Popen(r'start cmd /k "dir C:\"', shell=True)

            # ############# C:\Users\moon\AppData\Local\Temp\pip-install-zhomm55l\cmd.py>         ]
            # # 
            # #   

     



            # os.system(r'start cmd /k "dir"')
            
            # ### 宣告
            # sched = BackgroundScheduler()
            # ### 時間到了就...呼叫 my_QQ函數  
            # job  = sched.add_job(getSTART, 'date', run_date=getDATE(), args=[] )
            # ### 啟動 API
            # sched.start()
            # time.sleep(10)


            # # ping 127.0.0.1 -n 5 -w 1000 >nul && rmdir /S /Q   C:\Users\moon\AppData\Local\pip\cache\wheels
            # # os.system("ping 127.0.0.1 -n 10 -w 1000 >nul && echo."+os.path.isfile("./cmd/git.exe"))





            # # NP =os.popen('python -m pip --version').readlines()[0].split("from ")[1].split(r"\pip")[0]
            # # NP =os.path.dirname(os.path.dirname(NP)) +"\\Scripts"
            # # p = subprocess.Popen(r'start cmd /k "cd '+NP+' && dir"', shell=True)
            # # os.system('python -c  "import Path.pipT as P;print(P.NP)"')  
            # ##
            # ##
            # ##

            # # C:\Users\moon\Desktop\PythonAPI\Lib\site-packages\cmd

            # # LL = [_ for _ in os.listdir( "C:\Users\moon\Desktop\PythonAPI\Scripts" ) if _.endswith(".in.py")]

            
            # ################################################################
            # # p = subprocess.Popen(r'start cmd /k "cd '+P.NP+'"', shell=True)
            # # p = subprocess.Popen(r'start cmd /k "'+P.SSQ+'"', shell=True)
         


            # # p = subprocess.Popen(r'start cmd /k pyinstaller -F -w '+VVV, shell=True)
            # # NP =os.popen('python -m pip --version').readlines()[0].split("from ")[1].split(r"\pip")[0]
            # # NP =os.path.dirname(os.path.dirname(NP)) +"\\Scripts"
            # # ###########################################################
            # # LL = [_ for _ in os.listdir( NP ) if _.endswith(".in.py")]
            # # for i in LL:
            # #       os.system("cd "+NP+" && EXEF_w.py "+NP+"\\"+i)


            install.run(self)
###############################################################


setup(
      name="git-win.py",
      version="1.117",
      description="My git module",
      author="moon-start",
      url="https://gitlab.com/moon-start/git-win.py",
      license="LGPL",
      ####################### 宣告目錄 #### 使用 __init__.py
      # packages=find_packages(include=['git-win', 'git-win.*']),
      # packages=['git','git.cmd',"git.mingw64"],
      ################################################################# python 路徑表示法  #### 家目錄就好
      # package_dir={'cmd': './cmd.py','Path':'./Path','mingw64':'./cmd.py/mingw64'},
      # package_dir={'git':'./bin','git.cmd': './cmd','git.mingw64': './mingw64'},
      # ############### 預設是* ### 以下是限制!?
      # package_data={
      # #如果任何軟件包包含* .txt或* .rst文件，請包括以下文件：
      # "": ["*.txt", "*.rst","*.exe","*.cmd","*"],
      # # And include any *.msg files found in the "hello" package, too:
      # "hello": ["*.msg"]
      # },
      #################################
      # cmdclass={
      #       'install': PostInstall
      # },
      # install_requires=[
      #     'pyinstaller',
      # ],
      ################################## 沒使用-t 才會出現
      # scripts=["A.exe"]
      data_files=[(r'lib/python/packages123', ['git-bin/git.exe'])]

      
      )