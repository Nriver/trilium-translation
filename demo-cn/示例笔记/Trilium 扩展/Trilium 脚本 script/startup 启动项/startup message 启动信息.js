/*
 * 作者: Nate
 * Trilium启动时随机选一条信息显示
 */

console.log("banner notification 启动通知");

var messages = [
    "欢迎回来~",
    "深呼吸 xi~~ 放轻松 hu~~",
    "抬头看看蓝天吧~"
]


api.showMessage(messages[Math.floor(Math.random()*messages.length)]);