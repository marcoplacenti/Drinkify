// data is loaded in the html script and can be used here as a variable
const barPlot2 = vl.markBar().
    encode(
        vl.x().fieldO('timestamp').timeUnit('yearmonthdate'),
        vl.y().sum('water_amount'),
        vl.color().fieldN("drink")
    )
barPlot2
    .data(data.filter(x => {
        var date = new Date(x.timestamp);
        const d = new Date();
        return date.getMonth() == d.getMonth()
    }))
    .width(width)
    .render()
    .then(viewElement => {
        document.getElementById('chart1').appendChild(viewElement); 
    })