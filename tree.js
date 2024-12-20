<script>
  const width = 800, height = 600;
  let currentNodeId = 0;
  const treeData = { id: currentNodeId++, name: "Center", children: [] };
  let selectedNode = null;

  const svg = d3.select("#mindmap")
    .attr("width", width)
    .attr("height", height);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const treeLayout = d3.tree().nodeSize([100, 100]);
  const root = d3.hierarchy(treeData);

  function update() {
    // Update tree layout
    const nodes = root.descendants();
    const links = root.links();

    treeLayout(root);

    // Update links
    const link = g.selectAll(".link")
      .data(links, d => `${d.source.data.id}-${d.target.data.id}`);

    link.enter()
      .append("path")
      .attr("class", "link")
      .merge(link)
      .attr("d", d3.linkVertical()
        .x(d => d.x)
        .y(d => d.y));

    link.exit().remove();

    // Update nodes
    const node = g.selectAll(".node")
      .data(nodes, d => d.data.id);

    const nodeEnter = node.enter()
      .append("circle")
      .attr("class", "node")
      .attr("r", 20)
      .on("click", function (e, d) {
        d3.selectAll(".node").classed("selected", false);
        d3.select(this).classed("selected", true);
        selectedNode = d;
        e.stopPropagation();
      });

    nodeEnter.merge(node)
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);

    node.exit().remove();
  }

  update();

  // Button actions
  d3.select("#add-branch").on("click", () => {
    if (!selectedNode) return;

    // Ensure `children` array exists
    if (!selectedNode.data.children) {
      selectedNode.data.children = [];
      selectedNode.children = [];
    }

    // Add a new child node
    const newChild = { id: currentNodeId++, name: `Node ${currentNodeId}`, children: [] };
    selectedNode.data.children.push(newChild);

    // Recreate the hierarchy for the selected node
    selectedNode.children = selectedNode.data.children.map(d3.hierarchy);

    // Update the tree
    update();
  });

  d3.select("#delete-branch").on("click", () => {
    if (!selectedNode || selectedNode === root) return;

    const parent = selectedNode.parent;
    parent.data.children = parent.data.children.filter(d => d.id !== selectedNode.data.id);
    parent.children = parent.data.children.length ? parent.data.children.map(d3.hierarchy) : null;
    selectedNode = null;
    update();
  });

  // Deselect node on background click
  svg.on("click", () => {
    d3.selectAll(".node").classed("selected", false);
    selectedNode = null;
  });
</script>
