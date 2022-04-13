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
const width  = window.innerWidth || document.documentElement.clientWidth || 
document.body.clientWidth;
const height = window.innerHeight|| document.documentElement.clientHeight|| 
document.body.clientHeight;