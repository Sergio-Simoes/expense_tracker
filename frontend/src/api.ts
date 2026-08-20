export async function getExpenses(userId: number) {
  const params = new URLSearchParams({
    user_id: userId.toString(),
  });

  const response = await fetch(
    `http://127.0.0.1:8000/expenses/?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch expenses");
  }

  return response.json();
}

export async function askAI(message: string, userId: number) {
  const response = await fetch("http://127.0.0.1:8000/ai/agent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      user_id: userId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to communicate with AI");
  }

  return response.json();
}