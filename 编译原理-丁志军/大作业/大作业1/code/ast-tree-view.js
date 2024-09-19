import $ from "jquery"

class TreeView {
  constructor() {
    this.buffer = []
    this.scaleProp = "ast_tree_scale"
    this.scale(0.75)
    const baseFactor = 11 / 10
    $("#ast-zoom-in").on("click", () => {
      this.scale(baseFactor)
    })
    $("#ast-zoom-out").on("click", () => {
      this.scale(1 / baseFactor)
    })
  }
  scale(factor) {
    if (!window[this.scaleProp]) {
      window[this.scaleProp] = 1
    }
    window[this.scaleProp] *= factor;
    $("#ast-tree").css("transform", `scale(${window[this.scaleProp]})`)
  }
  draw(tree) {
    if (typeof tree === "object" && !Array.isArray(tree)) {
      $("#ast-tree").html("");
      this.buffer = ["<ul>"];
      this.drawChildNode(tree);
      this.buffer.push("</ul>");
      $("#ast-tree").html(this.buffer.join(""));
    } else {
      console.error(`Cannot display ${typeof tree} in TreeView: ${tree}`)
    }
  }
  drawNode(node) {
    for (const prop in node) {
      if (prop === "children") {
        if (node["children"].length > 0) {
          this.buffer.push("</div><ul>");
          for (const child of node["children"]) {
            this.drawChildNode(child)
          }
          this.buffer.push("</ul>");
        }
      } else if (prop === "root") {
        this.buffer.push(`<span> ${node[prop]} </span>`);
      }
    }
  }
  drawChildNode(child) {
    this.buffer.push(`<li><div class="ast-tree-node">`);
    // fetch the parent object
    this.drawNode(child);
    // push the closing tag for parent
    this.buffer.push("</li>");
  }
}

// call the function on page load
window.addEventListener("load", () => {
  window.treeView = new TreeView()
})