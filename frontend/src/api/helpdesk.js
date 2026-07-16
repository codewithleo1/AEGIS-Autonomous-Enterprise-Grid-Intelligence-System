const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_KEY  = import.meta.env.VITE_API_KEY  || 'aegis-secret-123'

const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY,
}

export async function askAegis({ sessionId, message, employeeId }) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      session_id:  sessionId,
      message:     message,
      employee_id: employeeId || 'UNKNOWN',
    }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function fetchTickets(filters = {}) {
  const params = new URLSearchParams(filters).toString()
  const res = await fetch(`${BASE_URL}/tickets${params ? '?' + params : ''}`, { headers })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function deleteSession(sessionId) {
  const res = await fetch(`${BASE_URL}/session/${sessionId}`, {
    method: 'DELETE',
    headers,
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}