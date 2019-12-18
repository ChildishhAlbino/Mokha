import subprocess
import pyperclip
import os
template = "sh ./jasypt/bin/encrypt.sh input=%s verbose=false password=%s algorithm=PBEWITHHMACSHA512ANDAES_256 keyObtentionIterations=1000 saltGeneratorClassName=org.jasypt.salt.RandomSaltGenerator providerName=SunJCE stringOutputType=base64 ivGeneratorClassName=org.jasypt.iv.RandomIvGenerator"
password = os.environ["TINA_ADMIN_ENCRYPT_PASSWORD"]


def encrypt(value=None):
    try:
        to_be_encrypted = value if(value != None) else pyperclip.paste()
        if(to_be_encrypted == ""):
            raise Exception(
                "For some reason I've got a null value to encrypt. Das bad.")
        filled = template % (
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
