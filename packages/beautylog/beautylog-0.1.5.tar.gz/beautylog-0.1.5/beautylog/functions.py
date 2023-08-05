import time
from functools import wraps
import os
import sys
import traceback
import _ctypes

IS_CUS_ENABLE = True
STDOUT = sys.stdout
#python setup.py sdist bdist_wheel 
#python -m twine upload dist/*


def set_cus_enable():
    global IS_CUS_ENABLE
    IS_CUS_ENABLE = True

def set_cus_disable():
    global IS_CUS_ENABLE
    IS_CUS_ENABLE = False


def writeFile(file_path, mode, content):
    with open(file_path, mode) as f:
        f.write(content + '\n')


def readFile(file_path):
    with open(file_path) as f:
        print(f.read())


def writeLog(msg, file_dir = os.path.dirname(__file__)):
    msg = str(msg)
    run_time = time.strftime( "%Y-%m-%d %H:%M:%S ", time.localtime())
    writeFile(os.path.join(file_dir, 'debug.log'), 'a', '%s %s' % (run_time, msg))
    print('%s %s' % (run_time, msg))


def failExsit(err, file_dir = os.path.dirname(__file__)):
    writeLog('[[ERROR]] : %s ' % err, file_dir)

# 让输出变为标准输出
def beStdOut():
    sys.stdout = STDOUT

# 让输出变为定制输出
def beCusOut(custom_out, is_enable=True):
    if IS_CUS_ENABLE and is_enable:
        sys.stdout = custom_out

class __BeautyLogOut__:
    def __init__(self, func_name, file_dir = os.path.dirname(__file__)):
        self._buff = ''
        self.func_name = func_name
        self.file_dir = file_dir

    def write(self, out_stream):
        if out_stream not in ['', '\r', '\n', '\r\n']: # 换行符不单独输出一行log
            self_out = sys.stdout
            beStdOut() # 设为标准输出
            writeLog("[%s] %s" % (self.func_name, out_stream), self.file_dir)
            beCusOut(self_out) # 设为定制输出

    def flush(self):
        self._buff = ""


def logDecoration(func):

    @wraps(func) 
    def log(*args, **kwargs):
        try:
            file_dir = os.path.dirname(func.__code__.co_filename)
            caller_name = sys._getframe(1).f_code.co_name
            # 判断是否为类内调用
            try:
                func_args = str(args[0]).strip('<>').split(' ')
                class_id = int(func_args[-1], 16) # 获取对象地址
                func_class = func_args[0].split('.')[-1]
                # print(int(str(func.__code__).replace(',', '').strip('<>').split(' ')[4], 16)) # 查看函数地址
            except:
                func_args = str(args)
            if '.' in func.__qualname__ and '<local>' not in func.__qualname__: # 若为类内调用
                func_name = '<%s %s><%s>' % (func_class, class_id, func.__name__)
                caller_name = '<%s %s><%s>' % (func_class, class_id, caller_name)
            else:
                func_name = func.__name__

            beStdOut() # 设为标准输出
            if '<module>' not in caller_name: # 若函数中调用了子函数，应打印调用者信息
                writeLog("[%s] is calling [%s]" % (caller_name, func_name), file_dir)
            writeLog("[%s] is called" % func_name, file_dir)

            beCusOut(__BeautyLogOut__(func_name, file_dir)) # 设为定制输出
            func_return = func(*args, **kwargs)

            beStdOut() # 设为标准输出
            writeLog("[%s] return [%s]" % (func_name, func_return), file_dir)
            if '<module>' not in caller_name: # 若函数中调用了子函数，子函数退出时，定制输出应为主函数的定制输出
                beCusOut( __BeautyLogOut__(caller_name, file_dir)) # 设为定制输出
            return func_return

        except Exception as err:
            beStdOut() # 设为标准输出
            failExsit("<%s> %s" % (func_name, err), file_dir)
            sys.exit(0)
    return log


class LogDecorationClass:
    def __init__(self, is_cus_enable=True):
        self.is_cus_enable = is_cus_enable

    def __call__(self, func):
        @wraps(func) 
        def log(*args, **kwargs):
            try:
                file_dir = os.path.dirname(func.__code__.co_filename)
                caller_name = sys._getframe(1).f_code.co_name
                # 判断是否为类内调用
                try:
                    func_args = str(args[0]).strip('<>').split(' ')
                    class_id = int(func_args[-1], 16) # 获取对象地址
                    func_class = func_args[0].split('.')[-1]
                    # print(int(str(func.__code__).replace(',', '').strip('<>').split(' ')[4], 16)) # 查看函数地址
                except:
                    func_args = str(args)
                if '.' in func.__qualname__ and '<local>' not in func.__qualname__: # 若为类内调用
                    func_name = '<%s %s><%s>' % (func_class, class_id, func.__name__)
                    caller_name = '<%s %s><%s>' % (func_class, class_id, caller_name)
                else:
                    func_name = func.__name__

                beStdOut() # 设为标准输出
                if '<module>' not in caller_name: # 若函数中调用了子函数，应打印调用者信息
                    writeLog("[%s] is calling [%s]" % (caller_name, func_name), file_dir)
                writeLog("[%s] is called" % func_name, file_dir)

                beCusOut(__BeautyLogOut__(func_name, file_dir), self.is_cus_enable) # 设为定制输出
                func_return = func(*args, **kwargs)

                beStdOut() # 设为标准输出
                writeLog("[%s] return [%s]" % (func_name, func_return), file_dir)
                if '<module>' not in caller_name: # 若函数中调用了子函数，子函数退出时，定制输出应为主函数的定制输出
                    beCusOut( __BeautyLogOut__(caller_name, file_dir)) # 设为定制输出
                return func_return

            except Exception as err:
                beStdOut() # 设为标准输出
                failExsit("<%s> %s" % (func_name, err), file_dir)
                sys.exit(0)
        return log

if __name__ == "__main__":

    @LogDecorationClass()
    def my():
        print('a')
        print('b')
        try:
            print('try')
            raise Exception("ERERERER")
        except Exception as err:
            print('except')

    @LogDecorationClass()
    def main(args):
        print('main1')
        my()
        print("main2")
        try:
            print('try')
            raise Exception("ERERERER")
        except Exception as err:
            print('except')

    class Test:
        @LogDecorationClass(False)
        def main(self):
            print('I\'m in the test_main')
        @LogDecorationClass()
        def main2(self):
            print('m1')
            self.main()
            print('m2')

    @LogDecorationClass()
    def person(name):
        def child():
            return 'Hello child of ' + name
        return child
    test = Test()
    test.main2() # 调用类中方法
    print('this is the split line-------------------------------------')
    set_cus_disable()
    my() # 调用函数
    print('this is the split line-------------------------------------')
    main(test) # 调用类内方法同名函数
    print('this is the split line-------------------------------------')
    result=person("Me!") # 需要优化的情况，返回值为函数名
    result()

    