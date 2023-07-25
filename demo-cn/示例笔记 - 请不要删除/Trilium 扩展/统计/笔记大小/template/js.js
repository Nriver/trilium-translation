const notes = await api.runOnBackend(() => {
    const blobSizes = api.sql.getMap(`SELECT blobId, LENGTH(content) FROM blobs`);
    const noteBlobIds = api.sql.getRows(`
        SELECT
            notes.noteId,
            notes.blobId,
            GROUP_CONCAT(revisions.blobId) AS revisions_blobIds,
            GROUP_CONCAT(note_attachments.blobId) AS note_attachments_blobIds,
            GROUP_CONCAT(revision_attachments.blobId) AS revision_attachments_blobIds
        FROM
            notes
            LEFT JOIN revisions USING (noteId)
            LEFT JOIN attachments AS note_attachments ON notes.noteId = note_attachments.ownerId
            LEFT JOIN attachments AS revision_attachments ON revisions.revisionId = revision_attachments.ownerId
        GROUP BY noteId`);
    
    let noteSizes = [];
    
    for (const {noteId, blobId, revisions_blobIds, note_attachments_blobIds, revision_attachments_blobIds} of noteBlobIds) {
       const blobIds = new Set(`${blobId},${revisions_blobIds},${note_attachments_blobIds},${revision_attachments_blobIds}`.split(',').filter(blobId => !!blobId));
        
        const lengths = [...blobIds].map(blobId => blobSizes[blobId] || 0);
        const totalLength = lengths.reduce((partialSum, a) => partialSum + a, 0);
        
        noteSizes.push({ noteId, size: totalLength });
    }
    
    noteSizes.sort((a, b) => a.size > b.size ? -1 : 1);
    
    noteSizes = noteSizes.splice(0, 100);
    
    return noteSizes;
});

const $statsTable = api.$container.find('.stats-table');

function formatSize(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

for (const note of notes) {     
    $statsTable.append(
        $("<tr>")
            .append(
                $("<td>").append(await api.createNoteLink(note.noteId, {showNotePath: true}))
            ) 
            .append(
                //$("<td nowrap>").text(note.size + " bytes")
                $("<td nowrap>").text(formatSize(note.size))
            )
    );
}