import nacl.secret
import nacl.utils
import colorama
import os
import sys

#config
outfile = 'out'

#end config


#scanner class
class Scanner:
    def __init__(self):
        pass

    def executeInput(self, text):
        args = text.split(" ")

        if(args[0] == "encrypt"):
            encrypt(args)
        elif(args[0] == "decrypt"):
            decrypt(args)
        elif(args[0] == "clr"):
            clr(args)
        elif(args[0] == "read"):
            read(args)
        elif(args[0] == "write"):
            pass
        elif(args[0] == "os"):
            osExec(args)
        else:
            print("Symmetric Crypt Help")
            print("Usage:")
            print("encrypt <filename> <key>")
            print("decrypt <filename> <key>")
            print("read <filename>")
            print("cls <filename (outfile if none specified)>")
            print("os <command>")
            print("help")
            
        
scanner = Scanner()

#crypt class
class SymmetricCrypt:
    def __init__(self, key):
        self.key = key

    def encrypt(self, body, nonce):
        return nacl.secret.SecretBox(self.key).encrypt(body, nonce)

    def decrypt(self, body):
        decrypted = nacl.secret.SecretBox(self.key).decrypt(body)
        return decrypted.decode("utf-8")

#globals
def keyTo32byte(key):
    key = f"{key:<32}"[:32] #fix it to 32 chars
    #        forces it to 32 chars minimum, then cuts off the rest
    return bytes(key, 'utf-8') #turn it into bytes

nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
crypt = SymmetricCrypt("")

#executables

def encrypt(args):
    fileName = args[1]
    key = args[2]

    key = keyTo32byte(key)
    crypt.key = key

    encrypted = crypt.encrypt(open(fileName, 'rb').read(), nonce)
    with open(outfile, 'wb') as f:
        f.write(encrypted)
    print(f"Encrypted to {outfile}")

def decrypt(args):
    fileName = args[1]
    key = args[2]

    key = keyTo32byte(key)
    crypt.key = key

    decrypted = crypt.decrypt(open(fileName, 'rb').read())
    with open(outfile, "w") as f:
        f.write(decrypted)
    print(f"Decrypted {fileName} to {outfile}\n type 'read {outfile}' to read the file")

def clr(args):
    fileName = outfile if len(args) == 1 else args[1]
    with open(fileName, "w") as f:
        f.write("")
    print(f"Cleared {fileName}")

def read(args):
    fileName = args[1]
    with open(fileName, "r") as f:

        length = 50

        halfLength = (length // 2) - (len(fileName) // 2)

        print(f"{'=' * halfLength}{fileName}{'=' * halfLength}")

        print(f.read())
        print(f"{ ((halfLength*2) + len(fileName)) * '='}")

def osExec(args):
    print(os.system(" ".join(args[1:])))

#main 

def main():
    if(len(sys.argv) > 1): #if there is a command line argument, run it
        scanner.executeInput(" ".join(sys.argv[1:]))
    else: #otherwise, run the program in interactive mode
        while(True):
            scanner.executeInput(input( colorama.Fore.BLUE + "crypt> " + colorama.Fore.RESET))

if(__name__ == "__main__"):
    main()