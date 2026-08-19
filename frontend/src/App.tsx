import { useEffect, useState } from "react";
import { getExpenses } from "./api";

function App() {
  const [expenses, setExpenses] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getExpenses(1)
      .then((data) => {
        setExpenses(data);
      })
      .catch(() => {
        setError("Could not load expenses.");
      });
  }, []);

  return (
    <div>
      <h1>Expense Tracker</h1>

      {error && <p>{error}</p>}

      <h2>Expenses</h2>

      {expenses.map((expense) => (
        <div key={expense.id}>
          <p>
            {expense.merchant} - £{expense.amount} - {expense.category}
          </p>
        </div>
      ))}
    </div>
  );
}

export default App;