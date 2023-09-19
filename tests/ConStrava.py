import requests
import webbrowser


def main():
    CLIENT_SECRET= 'a894f828ebc4cb29861f4c9c04292e7645cddbb9'
    CLIENT_ID = 47324    
    redirect_uri = "localhost" 
    SCOPE = ["read", "read_all", "profile:read_all", "profile:write", "activity:read", "activity:read_all", "activity:write", "", "", ""]

    # PASO 1. PEDIR CODE (a strava) y AUTORIZACION (al usuario)
    code = AskForAuthorization(CLIENT_ID, SCOPE[5], redirect_uri)

    # PASO 2. Cambiar CODE por TOKEN
    data = GetFirstAccessToken(CLIENT_ID, CLIENT_SECRET, code)
    access_token = data[0]

    if access_token == None:
        with open("token.txt", "r") as f:
            access_token = str(f.readline())





    # PASO 3. Make Athlete Query
#    resp = GetAthlete(access_token)

    url = "https://www.strava.com/api/v3/athlete/activities"
    para = {
        "per_page" : 2,
         "access_token": access_token
    }
    headeeers = {
        "authorization": "Bearer " + access_token
    }

    resp = requests.get(url = url, params=para)
    lala = resp.json()

    # MOSTRAR en yeison
    print (lala)



    with open("lalala.json", "w") as f:
        f.write(str(lala))

    with open("token.txt", "w") as f:
        f.write(str(access_token))
    


def GetAthlete(access_token):
    """ Retrieves information about de logged in Athelete """

    url_athlete = "https://www.strava.com/api/v3/athlete"
    params_query_athlete = {
        "access_token" : access_token
    }
    resp = requests.get(url_athlete, params_query_athlete)
    resp_dict = resp.json()

    return resp_dict



def AskForAuthorization(client_id, scope, redirect_uri, approval_prompt = "auto"):
    """ Opens the web browser to ask the user for authorization. """

    # SCOPE = ["read", "read_all", "profile:read_all", "profile:write", "activity:read", "activity:read_all", "activity:write", "", "", ""]
    url_auth = "https://www.strava.com/api/v3/oauth/authorize"
    params_auth = {
        "client_id":client_id,
        "scope": scope,
        "redirect_uri" : redirect_uri,
        "response_type":"code",
        "approval_prompt" : approval_prompt
    }
    ur = BuildAuthURL(url_auth, params_auth)
    webbrowser.open_new_tab(ur)

    # Here comes the code returned as part of the URL
    code = input("CLAVE: ")

    return code




def GetFirstAccessToken(client_id, client_secret, code):
    """ Changes the code obtained for the access_token needed... aunque es una pija """ 

    params = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "code": code,
        "grant_type" : "authorization_code"
    }
    url = "https://www.strava.com/oauth/token"

    resp = requests.post(url, data = params)
    resp_dict = resp.json() # json.loads(resp.content)

    access_token = resp_dict["access_token"]
    refresh_token = resp_dict["refresh_token"]
    expires_in = resp_dict["expires_in"]
    expires_at = resp_dict["expires_at"]
    token_type = resp_dict["token_type"]

    return (access_token, expires_at, expires_in, refresh_token, token_type)




def RefreshAccessToken(client_id, client_secret, refresh_token):
    """ Retrieves the new access_token and its data when it has been renewed """

    params = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "refresh_token ": refresh_token,
        "grant_type" : "refresh_token"
    }
    url = "https://www.strava.com/oauth/token"

    resp = requests.post(url, data = params)
    resp_dict = resp.json() # json.loads(resp.content)

    access_token = resp_dict["access_token"]
    refresh_token = resp_dict["refresh_token"]
    expires_in = resp_dict["expires_in"]
    expires_at = resp_dict["expires_at"]

    return (access_token, expires_at, expires_in, refresh_token)




def BuildAuthURL(url, params):
    text = url+"?"

    for v in params:
        if v == 'redirect_uri':
            text += v + "=https%3A%2F%2F" + str(params[v]) + "&"
        else:
            text += v + "=" + str(params[v]) + "&"

    return text[:-1]


if __name__ == "__main__":
    main()