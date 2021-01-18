# fastapi start project

这个起始的项目中主要是用户的jwt登录

首先介绍一下什么是JSON Web Token（JWT）？
官方文档是这样解释的：JSON Web Token（JWT）是一个开放标准（RFC 7519），它定义了一种紧凑且独立的方式，可以在各方之间作为JSON对象安全地传输信息。此信息可以通过数字签名进行验证和信任。JWT可以使用秘密（使用HMAC算法）或使用RSA或ECDSA的公钥/私钥对进行签名。

## 注意
因为fastapi中给的项目结构太乱了，所有的model都放在一个model.py中，所有的内容都都放在一个CRUD里面，我感觉这样的项目是不好维护的
所有自己整理了一个项目结构


