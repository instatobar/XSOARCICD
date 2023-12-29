import requests
import urllib3
from json import dumps

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FortiTokenAPI:
    def __init__(self, ip: str, vdom: str, authentication_token: str):
        """
        Inicializa una instancia de la clase FortiTokenAPI.

        Args:
            ip (str): Dirección IP del servidor.
            vdom (str): VDOM del servidor.
            authentication_token (str): Token de autenticación.
        """
        self.__session = requests.Session()
        self.__session.headers.update({'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.__base_url = f"https://{ip}"
        self.__auth_token = authentication_token
        self.__vdoms = vdom
        self.__verify = False  # Deshabilitar la verificación del certificado SSL, si es necesario

    def __clear_keys(self, kwargs):
        newDict: dict = {}
        
        for k, v in kwargs.items():
            if "_" in k:
                newDict[k.replace("_", "-")] = v
            else:
                newDict[k] = v
                
        return newDict


    def retrieve_token_all(self):
        """
        Obtener todos los tokens.

        Returns:
            list: Lista de tokens.
        """
        url_endpoint = "/api/v2/cmdb/user/fortitoken"
        url = self.__base_url + url_endpoint
        params = {'vdom': self.__vdoms, 'access_token': self.__auth_token}
        response = self.__session.get(url, params=params, verify=self.__verify)
        response.raise_for_status()
        data = response.json()
        data_fill_tokens = data.get("results", [])       
        return data_fill_tokens
    
    def retrieve_user_all(self):
        """
        Obtener todos los usuarios.

        Returns:
            list: Lista de usuarios.
        """
        url_endpoint = "/api/v2/cmdb/user/local"
        url = self.__base_url + url_endpoint
        params = {'vdom': self.__vdoms, 'access_token': self.__auth_token}
        response = self.__session.get(url, params=params, verify=self.__verify)
        response.raise_for_status()
        data = response.json()
        data_fill_users = data.get("results", [])       
        return data_fill_users
    
    def update_user(self, name, **kwargs):
        """
        Actualiza el usuario con el nombre especificado y cambia el estado.

        Args:
            name (str): Nombre del usuario a actualizar.
            status (str): Nuevo valor para el campo "status" enable/disable.

        Returns:
            dict or str: Si se encuentra el usuario, se devuelve el usuario actualizado en forma de diccionario. 
                         Si no se encuentra el usuario, se devuelve el mensaje "Usuario no encontrado".
        """

        url_endpoint = f"/api/v2/cmdb/user/local/{name}"
        url = self.__base_url + url_endpoint
        params = {'vdom': self.__vdoms, 'access_token': self.__auth_token}
        
        if (user_data := self.__session.get(url, params=params, verify=self.__verify)):
            update_user = user_data.json()["results"][0]

            update_user.update(self.__clear_keys(kwargs))
            
            response = self.__session.put(url, params=params, json=update_user, verify=self.__verify)

            return response.json()
            


def main():
    # Crear una instancia de FortiTokenAPI
    ft = FortiTokenAPI(ip="172.16.93.101", vdom="cdlv-intra", authentication_token="nw14yqQQ4wH7p7tmqh6g67Gw61n7t4")
        
    # Obtener todos los tokens
    # tokens = ft.retrieve_token_all()
    # print(json.dumps(tokens, indent=1))

    # Obtener todos los usuarios
    # users = ft.retrieve_user_all()
    # print(json.dumps(users, indent=1))
    
    # Actualizar el usuario con el nombre especificado
    oUser = ft.update_user("soc_corporaciones_dev", status="enable", two_factor="fortitoken", two_factor_authentication="fortitoken", fortitoken="FTKMOB1CF413383F", email_to="ints_atobar@externos.entel.cl")
    print(oUser)
    #print(json.dumps(oUser, indent=1))       
        
if __name__ == "__main__":
    main()
