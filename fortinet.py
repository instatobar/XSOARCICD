import requests

class Fortinet:
    
    def __init__(self, ip: str = "", token: str = "", protocol: str = "https", port: int = 443, verify: bool = False):
        self.__token = token
        self.__url_base = protocol + f"://{ip}" + [":"+str(port) if port != 443 else ""][0]
        self.__session = requests.Session()
        self.__verify
        
    def get_loca_user_name(self, username = "", **kwargs):
        if username: 
            url = self.__url_base + f"/user/local/{username}"
            if kwargs:
                kwargs.update({'access_token': self.__access_token})
            else:
                kwargs = {'access_token': self.__access_token}
            
            user_data = self.__session.get(url, )

        else:
            raise Exception("Se debe indicar el nombre de usuario.")
        
#f = Fortinet("1.1.1.1", "asdasdasd", protocol="https", port=80)

