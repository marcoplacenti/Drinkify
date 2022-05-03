const heatmap = vl.markRect()
    .data(data)
    //.params(brush)
    //.select(vl.selectInterval().encodings("x").empty("none"))
    .transform(vl.calculate("month(datum.date)").as('month'))
    .encode(
    vl.x().fieldO("timestamp").timeUnit("date").title("").axis({labelFontSize: 11}),
    vl.y().fieldO("timestamp").timeUnit("hours").title("").sort("descending").axis({labelFontSize: 11}),
    //vl.color().if(vl.selectInterval().encodings("x").empty("none"), vl.value("firebrick")).value("steelblue"),
    vl.color().sum("amount").scale({scheme: "spectral", reverse: true}).legend({labelExpr: "datum.label+' ml'", title: "", labelFontSize: 12}),
    vl.tooltip().sum("amount")
    )


heatmap
    .data(data)
    .config({view: {stroke: null}}) // no cell borders
    .width(width) // predefined as width of the screen
    .render()
    .then(viewElement => {
        document.getElementById('chart5').appendChild(viewElement); 
    })