import os,sys
NP =os.popen('python -m pip --version').readlines()[0].split("from ")[1].split(r"\pip")[0]
# NP =os.path.dirname(os.path.dirname(NP)) +"\\Scripts"
NP = NP+"\\git\\cmd"
os.chdir(NP)

print(os.getcwd())
print(len(sys.argv))


# if len(sys.argv)==2:
#     os.system("git.exe "+sys.argv[1])

# if len(sys.argv)==1:
#     os.system("git.exe")