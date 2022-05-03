const locationPlot = vl.markBar({cornerRadius: 5, width:50}).
    encode(
        vl.y().fieldO('location').title(null).axis({labelFontSize: 14}),
        vl.x().aggregate("sum").field("amount").stack('normalize').axis({labelFontSize: 12, tickCount:10, title: "", labelExpr: "datum.label*100+'%'"}),
        vl.color().field("drink").scale({scheme: "category20"}).
            legend({orient: "bottom", titleFontSize: 20, title:"", labelFontSize: 14, columns: 4}),
        vl.tooltip("drink")
    )


locationPlot
    .data(data)
    .config({view: {stroke: null}}) // no cell borders
    .width(width) // predefined as width of the screen
    .render()
    .then(viewElement => {
        document.getElementById('chart3').appendChild(viewElement); 
    })