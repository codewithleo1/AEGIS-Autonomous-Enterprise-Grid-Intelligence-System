import { useState, useEffect, useCallback } from 'react'
import Header from './components/Header.jsx'
import TicketSidebar from './components/TicketSidebar.jsx'
import ChatPanel from './components/ChatPanel.jsx'
import ToolPanel from './components/ToolPanel.jsx'
import LoginPage from './components/LoginPage.jsx'
import { askAegis, fetchTickets, fetchHealth, deleteSession } from './api/helpdesk.js'

const SESSION_ID = 'session-' + Math.random().toString(36).slice(2, 9)

export default function App() {
  const [user, setUser]           = useState(null)
  const [tickets, setTickets]     = useState([])
  const [ticketsLoading, setTL]   = useState(false)
  const [health, setHealth]       = useState(false)
  const [toolLogs, setToolLogs]   = useState([])

  // Check for existing session on load
  useEffect(() => {
    const stored = localStorage.getItem('aegis_user')
    const token  = localStorage.getItem('aegis_token')
    if (stored && token) {
      setUser(JSON.parse(stored))
    }
  }, [])

  const stats = {
    total: tickets.length,
    open:  tickets.filter(t => t.status === 'Open').length,
    high:  tickets.filter(t => (t.priority === 'HIGH' || t.priority === 'CRITICAL') && t.status === 'Open').length,
  }

  const loadTickets = useCallback(async () => {
    setTL(true)
    try {
      const data = await fetchTickets()
      setTickets(data.tickets || [])
    } catch(e) { console.error(e) }
    finally { setTL(false) }
  }, [])

  useEffect(() => {
    if (!user) return
    fetchHealth().then(() => setHealth(true)).catch(() => setHealth(false))
    loadTickets()
    const interval = setInterval(loadTickets, 15000)
    return () => clearInterval(interval)
  }, [user, loadTickets])

  async function handleMessage(message) {
    return await askAegis({
      sessionId:  SESSION_ID,
      message:    message,
      employeeId: user?.id || 'UNKNOWN',
    })
  }

  function handleToolLog(tools) {
    setToolLogs(prev => [...prev, { timestamp: Date.now(), tools }])
  }

  function handleLogout() {
    localStorage.removeItem('aegis_token')
    localStorage.removeItem('aegis_user')
    setUser(null)
    setTickets([])
    setToolLogs([])
  }

  // Show login if not authenticated
  if (!user) {
    return <LoginPage onLogin={setUser} />
  }

  return (
    <div className="h-screen flex flex-col bg-slate-900 overflow-hidden">
      <Header health={health} stats={stats} user={user} onLogout={handleLogout} />
      <div className="flex flex-1 overflow-hidden">
        <TicketSidebar tickets={tickets} loading={ticketsLoading} onRefresh={loadTickets} />
        <ChatPanel
          onMessage={handleMessage}
          onToolLog={handleToolLog}
          onTicketsRefresh={loadTickets}
        />
        <ToolPanel logs={toolLogs} />
      </div>
    </div>
  )
}