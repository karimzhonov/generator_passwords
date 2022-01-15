import hashlib

ALPHABIT = 'qwertyuiopasdfghjklzxcvbnm1234567890 -_=+~@!#$%^&*()'

def decorator_password_generator(symbols=ALPHABIT, min_lenght=1):
    """
    This functions is decorator: 
    @param: symbols
    @param: min_lenght
    @return: True password
    Take function:
    def extra_main(checking_password) -> bool:
        pass
    """

    def decorator(extra_main):
        from time import time


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


if __name__ == '__main__':

    # with open('true_password.txt', 'w') as file:
    #     file.write(hashlib.sha256(b'4944').hexdigest())

    with open('true_password.txt', 'r') as file:
        password = file.read()

    @decorator_password_generator()
    def get_password(checking_password:str):
        
        if password == hashlib.sha256(checking_password.encode()).hexdigest():
            return True
        else:
            return False

    print(get_password())
