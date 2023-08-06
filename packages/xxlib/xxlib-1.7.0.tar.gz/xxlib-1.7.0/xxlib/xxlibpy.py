def py(name):
 f = open(name+".py")
 contents = f.read()
 f.close()
 exec(contents)


def py2(d):
    exec(d)

def pyhelp():
    a="""
      from xxlib.xxlibpy import*
      n=input("文件名（.py):")
      py(n)
      
      在同一文件夹内的文件名，不用输入后缀，默认后缀为.py，支持多行语句
      
      
      
      from xxlib.xxlibpy import*
      n=input("要执行的语句:")
      py2(n)
      
      仅支持单行语句
      """