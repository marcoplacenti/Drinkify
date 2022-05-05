const markArea = vl.markArea().
    encode(
    vl.x().fieldO('timestamp').timeUnit("hours").title(false).
        axis({labelFontSize: 12}),
    vl.y().aggregate("sum").field("amount").stack('normalize').
        axis({grid: false, labelFontSize: 12, titleFontSize:12, labelExpr: "datum.label*100+'%'"}).
        title("Proportion of intake"),
    vl.color().field("drink").
        legend({orient: "bottom", titleFontSize: 20, title:"", labelFontSize: 14, columns: 4}).
        scale({scheme: "category20"}),
    vl.tooltip("drink")
    )


markArea
    .data(data)
    .config({view: {stroke: null}}) // no cell borders
    .width(width) // predefined as width of the screen
    .render()
    .then(viewElement => {
        document.getElementById('chart4').appendChild(viewElement); 
    })