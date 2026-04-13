import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import generate_daily_news

def handler(request):
    try:
        result = generate_daily_news()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8"
            },
            "body": f"""
<html>
<head>
<meta charset="utf-8">
<title>每日新闻简报</title>
</head>
<body style="padding: 30px; font-size: 16px; line-height: 1.8;">
<h1>📰 每日新闻简报</h1>
<pre style="white-space: pre-wrap; font-size: 16px;">{result}</pre>
</body>
</html>
"""
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"错误：{str(e)}"
        }
