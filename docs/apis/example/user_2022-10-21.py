"""
@api {post} /api/example_api/users 注册
@apiVersion 1.0.0
@apiName register_user
@apiGroup Users
@apiDescription 手机用户注册
@apiParam {String} mobile  用户手机号
@apiParam {String} password 用户密码
@apiParam {String} sms_code 用户短信验证码
@apiParamExample {json} Request-Example:
 {
  mobile: "13000000000",
  password: "123456",
  sms_code: "907896"
 }
@apiSuccess (回参) {int} user_id 用户注册id
@apiSuccess (回参) {String} name 用户昵称
@apiSuccess (回参) {String} mobile 用户注册手机号
@apiSuccessExample {json} Success-Response:
 {
  "errno":0,
  "errmsg":"注册成功！",
  "data": {
   "user_id": 1,
   "name": "lifangjun",
   "mobile": "13000000000",
  }
 }
@apiErrorExample {json} Error-Response:
 {
  "errno":4001,
  "errmsg":"数据库查询错误！"
 }
"""