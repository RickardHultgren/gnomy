let treeData = {
    name: "Root",
    children: [
      {
        name: "Branch A",
        children: [{ name: "Leaf A1" }, { name: "Leaf A2" }],
      },
      { name: "Branch B" },
    ],
  };

  const width = 600;
  const height = 400;

  const svg = d3.select("svg");
  const treeLayout = d3.tree().size([width, height - 100]);

  let markedNode = null;

  function updateTree() {
    const root = d3.hierarchy(treeData);
    treeLayout(root);

    // Update nodes
    const nodes = svg.selectAll(".node").data(root.descendants(), (d) => d.data.name);

    const nodeEnter = nodes
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.x},${height - d.y})`)
      .on("click", (event, d) => {
        markedNode = d;
        markBranch(d);
      });

    nodeEnter.append("circle").attr("r", 5);
    nodeEnter.append("text").attr("dy", -8).text((d) => d.data.name);

    nodes
      .merge(nodeEnter)
      .transition()
      .duration(500)
      .attr("transform", (d) => `translate(${d.x},${height - d.y})`);

    nodes.exit().remove();

    // Update links
    const links = svg.selectAll(".link").data(root.links(), (d) => `${d.source.data.name}-${d.target.data.name}`);

    links
      .enter()
      .insert("path", "g")
      .attr("class", "link")
      .merge(links)
      .transition()
      .duration(500)
      .attr(
        "d",
        d3
          .linkVertical()
          .x((d) => d.x)
          .y((d) => height - d.y)
      );

    links.exit().remove();
  }

  function markBranch(d) {
    // Clear all marks
    svg.selectAll(".node circle").classed("marked", false).classed("child", false);
    svg.selectAll(".node text").classed("marked", false).classed("child", false);
    svg.selectAll(".link").classed("marked", false).classed("child", false);

    // Mark the selected branch
    d3.select(d3.select(`.node circle:nth-of-type(${d.depth + 1})`).node())
      .classed("marked", true);

    d3.selectAll(d.ancestors().reverse()).selectAll(".node").classed("marked", true);
  }

  function addNode() {
    if (markedNode) {
      if (!markedNode.data.children) markedNode.data.children = [];
      markedNode.data.children.push({ name: "new node" });
      updateTree();
    }
  }

  document.getElementById("addNodeButton").addEventListener("click", addNode);

  updateTree();
