// Set up the D3 environment and mindmap div dimensions
const mindmap = d3.select("#mindmap");
const width = parseInt(mindmap.style("width"));
const height = parseInt(mindmap.style("height"));

// Reference to the currently marked node
let markedNode = null;

// Function to generate a random position within the mindmap div
function getRandomPosition() {
    const x = Math.random() * (width - 80);  // Subtract node width
    const y = Math.random() * (height - 80); // Subtract node height
    //const x = Math.random() * (100 - 80);  // Subtract node width
    //const y = Math.random() * (100 - 80); // Subtract node height

    return { x, y };
}

// D3 Drag Behavior for Nodes
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

// Function to mark a node
function markNode(node) {
    if (markedNode) {
        markedNode.classed("marked", false);
    }
    node.classed("marked", true);
    markedNode = node;
    document.getElementById("deleteNodeBtn").style.display = "inline";
}

// Function to unmark the currently marked node
function unmarkNode() {
    if (markedNode) {
        markedNode.classed("marked", false);
        markedNode = null;
        document.getElementById("deleteNodeBtn").style.display = "none";
    }
}

// Function to add a mindmap node
function addNode() {
    alert("hej1");
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
    alert("hej2");
}

// Function to delete the marked node
function deleteNode() {
    if (markedNode) {
        markedNode.remove();
        markedNode = null;
        document.getElementById("deleteNodeBtn").style.display = "none";
    }
}

// Function to create a branch (line with two endpoints)
function addBranch() {
    const startPos = getRandomPosition();
    const endPos = getRandomPosition();

    // Append line (branch)
    const line = mindmap.append("line")
        .attr("class", "branch")
        .attr("x1", startPos.x + 5)  // Adjusting to match center of the endpoint
        .attr("y1", startPos.y + 5)
        .attr("x2", endPos.x + 5)
        .attr("y2", endPos.y + 5);

    // Append label for the line
    const label = mindmap.append("div")
        .attr("class", "label")
        .style("left", `${(startPos.x + endPos.x) / 2}px`)
        .style("top", `${(startPos.y + endPos.y) / 2}px`)
        .text("path");

    // Append endpoints (movable circles)
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
                    line.attr("x1", newX + 5).attr("y1", newY + 5);  // Adjusting to match center
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
                    line.attr("x2", newX + 5).attr("y2", newY + 5);  // Adjusting to match center
                    label.style("left", `${(newX + parseInt(endpoint1.style("left"))) / 2}px`)
                        .style("top", `${(newY + parseInt(endpoint1.style("top"))) / 2}px`);
                })
        );
}

// Add event listeners to buttons
alert("hej0");
document.getElementById("addNodeBtn").addEventListener("click", addNode);
document.getElementById("addBranchBtn").addEventListener("click", addBranch);
document.getElementById("deleteNodeBtn").addEventListener("click", deleteNode);

// Add event listener to mindmap for background clicks to unmark the node
mindmap.on("click", function() {
    unmarkNode();
});
