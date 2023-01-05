/*
    执行这个笔记可以跳转到`今天`
*/
const todayNote = await api.getTodayNote();
await api.waitUntilSynced();
api.activateNote(todayNote.noteId);