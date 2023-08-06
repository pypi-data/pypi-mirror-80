import ctypes, sys, os

ALLFILES = os.listdir()
FILE = ''

archive_extensions = ('.7z', '.ace', '.alz', '.a', '.arc', '.arj', '.bz2', '.cab', '.Z', '.cpio', '.deb', '.dms', '.gz', '.lrz', '.lha', '.lzh', 
'.lz', '.lzma', '.lzo', '.rpm', '.rar', '.rz', '.tar', '.xz', '.zip', '.jar', '.zoo')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    archives = []
    print('Searching for archives in the current directory...')
    for file in ALLFILES:
        if file.endswith(archive_extensions):
            archives.append(file)
    clear()
    print('Found the following files:')
    n=1
    for archive in archives:
        print('{}. {}'.format(str(n), archive))
        n += 1
    choice = int(input('Which one is the font archive? '))
    FILE = archives[choice - 1]

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)