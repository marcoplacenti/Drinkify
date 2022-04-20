// data is loaded in the html script and can be used here as a variable
const barPlot2 = vl.markBar().
    encode(
        vl.x().fieldO('time').timeUnit('hoursofhour'),
        vl.y().count()
    )
barPlot2
    .data(data) 
    .width(width)
    .render()
    .then(viewElement => {
        document.getElementById('chart1').appendChild(viewElement); 
    })