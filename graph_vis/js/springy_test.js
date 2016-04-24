$(function() {

    var graph = new Springy.Graph();

    for (var i = 0; i < nodes.length; ++i) {
        graph.addNodes(nodes[i]);
    }

    for (var i = 0; i < 50; ++i) {
        graph.addEdges(edges[i]);
    }

    jQuery(function(){
        var springy = jQuery('#springydemo').springy({
          graph: graph
        });
    });
});
