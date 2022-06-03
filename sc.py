import nacl.secret
import nacl.utils
import colorama
import os
import sys

#config
outfile = 'out'
useSecondKey = True #if true, the second key is used for encryption. It is recommended to store the second key on the devices you want to use the program with
hiddenKeyPath = "C:\key.txt" #should be a text file with a single line of 32 chars

#scanner class
class Scanner:
    def __init__(self):
        pass

    def executeInput(self, text):
        args = text.split(" ")

        if(args[0] == "enc"):
            encrypt(args)
        elif(args[0] == "dec"):
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
            print("enc <filename> <key>")
            print("dec <filename> <key>")
            print("read <filename>")
            print("cls <filename (outfile if none specified)>")
            print("os <command>")
            print("help")

#crypt class
class SymmetricCrypt:
    def __init__(self, key):
        self.key = key

    def encrypt(self, body):

        if(useSecondKey):
            with open(hiddenKeyPath, "r") as f:
                nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
                hiddenKey = bytes(f.read(), "utf-8")
                body = nacl.secret.SecretBox(hiddenKey).encrypt(body, nonce)

        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return nacl.secret.SecretBox(self.key).encrypt(body, nonce)

    def decrypt(self, body):
        decrypted = nacl.secret.SecretBox(self.key).decrypt(body)

        if(useSecondKey):
            with open(hiddenKeyPath, "r") as f:
                hiddenKey = bytes(f.read(), "utf-8")
                decrypted = nacl.secret.SecretBox(hiddenKey).decrypt(decrypted)

        return decrypted.decode("utf-8")

#globals
def keyTo32byte(key):
    key = f"{key:<32}"[:32] #fix it to 32 chars
    #        forces it to 32 chars minimum, then cuts off the rest
    return bytes(key, 'utf-8') #turn it into bytes

scanner = Scanner()
crypt = SymmetricCrypt("")


#executables
def encrypt(args):
    fileName = args[1]
    key = args[2]

    key = keyTo32byte(key)
    crypt.key = key

    encrypted = crypt.encrypt(open(fileName, 'rb').read())
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