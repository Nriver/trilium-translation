api.addButtonToToolbar({
    title: '今天',
    icon: 'calendar-star',
    // 快捷键
    shortcut: 'alt+t',
    // 触发的异步函数
    action: async function() {
        const todayNote = await api.getTodayNote();

        await api.waitUntilSynced();
        
        api.activateNote(todayNote.noteId);
    }
});