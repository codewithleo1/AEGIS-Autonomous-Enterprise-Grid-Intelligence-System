const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_KEY  = import.meta.env.VITE_API_KEY  || 'aegis-secret-123'

function getAuthHeaders() {
  const token = localStorage.getItem('aegis_agent_token')
  return {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  }
}

export async function agentLogin(email, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) throw new Error('Invalid credentials')
  return res.json()
}

export async function fetchAllTickets(filters = {}) {
  const params = new URLSearchParams(filters).toString()
  const res = await fetch(`${BASE_URL}/tickets${params ? '?' + params : ''}`, {
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Failed to fetch tickets')
  return res.json()
}

export async function updateTicket(ticketId, status, note = '') {
  const res = await fetch(`${BASE_URL}/tickets/${ticketId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ status, note }),
  })
  if (!res.ok) throw new Error('Failed to update ticket')
  return res.json()
}