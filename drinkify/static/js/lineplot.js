console.log(data)
const linePlot = vl.markLine().
    encode(
        vl.x().fieldO('time').timeUnit('hoursofhour'),
        vl.y().count()
    )
linePlot
    .data(data)
    .width(width) // predefined as width of the screen
    .render()
    .then(viewElement => {
        document.getElementById('chart1').appendChild(viewElement); 
    })

console.log("EHHEOFHEDJKNG")
console.log(data['time'])