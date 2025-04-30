export async function fetchFinancialData(currency = "LKR") {
  const res = await fetch(
    `http://localhost:5000/api/financials?currency=${currency}`
  );
  const json = await res.json();
  return json.data || [];
}
