const API = "http://127.0.0.1:5000";

async function addExpense() {
  const name = document.getElementById("name").value;
  const amount = parseFloat(document.getElementById("amount").value);
  const category = document.getElementById("category").value;
  const date = document.getElementById("date").value;

  if (!name || !amount || !category || !date) {
    alert("⚠️ Please fill all fields!");
    return;
  }

  const expense = { name, amount, category, date };

  await fetch(`${API}/add_expense`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expense)
  });

  document.getElementById("name").value = "";
  document.getElementById("amount").value = "";
  document.getElementById("category").value = "";
  document.getElementById("date").value = "";

  loadExpenses();
}

async function loadExpenses() {
  const res = await fetch(`${API}/get_expenses`);
  const expenses = await res.json();

  const list = document.getElementById("expense-list");
  list.innerHTML = "";
  expenses.forEach((exp, i) => {
    list.innerHTML += `<li>${exp.date} | ${exp.name} | ${exp.category} | Rs. ${exp.amount}</li>`;
  });

  const totalRes = await fetch(`${API}/total`);
  const totalData = await totalRes.json();
  document.getElementById("total").innerText = `Total: Rs. ${totalData.total}`;
}

window.onload = loadExpenses;
