1. 先发送根url加参数获取所有山东临工相关信息：

    ```
    https://m.weibo.cn/api/container/getIndex?
    containerid:100103type=60&q=山东临工&t=0
    lfid:106003type=1
    luicode:10000011
    queryVal:山东临工
    title:山东临工
    type:all
    page:0
    ```

2. 因为部分博文为点击`全文`后加载，所以找到请求地址，发送

    - 根据观察，发现，`全文`地址为：`https://m.weibo.cn/status/4103996270375689`
    后面数字为`id`，`id`可以在上一步中每条博文内获取。
    - 获取所有博文内容及评论信息(评论信息为ajax加载) ，地址为：
    `https://m.weibo.cn/api/comments/show?id=4103996270375689&page=2`
