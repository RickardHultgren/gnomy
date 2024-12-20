const width = 800;
const height = 600;

let treeData = {
  name: "Root",
  marked: false,
  children: []
};

let selectedNode = null;

const svg = d3.select("#mindmap")
  .attr("width", width)
  .attr("height", height);

const g = svg.append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

const tree = d3.tree().size([width - 100, height - 100]);

function update(source) {
  const root = d3.hierarchy(treeData);
  tree(root);

  const nodes = root.descendants();
  const links = root.links();

  const link = g.selectAll(".link")
    .data(links, d => d.target.data.id);

  link.enter().append("path")
    .attr("class", "link")
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x))
    .merge(link)
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x));

  link.exit().remove();

  const node = g.selectAll(".node")
    .data(nodes, d => d.data.id);

  const nodeEnter = node.enter().append("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${d.y},${d.x})`)
    .on("click", (event, d) => {
      selectedNode = d;
      update(root);
    });

  nodeEnter.append("circle")
    .attr("r", 10)
    .attr("class", d => d.data.marked ? "marked" : "")
    .on("dblclick", (event, d) => {
      d.data.marked = !d.data.marked;
      update(root);
    });

  nodeEnter.append("text")
    .attr("dy", -15)
    .attr("text-anchor", "middle")
    .text(d => d.data.name)
    .on("dblclick", (event, d) => {
      const newName = prompt("Enter new name:", d.data.name);
      if (newName) d.data.name = newName;
      update(root);
    });

  node.exit().remove();
}

function addBranch() {
  if (selectedNode) {
    const newBranch = {
      name: `Branch ${Math.random().toFixed(2)}`,
      marked: false,
      children: []
    };
    if (!selectedNode.data.children) {
      selectedNode.data.children = [];
    }
    selectedNode.data.children.push(newBranch);
    update(selectedNode);
  } else {
    alert("Please select a node first!");
  }
}

function deleteBranch() {
  if (selectedNode && selectedNode.parent) {
    const index = selectedNode.parent.children.indexOf(selectedNode);
    if (index !== -1) {
      selectedNode.parent.children.splice(index, 1);
    }
    selectedNode = null;
    update(treeData);
  } else {
    alert("Cannot delete root node or no node selected!");
  }
}

document.getElementById("add-branch").addEventListener("click", addBranch);
document.getElementById("delete-branch").addEventListener("click", deleteBranch);

update(treeData);
