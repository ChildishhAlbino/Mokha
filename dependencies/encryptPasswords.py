import subprocess
import pyperclip
import os
import os.path as path
template = "sh %s input=%s verbose=false password=%s algorithm=PBEWITHHMACSHA512ANDAES_256 keyObtentionIterations=1000 saltGeneratorClassName=org.jasypt.salt.RandomSaltGenerator providerName=SunJCE stringOutputType=base64 ivGeneratorClassName=org.jasypt.iv.RandomIvGenerator"


def encrypt(clipboardContext=None, scriptRelPath="./jasypt/bin/encrypt.sh"):
    print(os.getcwd())
    password = os.environ["TINA_ADMIN_ENCRYPT_PASSWORD"]
    try:
        to_be_encrypted = clipboardContext if(
            clipboardContext != None) else pyperclip.paste()
        filled = template % (scriptRelPath,
                             to_be_encrypted, password)
        print("Attemping to encrypt the value `%s` with Jasypt CLI." %
              (to_be_encrypted))
        split = filled.split()
        result = subprocess.run(split, stdout=subprocess.PIPE)
        resultAsString = result.stdout.decode('utf-8')
        print(resultAsString)
        if(resultAsString != None):
            pyperclip.copy(resultAsString)
    except:
        print("Error encrypting string.")


if __name__ == "__main__":
    encrypt()
