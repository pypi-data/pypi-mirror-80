## 介绍

cloud activity API client library.

```
                       .::::.
                     .::::::::.
                    :::::::::::
                ..:::::::::::'
              '::::::::::::'
                .::::::::::
           '::::::::::::::..
                ..::::::::::::.
              ``::::::::::::::::
               ::::``:::::::::'        .:::.
              ::::'   ':::::'       .::::::::.
            .::::'      ::::     .:::::::'::::.
           .:::'       :::::  .:::::::::' ':::::.
          .::'        :::::.:::::::::'      ':::::.
         .::'         ::::::::::::::'         ``::::.
     ...:::           ::::::::::::'              ``::.
    ```` ':.          ':::::::::'                  ::::..
                       '.:::::'                    ':'````..


```

## 问题
```
# TypeError: 'Response' object is not callable
# The view function did not return a valid response.
# The return type must be a string, tuple, Response instance, or WSGI callable, but it was a Response.

result = activity_client.generate_serials(quantity, stale_time, category, 1)

response = flask.Response(result)
response.headers["Content-Type"] = result.headers["Content-Type"]
response.headers["Content-length"] = result.headers["Content-length"]
response.headers["Content-Disposition"] = result.headers["Content-Disposition"]

return response
```
