// enable vega lite API
const options = {
    config: {
    // Vega-Lite default configuration
    },
    init: (view) => {
    // initialize tooltip handler
    view.tooltip(new vegaTooltip.Handler().call);
    },
    view: {
    // view constructor options
    // remove the loader if you don't want to default to vega-datasets!
    renderer: "canvas",
    },
};

// register vega and vega-lite with the API
vl.register(vega, vegaLite, options);
var scale = 0.85;
const width  = window.innerWidth*scale || document.documentElement.clientWidth*scale || 
document.body.clientWidth*scale;
const height = window.innerHeight*scale|| document.documentElement.clientHeight*scale|| 
document.body.clientHeight*scale;