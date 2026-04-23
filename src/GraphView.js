import React, { useEffect, useState } from "react";
import axios from "axios";
import CytoscapeComponent from "react-cytoscapejs";

const API = "http://127.0.0.1:8000";

function GraphView({ onNodeClick }) {
  const [elements, setElements] = useState([]);

  useEffect(() => {
    fetchGraph();
  }, []);

  const fetchGraph = async () => {
    const res = await axios.get(`${API}/notes/graph/`);
    const data = res.data;

    const nodes = data.nodes.map(n => ({
      data: { id: n.id.toString(), label: n.title }
    }));

    const edges = data.edges.map(e => ({
      data: {
        source: e.source.toString(),
        target: e.target.toString()
      }
    }));

    setElements([...nodes, ...edges]);
  };

  return (
    <CytoscapeComponent
      elements={elements}
      style={{ width: "100%", height: "450px" }}
      layout={{
        name: "cose",
        animate: true,
        fit: true,
        padding: 30
      }}
      stylesheet={[
        {
          selector: "node",
          style: {
            label: "data(label)",
            "background-color": "#007bff",
            color: "#fff",
            "text-valign": "center",
            "text-halign": "center",
            "font-size": "10px"
          }
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#ccc",
            "target-arrow-color": "#ccc",
            "target-arrow-shape": "triangle"
          }
        },
        {
          selector: ".highlight",
          style: {
            "background-color": "#ff5722",
            "line-color": "#ff5722",
            "target-arrow-color": "#ff5722"
          }
        }
      ]}
      cy={(cy) => {
        cy.on("tap", "node", (evt) => {
          const node = evt.target;
          onNodeClick(node.id());
        });

        cy.on("mouseover", "node", (evt) => {
          const node = evt.target;

          cy.elements().removeClass("highlight");

          node.addClass("highlight");
          node.connectedEdges().addClass("highlight");
          node.connectedEdges().targets().addClass("highlight");
        });
      }}
    />
  );
}

export default GraphView;