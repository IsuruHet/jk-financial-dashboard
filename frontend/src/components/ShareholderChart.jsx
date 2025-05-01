import React from "react";
import { Pie } from "react-chartjs-2";

export default function ShareholderChart({ data, year }) {
  const filtered = data.filter((d) => d.year);
  const labels = filtered.map((s) => s.shareholder_name);
  const percentages = filtered.map((s) => parseFloat(s.share_percentage));

  const chartData = {
    labels,
    datasets: [
      {
        label: "Share %",
        data: percentages,
        backgroundColor: [
          "#4ade80",
          "#60a5fa",
          "#facc15",
          "#f87171",
          "#a78bfa",
          "#fb923c",
          "#34d399",
          "#f472b6",
          "#c084fc",
          "#38bdf8",
          "#fbbf24",
          "#f97316",
          "#ef4444",
          "#6366f1",
          "#14b8a6",
          "#0ea5e9",
          "#22c55e",
          "#e879f9",
          "#f43f5e",
          "#64748b",
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "#E5E7EB",
        },
      },
    },
  };

  return (
    <div className="p-4 rounded-xl shadow bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200">
      <h2 className="text-xl font-semibold mb-4">
        Top 20 Shareholders - {year}
      </h2>
      <div className="w-[900px] h-[500px] mx-auto">
        <Pie data={chartData} options={chartOptions} />
      </div>
    </div>
  );
}
