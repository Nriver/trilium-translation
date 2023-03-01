/*
 * 作者: Nate
 * Trilium启动时随机选一条信息显示 MoTD（Message of The Day）功能
 * 给前端js笔记加上 #run=frontendStartup 的属性就能在起动时运行了
 */

console.log("banner startup notification 启动通知");

// read config from config files
// 从配置文件读取信息
var messages = config.messages;

api.showMessage(messages[Math.floor(Math.random()*messages.length)]);