// data is loaded in the html script and can be used here as a variable
const markBar = vl.markBar({width: {"band": 0.8}, cornerRadiusEnd:0, fillOpacity: 1, stroke: "black"}).
    encode(
      vl.x().fieldO('timestamp').timeUnit('dateofmonth').
        title("May").
          axis({titleFontSize: 14, format: "%d", tickCount:10, labelFontSize:12}),
      vl.y().sum('relative_intake').title("Goal Reached").axis({labelFontSize: 12, titleFontSize: 16, tickCount:10, labelExpr: "datum.label+'%'"}),
      vl.color().field("drink").legend({orient: "bottom", titleFontSize: 20, title:"", labelFontSize: 14, columns: 8}).scale({scheme: "category20"}),
      vl.tooltip("drink")
  )

  const line = vl.markRule({strokeDash: [10,2]}).
    encode(
      vl.y({datum: 99.6})
    )

  const plot = vl.layer(line, markBar)

  plot
    .data(data.filter(x => {
        var date = new Date(x.timestamp);
        const d = new Date();
        return date.getMonth() == d.getMonth();
    }))
    .transform(
        vl.calculate("(datum.water_amount*100)/2500").as("relative_intake")
    )
    .config({view: {stroke: null}}) // no cell borders
    .width(width)
    .render()
    .then(viewElement => {
        document.getElementById('chart1').appendChild(viewElement); 
})