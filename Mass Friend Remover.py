import riotgames_api

lolcapi = riotgames_api.LeagueOfLegendsClientAPI()

r = lolcapi.get("/lol-chat/v1/friends/")

def menu():
    print("-"*70)
    print('[!] (1) Excluir todos os amigos. (2) Listar o nick de todos os amigos.')
    print("-"*70)

    selection = int(input("[=] Seleção : "))

    if selection == 1:
        for i in r:
            print("[-] Deletado (%s) da lista de amigos." % i["gameName"])
            lolcapi.delete("/lol-chat/v1/friends/%s" % i["puuid"])
                
    if selection == 2:
        for i in r:
            print(i["gameName"])
            
    input('[!] Press Enter to Continue')
    menu()
            
menu()