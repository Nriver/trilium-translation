api.addButtonToToolbar({
    title: '体重记录',
    icon: 'star',
    action: async () => api.activateNote(await api.startNote.getRelationValue('targetNote'))
});