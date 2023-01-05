/*
 * 作者: Nate
 * Trilium启动时随机选一条信息显示 MoTD（Message of The Day）功能
 */

console.log("banner notification 启动通知");

var messages = [
    "欢迎回来~",
    "深呼吸 xi~~ 放轻松 hu~~",
    "抬头看看蓝天吧~",
    "世界是实力至上的，要多在正确的方向上努力",
    "给自己多充充电，多学点东西，总会有用得到的地方",
    "锻炼身体能让人焕然一新，有事没事锻炼一下总没错",
    "书是好东西，要多看书",
    "Trilium是第二大脑",
    "爱护自己",
    "出门在外保护好自己",
    "吾生也有涯，而知也无涯。",
]


api.showMessage(messages[Math.floor(Math.random()*messages.length)]);