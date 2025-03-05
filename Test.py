from crawl import UserAgent


def UserAgent_test():
    ua = UserAgent.Random_User_Agents()
    ua_get = ua.get()
    ua_get_by_browser = ua.get_by_browser("edge")
    print(ua_get)
    print(ua_get_by_browser)


if __name__ == "__main__":
    UserAgent_test()
