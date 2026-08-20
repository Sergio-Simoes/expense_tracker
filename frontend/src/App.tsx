import { useEffect, useState } from "react";
import { askAI, getExpenses } from "./api";
import "./App.css";

type Expense = {
  id: number;
  merchant: string;
  description: string;
  amount: string;
  category: string;
  expense_date: string;
  notes: string | null;
  user_id: number;
};

function App() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [message, setMessage] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const userId = 1;

  useEffect(() => {
    getExpenses(userId)
      .then((data) => {
        setExpenses(data);
      })
      .catch(() => {
        setError("Could not load expenses.");
      });
  }, []);

  async function handleAskAI() {
    if (!message.trim()) return;

    setLoading(true);
    setError("");

    try {
      const data = await askAI(message, userId);

      setAiResponse(data.response);
      setMessage("");

      // Refresh expenses in case the AI added/updated/deleted one
      const updatedExpenses = await getExpenses(userId);
      setExpenses(updatedExpenses);
    } catch {
      setError("Could not communicate with the AI.");
    } finally {
      setLoading(false);
    }
  }

  const totalExpenses = expenses.reduce(
    (total, expense) => total + Number(expense.amount),
    0
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div>
          <h1>Expense Tracker</h1>
          <p>Manage your expenses with your AI assistant.</p>
        </div>

        <div className="user">
          <div className="avatar">S</div>
          <span>Sergio</span>
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      {/* Summary */}
      <section className="summary">
        <div className="summary-card">
          <span>Total expenses</span>
          <strong>£{totalExpenses.toFixed(2)}</strong>
          <small>Across {expenses.length} transactions</small>
        </div>
      </section>

      {/* Expenses */}
      <section className="expenses-section">
        <div className="section-header">
          <div>
            <h2>Recent Expenses</h2>
            <p>Your latest transactions</p>
          </div>
        </div>

        <div className="expense-list">
          {expenses.map((expense) => (
            <div className="expense-card" key={expense.id}>
              <div className="expense-icon">
                {getCategoryIcon(expense.category)}
              </div>

              <div className="expense-info">
                <strong>{expense.merchant}</strong>
                <span>{expense.description}</span>
              </div>

              <div className="expense-category">
                {expense.category}
              </div>

              <div className="expense-date">
                {new Date(expense.expense_date).toLocaleDateString("en-GB")}
              </div>

              <div className="expense-amount">
                -£{Number(expense.amount).toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* AI Assistant */}
      <section className="ai-section">
        <div className="ai-header">
          <div className="ai-icon">✨</div>

          <div>
            <h2>AI Assistant</h2>
            <p>Ask me anything about your expenses.</p>
          </div>
        </div>

        {aiResponse && (
          <div className="ai-response">
            <strong>Assistant</strong>
            <p>{aiResponse}</p>
          </div>
        )}

        <div className="ai-input">
          <input
            type="text"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleAskAI();
              }
            }}
            placeholder="e.g. Add £40 for cinema"
          />

          <button onClick={handleAskAI} disabled={loading}>
            {loading ? "..." : "Send"}
          </button>
        </div>
      </section>
    </div>
  );
}

function getCategoryIcon(category: string) {
  switch (category) {
    case "Groceries":
      return "🛒";
    case "Fuel":
      return "⛽";
    case "Restaurants":
      return "🍽️";
    case "Pets":
      return "🐾";
    case "Bills":
      return "📄";
    case "Shopping":
      return "🛍️";
    case "Healthcare":
      return "💊";
    case "Entertainment":
      return "🎬";
    default:
      return "💰";
  }
}

export default App;