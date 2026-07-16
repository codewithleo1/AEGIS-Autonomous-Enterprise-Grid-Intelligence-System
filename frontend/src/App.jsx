import { useState, useEffect, useCallback } from 'react'
import Header from './components/Header.jsx'
import TicketSidebar from './components/TicketSidebar.jsx'
import ChatPanel from './components/ChatPanel.jsx'
import ToolPanel from './components/ToolPanel.jsx'
import { askAegis, fetchTickets, fetchHealth, deleteSession } from './api/helpdesk.js'

const SESSION_ID  = 'session-' + Math.random().toString(36).slice(2, 9)
let   EMPLOYEE_ID = 'UNKNOWN'

export default function App() {
  const [tickets, setTickets]     = useState([])
  const [ticketsLoading, setTL]   = useState(false)
  const [health, setHealth]       = useState(false)
  const [toolLogs, setToolLogs]   = useState([])

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
    fetchHealth().then(() => setHealth(true)).catch(() => setHealth(false))
    loadTickets()
    const interval = setInterval(loadTickets, 15000)
    return () => clearInterval(interval)
  }, [loadTickets])

  async function handleMessage(message) {
    // Extract employee ID from message if present
    const match = message.match(/EMP\d+/i)
    if (match) EMPLOYEE_ID = match[0].toUpperCase()

    return await askAegis({
      sessionId:  SESSION_ID,
      message:    message,
      employeeId: EMPLOYEE_ID,
    })
  }

  function handleToolLog(tools) {
    setToolLogs(prev => [...prev, { timestamp: Date.now(), tools }])
  }

  return (
    <div className="h-screen flex flex-col bg-slate-900 overflow-hidden">
      <Header health={health} stats={stats} />
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