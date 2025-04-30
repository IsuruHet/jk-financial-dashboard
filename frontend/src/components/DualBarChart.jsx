import React from "react";
import { Bar } from "react-chartjs-2";

export default function DualBarChart({ years, costData, opexData }) {
  const config = {
    labels: years,
    datasets: [
      {
        label: "Cost of Sales",
        data: costData,
        backgroundColor: "#f87171",
      },
      {
        label: "Operating Expenses",
        data: opexData,
        backgroundColor: "#60a5fa",
      },
    ],
  };
  return <Bar data={config} />;
}
