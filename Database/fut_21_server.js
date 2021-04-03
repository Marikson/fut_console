var jsonServer  = require('json-server')
var server      = jsonServer.create()
var router      = jsonServer.router(require('./multi_db.js')())
var middlewares = jsonServer.defaults()

server.use(middlewares)
server.use(router)
server.listen(3000, function () {
console.log('FUT_21_json Server is running')
})

