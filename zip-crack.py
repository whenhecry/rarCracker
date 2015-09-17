import zipfile


def main():
    """
    Zipfile password cracker using a brute-force dictionary attack
    """
    zipfilename = '2015.zip'
    dictionary = 'dic.py'

    password = None
    zip_file = zipfile.ZipFile(zipfilename)
    cnt = 0
    with open(dictionary, 'r') as f:
        for line in f.readlines():
            cnt += 1
            password = line.strip('\n')
            print '[*] testing %d' % cnt
            try:
                zip_file.extractall(pwd=password)
                password = 'Password found: %s' % password
                break
            except Exception as e:
                errMessage = e.args[0]
                if 'Bad' or 'Error -3 while decompressing' in errMessage:
                    pass
                else:
                    print '[-] other error: ' + errMessage
                    break
    print password

if __name__ == '__main__':
	main()