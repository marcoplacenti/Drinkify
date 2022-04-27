console.log(data)
const linePlot = vl.markLine().
    encode(
        vl.x().fieldO('timestamp').timeUnit('hoursofhour'),
        vl.y().count()
    )
linePlot
    .data(data)
    .width(width) // predefined as width of the screen
    .render()
    .then(viewElement => {
        document.getElementById('chart2').appendChild(viewElement); 
    })
