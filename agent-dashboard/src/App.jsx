import { useState, useEffect, useCallback } from 'react'
import AgentLogin from './components/AgentLogin.jsx'
import AgentHeader from './components/AgentHeader.jsx'
import TicketTable from './components/TicketTable.jsx'
import { fetchAllTickets } from './api/agent.js'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_KEY  = import.meta.env.VITE_API_KEY  || 'aegis-secret-123'

export default function App() {
  const [agent, setAgent]         = useState(null)
  const [tickets, setTickets]     = useState([])
  const [loading, setLoading]     = useState(false)
  const [health, setHealth]       = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('aegis_agent_user')
    const token  = localStorage.getItem('aegis_agent_token')
    if (stored && token) setAgent(JSON.parse(stored))
  }, [])

  const loadTickets = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchAllTickets()
      setTickets(data.tickets || [])
    } catch(e) { console.error(e) }
    finally { setLoading(false) }
  }, [])

  useEffect(() => {
    if (!agent) return
    fetch(`${BASE_URL}/health`).then(() => setHealth(true)).catch(() => setHealth(false))
    loadTickets()
    const interval = setInterval(loadTickets, 15000)
    return () => clearInterval(interval)
  }, [agent, loadTickets])

  async function handleUpdateTicket(ticketId, status) {
    try {
      await fetch(`${BASE_URL}/tickets/${ticketId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({ status }),
      })
      await loadTickets()
    } catch(e) { console.error(e) }
  }

  function handleLogout() {
    localStorage.removeItem('aegis_agent_token')
    localStorage.removeItem('aegis_agent_user')
    setAgent(null)
    setTickets([])
  }

  const stats = {
    total:      tickets.length,
    open:       tickets.filter(t => t.status === 'Open').length,
    inProgress: tickets.filter(t => t.status === 'In Progress').length,
    resolved:   tickets.filter(t => t.status === 'Resolved').length,
  }

  if (!agent) return <AgentLogin onLogin={setAgent} />

  return (
    <div className="h-screen flex flex-col bg-slate-900 overflow-hidden">
      <AgentHeader agent={agent} stats={stats} health={health} onLogout={handleLogout} />
      <TicketTable
        tickets={tickets}
        loading={loading}
        onRefresh={loadTickets}
        onUpdateTicket={handleUpdateTicket}
      />
    </div>
  )
}