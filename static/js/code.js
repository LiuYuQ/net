$(function(){
  	$.get('/graph', function(result) {
    	var style = [
      		{ selector: 'node',
      			css: {"width": "20",
    			"height": "20",
      			"content": "data(name)",
    			"font-size": "10px",
    			"text-valign": "center",
    			"text-halign": "center",
    			"background-color": "#555",
    			"text-outline-color": "#555",
    			"text-outline-width": "2px",
   			 	"color": "#fff",
    			"overlay-padding": "6px",
    			"z-index": "10"}
      		},
      		{ selector: "node:selected",
  			css: {
   				"border-width": "6px",
    			"border-color": "#AAD8FF",
    			"border-opacity": "0.5",
    			"background-color": "#77828C",
    			"text-outline-color": "#77828C"}
			},
      		{ selector:'node[exp>5]',
      		css:{"width": "80",
    			"height": "80"
      			<!--"background-color": "#0000CC",-->
      			}
      		},
      		{ selector:'node[exp>3]',
      		css:{"width": "60",
    			"height": "60"
    			<!--"background-color": "#0066FF",-->
      			}
      		},
      		{ selector:'node[exp>2]',
      		css:{"width": "40",
    			"height": "40"
    			<!--"background-color": "#99BBFF",-->
      			}
      		},
      		{ selector:'edge[relationship>0]',
      		css:{'line-color':'#FF0000',
      		"opacity": "0.4"}
      		},
      		{ selector:'edge[relationship<0]',
      		css:{'line-color':'#000000',
      		"opacity": "0.4"}
      		}
      	];

    	var cy = cytoscape({
     		container: document.getElementById('cy'),
    		style: style,
    		layout: { name: 'cose', fit: true },
    	    elements: result.elements
   		});
 	}, 'json');
});