export default function Header({
  currency,
  setCurrency,
  darkMode,
  setDarkMode,
}) {
  return (
    <header className="flex justify-between items-center py-6">
      <h1 className="text-3xl font-bold">JKH Financial Dashboard</h1>
      <div className="flex gap-4">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:text-white"
        >
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>

        <button
          onClick={() => setCurrency(currency === "LKR" ? "USD" : "LKR")}
          className="px-4 py-2 rounded bg-blue-600 text-white"
        >
          Currency: {currency}
        </button>
      </div>
    </header>
  );
}
