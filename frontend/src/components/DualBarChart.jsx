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

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#E5E7EB", // Tailwind's text-gray-200
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#E5E7EB", // Axis label color
        },
        grid: {
          color: "rgba(255,255,255,0.1)", // Optional: subtle grid lines
        },
      },
      y: {
        ticks: {
          color: "#E5E7EB",
        },
        grid: {
          color: "rgba(255,255,255,0.1)",
        },
      },
    },
  };

  return (
    <div className="p-4 rounded-xl shadow bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200">
      <div className="w-full h-[400px]">
        <Bar data={config} options={options} />
      </div>
    </div>
  );
}
