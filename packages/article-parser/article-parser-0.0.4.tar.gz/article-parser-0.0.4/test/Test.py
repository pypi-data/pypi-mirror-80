import article_parser

title, content = article_parser.parse(url="http://www.chinadaily.com.cn/a/202009/22/WS5f6962b2a31024ad0ba7afcb.html")
print(title)
print('---------------')
print(content)