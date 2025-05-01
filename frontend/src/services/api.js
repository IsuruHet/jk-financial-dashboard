export async function fetchFinancialData(currency = "LKR") {
  const res = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/api/financials?currency=${currency}`
  );
  const json = await res.json();
  return json.data || [];
}

export async function fetchShareholdersByYear(year) {
  const res = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/api/shareholders?year=${year}`
  );
  const json = await res.json();
  return json.shareholders || [];
}
