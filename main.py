import hashlib
from time import time


ALPHABIT = 'qwertyuiopasdfghjklzxcvbnm1234567890 -_=+~@!#$%^&*()'

def decorator_password_generator(symbols=ALPHABIT, min_lenght=1):
    def decorator(extra_main):

        def RGF(M, current_password):
            if M == 0:
                _flag = extra_main(current_password)
                return _flag, current_password
            else:
                for letter in list(symbols):
                    current_password += letter
                    status, password = RGF(M-1, current_password)
                    if status:
                        return True, password
                    else:
                        current_password = current_password[:-1]
                return False, current_password


        def main():
            n = min_lenght
            current_password = ''
            print('---------------------------------------------------------------')
            print('Symbols - ', symbols)
            print('Min_lenght - ', min_lenght)
            print('---------------------------------------------------------------')
            text = input('Do you wont to run(Y, n)? >> ').lower()
            if text == 'y' or text == '':
                t0 = time()
                while True:
                    print(f'[INFO] Checking password type: {"X" * n}')
                    status, password = RGF(n, current_password)
                    if status:
                        full_time_s = (time() - t0) % 60
                        full_time_m = int(((time() - t0) // 60) % 60)
                        full_time_h = int(((time() - t0) // 60) // 60 % 60)
                        print(f'[SUCCES] Generetor finished in time - {full_time_h}:{full_time_m}:{full_time_s}')
                        print('---------------------------------------------------------------')
                        return password
                    n += 1
            else:
                print('[INFO] Generotor not runned')
        
        return main

    return decorator


class NotRunGeneratorError(Exception):
    def __str__(self) -> str:
        return 'For get password, you need run generator'


class GeneratorPassword:
    def __init__(self, true_password: str, symbols=ALPHABIT, min_lenght=1):
        self.symbols = symbols
        self.min_lenght = min_lenght
        self.true_password = true_password
        self.generated_password = ''
        
    def checkeng_password(self, checking_password: str) -> bool:
        pass
    
    def get_password(self):
        if self.generated_password:
            return self.generated_password 
        else:
            raise NotRunGeneratorError

    def run(self):
        @decorator_password_generator(symbols=self.symbols, min_lenght=self.min_lenght)
        def extra_main(checking_password:str):
            return self.checkeng_password(checking_password)
        
        self.generated_password = extra_main()



if __name__ == '__main__':
    # Writing password to file
    # with open('true_password.txt', 'w') as file:
    #     file.write(hashlib.sha256(b'4944').hexdigest())

    # Reading password from file
    with open('true_password.txt', 'r') as file:
        password = file.read()

    # First method generating password(with decarator)
    @decorator_password_generator()
    def get_password(checking_password:str):
        # Method hashing - SHA256
        if password == hashlib.sha256(checking_password.encode()).hexdigest():
            return True
        else:
            return False
    print('[INFO] Generating password with decorator')
    print(f'Password - {get_password()}\n')

    # Second method generating password(with class)
    class CustomGeneratorPassword(GeneratorPassword):
        def checkeng_password(self, checking_password: str) -> bool:
            # Method hashing - SHA256
            return self.true_password == hashlib.sha256(checking_password.encode()).hexdigest()
    
    print('[INFO] Generating password with class')
    generator = CustomGeneratorPassword(password)
    generator.run()
    print(f'Password - {generator.get_password()}')


