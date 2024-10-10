document.addEventListener("DOMContentLoaded", function() {
    // Set up the D3 environment and mindmap div dimensions
    const mindmap = d3.select("#mindmap");
    const width = parseInt(mindmap.style("width"));
    const height = parseInt(mindmap.style("height"));

    let markedNode = null;

    function getRandomPosition() {
        const x = Math.random() * (width - 80);  
        const y = Math.random() * (height - 80); 
        return { x, y };
    }

    function dragStarted(event, d) {
        d3.select(this).style("cursor", "grabbing");
    }

    function dragged(event, d) {
        d3.select(this)
            .style("left", `${event.x}px`)
            .style("top", `${event.y}px`);
    }

    function dragEnded(event, d) {
        d3.select(this).style("cursor", "grab");
    }

    function markNode(node) {
        if (markedNode) {
            markedNode.classed("marked", false);
        }
        node.classed("marked", true);
        markedNode = node;
        document.getElementById("deleteNodeBtn").style.display = "inline";
    }

    function unmarkNode() {
        if (markedNode) {
            markedNode.classed("marked", false);
            markedNode = null;
            document.getElementById("deleteNodeBtn").style.display = "none";
        }
    }

    function addNode() {
        const position = getRandomPosition();
        const node = mindmap.append("div")
            .attr("class", "node")
            .style("left", `${position.x}px`)
            .style("top", `${position.y}px`)
            .text("tree")
            .call(
                d3.drag()
                    .on("start", dragStarted)
                    .on("drag", dragged)
                    .on("end", dragEnded)
            )
            .on("click", function(event) {
                event.stopPropagation();
                markNode(d3.select(this));
            });
    }

    function deleteNode() {
        if (markedNode) {
            markedNode.remove();
            markedNode = null;
            document.getElementById("deleteNodeBtn").style.display = "none";
        }
    }

    function addBranch() {
        const startPos = getRandomPosition();
        const endPos = getRandomPosition();

        const line = mindmap.append("line")
            .attr("class", "branch")
            .attr("x1", startPos.x + 5)
            .attr("y1", startPos.y + 5)
            .attr("x2", endPos.x + 5)
            .attr("y2", endPos.y + 5);

        const label = mindmap.append("div")
            .attr("class", "label")
            .style("left", `${(startPos.x + endPos.x) / 2}px`)
            .style("top", `${(startPos.y + endPos.y) / 2}px`)
            .text("path");

        const endpoint1 = mindmap.append("div")
            .attr("class", "endpoint")
            .style("left", `${startPos.x}px`)
            .style("top", `${startPos.y}px`)
            .call(
                d3.drag()
                    .on("drag", function(event) {
                        const newX = event.x;
                        const newY = event.y;
                        d3.select(this).style("left", `${newX}px`).style("top", `${newY}px`);
                        line.attr("x1", newX + 5).attr("y1", newY + 5);  
                        label.style("left", `${(newX + parseInt(endpoint2.style("left"))) / 2}px`)
                            .style("top", `${(newY + parseInt(endpoint2.style("top"))) / 2}px`);
                    })
            );

        const endpoint2 = mindmap.append("div")
            .attr("class", "endpoint")
            .style("left", `${endPos.x}px`)
            .style("top", `${endPos.y}px`)
            .call(
                d3.drag()
                    .on("drag", function(event) {
                        const newX = event.x;
                        const newY = event.y;
                        d3.select(this).style("left", `${newX}px`).style("top", `${newY}px`);
                        line.attr("x2", newX + 5).attr("y2", newY + 5);  
                        label.style("left", `${(newX + parseInt(endpoint1.style("left"))) / 2}px`)
                            .style("top", `${(newY + parseInt(endpoint1.style("top"))) / 2}px`);
                    })
            );
    }

    // Add event listeners to buttons once
    document.getElementById("addNodeBtn").addEventListener("click", addNode);
    document.getElementById("addBranchBtn").addEventListener("click", addBranch);
    document.getElementById("deleteNodeBtn").addEventListener("click", deleteNode);

    mindmap.on("click", function() {
        unmarkNode();
    });
});
