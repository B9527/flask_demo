PTIONS

使用该方法来获取资源支持的HTTP方法列表，或者ping服务器。

请求：只有header没有body。
响应：默认只有header，但是也可以在body中添加内容，比如描述性文字
示例：

# 测试对应资源所支持的方法
OPTIONS /test-options HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 204 No Content
Allow: GET, POST, OPTIONS
# ping服务器
OPTIONS * HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 204 No Content
安全：是
幂等：是
显然，它就是一个纯粹的信息读取的操作，不改变资源的状态，同时保证幂等性。

GET

该方法用以获取资源的表述。

请求：只有header，没有body。
响应：对应请求URI的资源表述，通常带有body。响应header中的Content-Type，Content-Length，Content-Language，Last-Modified，ETag等应该和响应body的表述一致。
# 请求
GET /hello HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 200 OK
Content-Type: application/xml; charset=UTF-8
Content-Length: 21
# 此处为空行，由于高亮插件原因，特此注明
<hello>tester</hello>
安全：是
幂等：是
简单的资源信息读取，不对资源状态造成影响，保证幂等性。

HEAD

使用该方法可以获取与GET响应相同的header，但是响应中没有任何body。

请求：只有header，没有body。
响应：只有header，没有body。服务器不能添加body。
# 请求
GET /hello HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 200 OK
Content-Type: application/xml; charset=UTF-8
Content-Length: 21
安全：是
幂等：是
简单的资源信息读取，不对资源状态造成影响，保证幂等性。

POST

让资源在服务器上执行一系列操作，如创建新资源、更新资源、变更资源等。

请求：一个资源的表述。
响应：一个资源的表述，或是一个重定向指令。如果body中存在表述，则其URI和请求URI不一致，包含一个带有改资源URI的Content-Location头。
# 执行动作的请求
POST /prompt/delete HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 204 No Content
# 创建资源的请求
POST /stu/bob HTTP/1.1
Host: localhost
Content-Type: application/xml
# 此处为空行，由于高亮插件原因，特此注明
<student>
	<name>Bob</name>
	<age>22</age>
</student>
# 响应
HTTP/1.1 201 Created
Location: http://localhost/stu/bob
Content-Location: http://localhost/stu/bob
Content-Type: application/xml
# 此处为空行，由于高亮插件原因，特此注明
<student>
	<name>Bob</name>
	<age>22</age>
</student>
# 修改资源的请求
POST /stu/bob/modify HTTP/1.1
Host: localhost
Content-Type: application/json
# 此处为空行，由于高亮插件原因，特此注明
{
	"Name": "Bob",
	"Age": 24
}
# 响应
HTTP/1.1 303 See Other
Location: http://localhost/stu/bob
Content-Type: application/xml
# 此处为空行，由于高亮插件原因，特此注明
<student>
	<name>Bob</name>
	<age>24</age>
</student>
安全：否
幂等：否
是一个资源写的操作，改变了资源的状态，同事HTTP标准设定POST方法为非幂等，也就是说不需要在实现服务端响应方法的时候，我们不需要保证幂等，这也就避免了很多冗余信息(我们会在DELETE中看到)。

PUT

完整地更新或替换一个现有资源，也可以用客户端制定的URI来创建一个新资源。

请求：一个资源的表述。请求的body可以与客户端后续收到的GET请求一样,当然，也可以不一样。在某些情况下，服务器也可要求客户端只提供资源的可变部分。
响应：更新的状态。可在响应中包含被更新资源的完整表述，但是客户端不能假设响应中包含完整状态，除非响应有一个Content-Location头。如果服务器没有包含这个头，客户端必须提交一个无条件GET请求来获取更新后的表述，带有Last-Modified和/或ETag头。
# 更新资源的请求
PUT /stu/bob HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 204 No Content
# 创建资源的请求
PUT /stu/alice HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 201 Created
Location: http://localhost/stu/alice
Content-Length: 0
安全：否
幂等：是
和POST方法一样，PUT方法也改变了资源的状态，所以是非安全的。但是有一点和POST不同，它是幂等的，这是为什么呢？想想setter函数吧，重复调用，只要参数是一样的，表述就是不变的。

DELETE

使用该方法来删除资源。对于客户端而言，资源在成功响应后，就不复存在了。

请求：只有header，没有body。
响应：成功或失败。body中可以包含操作的状态。
# 请求
DELETE /doc/old.txt HTTP/1.1
Host: localhost
# 响应
HTTP/1.1 204 No Content
安全：否
幂等：是
和POST方法一样，DELETE方法也改变了资源的状态，所以是非安全的。但是有一点和POST不同，它是幂等的，也就是说，就算是服务器在前一个请求中已经删除了资源，它也必须返回200.这就意味着，我们在实现服务端的该方法是，需要跟踪已经删除的资源，否则就会返回404的。

TRACE

回显服务器接收到的header。支持该方法的服务器可能存在XST安全隐患。

安全：
幂等：
请求：header与body。
响应：body中包含整个请求消息。
# 请求
TRACE /trace HTTP/1.1
Host: localhost
Accept: text/html
# 响应
HTTP/1.1 200 OK
Content-Type: message/http
# 空行
TRACE /trace HTTP/1.1
Host: localhost
Accept: text/html
qq
