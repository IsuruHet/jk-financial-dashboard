import React from "react";
import { Line, Bar } from "react-chartjs-2";

export default function FinancialCard({ title, type, data }) {
  const Chart = type === "bar" ? Bar : Line;
  return (
    <div className="p-4 rounded-xl shadow bg-white dark:bg-gray-800 dark:text-white">
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <Chart data={data} />
    </div>
  );
}
