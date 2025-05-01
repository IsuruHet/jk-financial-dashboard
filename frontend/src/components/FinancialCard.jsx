import React from "react";
import { Line, Bar } from "react-chartjs-2";

export default function FinancialCard({ title, type, data }) {
  const Chart = type === "bar" ? Bar : Line;

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#E5E7EB", // Light text color for legend in dark mode
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#E5E7EB", // Light text color for axis labels
        },
        grid: {
          color: "rgba(255,255,255,0.1)", // Light grid color
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
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <div className="w-full h-[400px]">
        <Chart data={data} options={options} />
      </div>
    </div>
  );
}
