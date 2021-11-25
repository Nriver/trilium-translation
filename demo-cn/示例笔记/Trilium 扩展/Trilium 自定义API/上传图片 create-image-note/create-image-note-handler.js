return
var SECRET_PASSWORD = '你的密码';

const {req, res} = api;
const {secret, title, content, type, target} = req.body;
api.log('创建笔记api调用');

// path 是当前api的路径, 比如 create-new-note
//const path = req.params.path + //req.params[0];
//api.log("path "+ path);

// 后端代码router定义
// trilium/src/routes/routes.js
// route(POST, '/api/images', [auth.checkApiAuthOrElectron, uploadMiddleware, csrfMiddleware], imageRoute.uploadImage, apiResultHandler);
// 必须要有 uploadMiddleware 的接口才能上传文件...
// 如果有这个uploadMiddleware, 文件可以通过req.file访问
// const file = req.file;
// api.log("file " + file);
// custom的自定义接口没有这个middleware所以怎么都传不了, 而且multipar-form的数据也不解析, 坑死了
// 看来只能通过json传图片了

api.log("secret "+ secret);
api.log("title "+ title);
api.log("type "+ type);

var imageData = Buffer.from(content, 'base64');


// 这里加了一个secret作为验证密码 防止匿名调用
if (req.method == 'POST' && secret === SECRET_PASSWORD) {
    var targetParentNoteId;
    if (target === 'today'){
        targetParentNoteId = await api.getTodayNote().noteId;
    } else {
        targetParentNoteId = await api.currentNote.getRelationValue('targetNote');
    }
    
    
    api.log("targetParentNoteId");
    api.log(targetParentNoteId);
    const noteParams = {
        parentNoteId: targetParentNoteId,
        title: title,
        content: imageData,
        type: type,
    }
    
    const {note} = await api.createNewNote(noteParams);

    res.status(201).json(note);
}
else {
    api.log("请求参数错误, 返回400");
    res.send(400);
}