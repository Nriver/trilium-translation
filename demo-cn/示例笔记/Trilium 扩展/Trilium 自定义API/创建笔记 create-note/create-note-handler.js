// 安全考虑，默认不启用。
// 如果要启用，请先修改 SECRET_PASSWORD 然后再去掉这个return。
return
var SECRET_PASSWORD = '你的密码';

const {req, res} = api;
const {secret, title, content} = req.body;
api.log('创建笔记api调用');
api.log(secret, title, content);

function getKeys(obj){
    console.log("===========");
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            console.log(key);
        }
    }
    console.log("===========");
}

getKeys(req.body);

// 这里加了一个secret作为验证密码 防止匿名调用
if (req.method == 'POST' && secret === SECRET_PASSWORD) {
    // notes must be saved somewhere in the tree hierarchy specified by a parent note. 
    // This is defined by a relation from this code note to the "target" parent note
    // alternetively you can just use constant noteId for simplicity (get that from "Note Info" dialog of the desired parent note)
    var targetParentNoteId;
    if (target === 'today'){
        targetParentNoteId = await api.getTodayNote().noteId;
    } else {
        targetParentNoteId = await api.currentNote.getRelationValue('targetNote');
    }
    api.log("targetParentNoteId");
    api.log(targetParentNoteId);
    const {note} = await api.createTextNote(targetParentNoteId, title, content);

    res.status(201).json(note);
}
else {
    res.send(400);
}