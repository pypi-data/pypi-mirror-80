from request import request


class DSC:
    def __init__(self, token):
        self.token = token

    def getLink(self, id):
        if id is None: return print("id is required parameter.")
        return request("/link/{}".format(id), "GET")

    def getLinks(self, userID):
        if id is None: return print("userID is required parameter.")
        return request("/links/{}".format(userID), "GET")

    def getUser(self, userID):
        if id is None: return print("userID is required parameter.")
        return request("/info/{}".format(userID), "GET")

    def getAnnouncements(self, userID):
        if id is None: return print("userID is required parameter.")
        return request("/announcements/{}".format(userID), "GET")

    def createLink(self, link, redirect, type):
        if link is None: return print("link is required parameter.")
        if redirect is None: return print("redirect is required parameter.")
        if type is None: return print("type is required parameter.")
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "link": link,
            "redirect": redirect,
            "type": type,
            "token": self.token
        }
        response = request("/create", "POST", headers, body)
        if response == 200:
            return {
                "status": 200,
                "message": "Successfully created the link.",
                "short:": "https://dsc.gg/{}".format(link),
                "type": type
            }
        if response == 401:
            return {
                "status": 401,
                "message": "You provided an invalid Discord oauth token."
            }
        if response == 403:
            return {
                "status": 403,
                "message": "You are blacklisted from dscpy and therefore can't create links."
            }
        if response == 500:
            return {
                "status": 500,
                "message": "Something missing."
            }

    def updateLink(self, link, redirect, type):
        if link is None: return print("link is required parameter.")
        if redirect is None: return print("redirect is required parameter.")
        if type is None: return print("type is required parameter.")
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "link": link,
            "redirect": redirect,
            "type": type,
            "token": self.token
        }

        response = request("/update", "POST", headers, body)
        if response == 200:
            return {
                "status": 200,
                "message": "The link was successfully updated."
            }
        if response == 401:
            return {
                "status": 401,
                "message": "You provided an invalid Discord oauth token."
            }
        if response == 500:
            return {
                "status": 500,
                "message": "Short link does not exist."
            }

    def deleteLink(self, link):
        if link is None: return print("link is required parameter.")
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "link": link,
            "token": self.token
        }
        response = request("/delete", "POST", headers, body)
        if response == 200:
            return {
                "status": 200,
                "message": "The link was successfully deleted."
            }
        if response == 401:
            return {
                "status": 401,
                "message": "You provided an invalid Discord oauth token."
            }
        if response == 403:
            return {
                "status": 403,
                "message": "You are blacklisted from dscpy and therefore can't create links."
            }
        if response == 500:
            return {
                "status": 500,
                "message": "Short link does not exist."
            }

    def transferLink(self, link, userID, message):
        if link is None: return print("link is required parameter.")
        if userID is None: return print("userID is required parameter.")
        if message is None: return print("message is required parameter.")
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "link": link,
            "transfer": userID,
            "comments": message,
            "token": self.token
        }
        response = request("/transfer", "POST", headers, body)
        if response == 200:
            return {
                "status": 200,
                "message": "Your request was submitted successfully."
            }
        if response == 401:
            return {
                "status": 401,
                "message": "You provided an invalid Discord oauth token."
            }
        if response == 403:
            return {
                "status": 403,
                "message": "The link you tried to transfer was not created or owned by you."
            }
        if response == 500:
            return {
                "status": 500,
                "message": "Something missing."
            }
