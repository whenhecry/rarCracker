import logging
from unrar import rarfile
import os


def testInput(rfName, pfName):
    # test rfName is rar and pfName is file
    if rarfile.is_rarfile(rfName) and os.path.isfile(pfName):
        return True
    else:
        print '[-] file invalid'


def pipeline(rfName, pfName, fns):
    if not fns:
        print '[+] pipeline completed'
        return
    elif not fns[0](rfName, pfName):
        print '[-] pipeline broke'
        return
    else:
        print '[+] pipeline: %s pass' % fns[0].func_name
        return pipeline(rfName, pfName, fns[1:])


def crack(rfName, pfName):
    rf = rarfile.RarFile(rfName)
    cnt = 0
    with open(pfName, 'rb') as pf:
        for line in pf:
            cnt += 1
            password = line.strip('\r\n')
            print '[*] testing: %s' % password
            try:
                rf.extractall(pwd=password)
                print '[+] password is %s' % password
                return True
            except RuntimeError as e:
                errMessage = e.args[0]
                if 'Bad' in errMessage:
                    print '[-] bad'
                else:
                    print '[-] unknown error'
            except rarfile.BadRarFile as e:
                errMessage = e.args[0]
                if 'Bad RAR archive data' in errMessage:
                    print '[-] bad'
                else:
                    print '[-] unknown error'
            finally:
                print '[*] %d attempts' % cnt


def main():
    rfName = 'test.rar'
    pfName = 'Dic.py'
    pipeline(rfName, pfName,
             [testInput, crack])


if __name__ == '__main__':
    main()
