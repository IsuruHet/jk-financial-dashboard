import { useEffect, useState } from "react";
import Header from "../components/Header";
import FileUploader from "../components/FileUploader";
import FinancialCard from "../components/FinancialCard";
import DualBarChart from "../components/DualBarChart";
import { fetchFinancialData } from "../services/api";
import Footer from "../components/Footer";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [currency, setCurrency] = useState("LKR");
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetchFinancialData(currency).then(setData);
  }, [currency]);

  const years = data.map((d) => d.year);

  const chartData = (label, key, color) => ({
    labels: years,
    datasets: [
      {
        label,
        data: data.map((d) => d[key]),
        borderColor: color,
        backgroundColor: color,
        tension: 0.4,
        fill: false,
      },
    ],
  });
  return (
    <div
      className={`${
        darkMode ? "dark bg-gray-900 text-white" : "bg-gray-100 text-black"
      } min-h-screen p-6`}
    >
      <Header {...{ currency, setCurrency, darkMode, setDarkMode }} />
      <FileUploader onUploadComplete={setData} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FinancialCard
          title="Total Revenue"
          type="line"
          data={chartData("Revenue", "revenue", "#10b981")}
        />
        <div className="p-4 rounded-xl shadow bg-white dark:bg-gray-800 dark:text-white">
          <h2 className="text-xl font-semibold mb-2">
            Cost vs Operating Expenses
          </h2>
          <DualBarChart
            years={years}
            costData={data.map((d) => d.cost_of_sales)}
            opexData={data.map((d) => d.operating_expenses)}
          />
        </div>
        <FinancialCard
          title="Gross Profit Margin (%)"
          type="line"
          data={chartData("GPM", "gross_profit_margin", "#facc15")}
        />
        <FinancialCard
          title="Earnings Per Share (EPS)"
          type="line"
          data={chartData("EPS", "eps", "#a78bfa")}
        />
        <FinancialCard
          title="Net Asset Per Share"
          type="line"
          data={chartData("Net Asset/Share", "net_asset_per_share", "#fb923c")}
        />
      </div>
      <Footer />
    </div>
  );
}
