from urllib.request import Request, urlopen
import json

ecoURL = "https://api.spookvooper.com/eco"
userURL = "https://api.spookvooper.com/user"
groupURL = "https://api.spookvooper.com/group"
authURL = "https://api.spookvooper.com/auth"

class Utils(object):
    @staticmethod
    def get_html(link,p=False):
        try:
            if p:
                print(link)
            fp = Request(link,headers={'User-Agent':'Mozilla/5.0'})
            fp = urlopen(fp).read()
            mybytes = fp
            mystr = mybytes.decode("utf8")
            return mystr
        except Exception as e:
            print(e)
            return "Error"

class User(object):
    @staticmethod
    def getUsername(svid):
        data = Utils.get_html(f"{userURL}/getUsername?svid={svid}")
        return data

    @staticmethod
    def getSvidFromDiscord(discordid):
        data = Utils.get_html(f"{userURL}/getSvidFromDiscord?discordid={discordid}")
        return data

class Eco(object):
    @staticmethod
    def getBalance(svid):
        data = Utils.get_html(f"{ecoURL}/getBalance?svid={svid}")
        return data
    
    @staticmethod
    def sendTransactionByIds(fromUser, to, amount, auth, detail):
        data = Utils.get_html(f"{ecoURL}/sendTransactionByIds?from={fromUser}&to={to}&amount={amount}&auth={auth}&detail={detail}")
        return data