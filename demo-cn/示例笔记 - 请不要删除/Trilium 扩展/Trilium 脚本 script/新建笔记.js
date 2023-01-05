/*
    createTextNote 的第一个参数是 父级笔记ID 改成你的笔记的ID 运行这个笔记会在你的笔记下创建一个子笔记
*/
const newNoteId = await api.runOnBackend(async () => {
    const {note} = await api.createTextNote("你的笔记ID", "默认标题", "默认内容");
    return note.noteId
})
await api.waitUntilSynced();
api.activateNote(newNoteId);