// data is loaded in the html script and can be used here as a variable
vl.markBar({cornerRadius: 5, width:50}).
  encode(
    vl.y().fieldO('location').title(null).axis({labelFontSize: 14}),
    vl.x().aggregate("sum").field("amount").stack('normalize').axis(null),
    vl.color().field("drink").scale({scheme: "category20"}).
      legend({orient: "bottom", titleFontSize: 20, title:"Type of drink", labelFontSize: 14, columns: 4})
  ).
  data(data)
    .width(width)
    .render()
    .then(viewElement => {
        document.getElementById('chart1').appendChild(viewElement); 
    })