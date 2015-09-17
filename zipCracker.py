import logging
import zipfile
import os


def testInput(zfName, pfName):
    # test rfName is rar and pfName is file
    if zipfile.is_zipfile(zfName) and os.path.isfile(pfName):
        return True
    else:
        print '[-] file invalid'


def pipeline(zfName, pfName, fns):
    if not fns:
        print '[+] pipeline completed'
        return
    elif not fns[0](zfName, pfName):
        print '[-] pipeline broke'
        return
    else:
        print '[+] pipeline: %s pass' % fns[0].func_name
        return pipeline(zfName, pfName, fns[1:])


def crack(zfName, pfName):
    zf = zipfile.ZipFile(zfName)
    cnt = 0
    with open(pfName, 'rb') as pf:
        for line in pf:
            cnt += 1
            password = line.strip('\r\n')
            print '[*] testing: %s' % password
            try:
                zf.extractall(pwd=password)
                print '[+] password is %s' % password
                return True
            except RuntimeError as e:
                errMessage = e.args[0]
                if 'Bad' in errMessage:
                    print '[-] bad'
                else:
                    print '[-] unknown error'
            except zipfile.BadZipfile as e:
                errMessage = e.args[0]
                if 'Bad RAR archive data' in errMessage:
                    print '[-] bad'
                else:
                    print '[-] unknown error'
            finally:
                print '[*] %d attempts' % cnt


def main():
    zfName = '2015.zip'
    pfName = 'Dic.py'
    pipeline(zfName, pfName,
             [testInput, crack])


if __name__ == '__main__':
    main()
