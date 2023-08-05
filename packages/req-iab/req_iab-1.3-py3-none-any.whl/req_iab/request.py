# coding=UTF-8
def getOrPost(postString,getOrPost,url):
    import json
    try:
        import requests
    except ModuleNotFoundError:
        return "<ERROR 3>无法在未安装requests库的情况下爬虫，请在cmd/Terminal中输入pip[版本] install requests安装，如pip3.8 install requests"
    if getOrPost=='get':
        try:
            getReturn=requests.get(url)
        except requests.exceptions.MissingSchema:
            return "<ERROR 1> 必须添加网址前缀https://"
        return getReturn.text.encode(getReturn.encoding).decode(getReturn.apparent_encoding)
    else:
        try:
            postDictionary=json.loads(postString)
        except json.decoder.JSONDecodeError:
            return "<ERROR 2>在转换成json时出现错误，函数自动退出"
        try:
            postReturn=requests.post(url=url,data=postDictionary)
        except requests.exceptions.MissingSchema:
            return "<ERROR 1> 必须添加网址前缀https://"
        return postReturn.text.encode(postReturn.encoding).decode(postReturn.apparent_encoding)

