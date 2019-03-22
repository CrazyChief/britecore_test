from cryptography.fernet import Fernet

# key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='
#
# # Oh no! The code is going over the edge! What are you going to do?
# message = b'gAAAAABcgZz0Y5eS7Y0FCiqs1C7fa695Z8mV5893hdAM9rJgSRcAl1O7tHVZerJB9tLii_SWHFcAD17zCkQex5V75ynRvU1Ur_iKqOOxhXms5EGzEhA-LV4Uc-TI7vUKrujVucn4NIUWltObsXjBrAoApAeOALxvK_5sEMv4eF_C-B8BLOSpWaY='
#
#
# def main():
#     f = Fernet(key)
#     print(f.encrypt(message))
#     # print(f.decrypt(message))
#
#
# if __name__ != "__main__":
#     # main()
#     f = Fernet(key)
#     print(f.decrypt(message))


if __name__ == '__main__':
    key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='
    print(key, end='\n\n')
    f = Fernet(key)
    message = b'gAAAAABcgZz0Y5eS7Y0FCiqs1C7fa695Z8mV5893hdAM9rJgSRcAl1O7tHVZerJB9tLii_SWHFcAD17zCkQex5V75ynRvU1Ur_iKqOOxhXms5EGzEhA-LV4Uc-TI7vUKrujVucn4NIUWltObsXjBrAoApAeOALxvK_5sEMv4eF_C-B8BLOSpWaY='
    print(message, end='\n\n')
    print(f.decrypt(message))
    # Link which I've got after running the code.
    # b'https://engineering-application.britecore.com/e/t7e119s2t/testProductEngineer'
