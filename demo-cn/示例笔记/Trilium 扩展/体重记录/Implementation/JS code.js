async function getChartData() {
    const days = await api.runOnServer(() => {
        const label_name = '体重';
        const notes = api.getNotesWithLabel(label_name);
        const days = [];

        for (const note of notes) {
            const date = note.getLabelValue('dateNote');
            const weight = parseFloat(note.getLabelValue(label_name));

            if (date && weight) {
                days.push({ date, weight });
            }
        }

        days.sort((a, b) => a.date > b.date ? 1 : -1);

        return days;
    });

    const datasets = [
        {
            label: "体重(kg)",
            backgroundColor: 'red',
            borderColor: 'red',
            data: days.map(day => day.weight),
            fill: false,
            spanGaps: true,
            datalabels: {
                display: false
            }
        }
    ];

    return {
        datasets: datasets,
        labels: days.map(day => day.date)
    };
}

const ctx = $("#canvas")[0].getContext("2d");

new chartjs.Chart(ctx, {
    type: 'line',
    data: await getChartData()
});
