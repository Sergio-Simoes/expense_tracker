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