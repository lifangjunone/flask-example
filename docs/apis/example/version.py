"""
@api {get} /api/example_api/version API Version
@apiVersion 1.0.0
@apiName get_apiversion
@apiGroup Version
@apiDescription 获取当前API的版本及环境信息
@apiSuccessExample {json} Success-Response:
 {
    "api_version": "v1",
    "app_version": "v0.1",
    "application": "flask-skeleton",
    "platform": "Linux-4.14.0-deepin2-amd64-x86_64-with",
    "production": "flask-example"
}
@apiErrorExample {json} Error-Response:
 {
  "errno":4001,
  "errmsg":"数据库查询错误！"
 }
"""