import { useState } from 'react'
import { RefreshCw, Filter } from 'lucide-react'

const PRIORITY_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 }

const PRIORITY_STYLES = {
  CRITICAL: 'text-red-300 bg-red-300/10 border-red-300/20',
  HIGH:     'text-red-400 bg-red-400/10 border-red-400/20',
  MEDIUM:   'text-amber-400 bg-amber-400/10 border-amber-400/20',
  LOW:      'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
}

const STATUS_STYLES = {
  'Open':        'text-blue-400 bg-blue-400/10 border-blue-400/20',
  'In Progress': 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  'Resolved':    'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
}

export default function TicketTable({ tickets, loading, onRefresh, onUpdateTicket }) {
  const [statusFilter, setStatusFilter]     = useState('')
  const [priorityFilter, setPriorityFilter] = useState('')
  const [updatingId, setUpdatingId]         = useState(null)
  const [resolutionNote, setResolutionNote] = useState('')
  const [pendingResolve, setPendingResolve] = useState(null)

  const filtered = tickets
    .filter(t => {
      if (statusFilter && t.status !== statusFilter) return false
      if (priorityFilter && t.priority !== priorityFilter) return false
      return true
    })
    .sort((a, b) => (PRIORITY_ORDER[a.priority] ?? 99) - (PRIORITY_ORDER[b.priority] ?? 99))

  async function handleStatusChange(ticketId, newStatus) {
    if (newStatus === 'Resolved') {
      setPendingResolve(ticketId)
      return
    }
    setUpdatingId(ticketId)
    await onUpdateTicket(ticketId, newStatus)
    setUpdatingId(null)
  }

  async function confirmResolve() {
    setUpdatingId(pendingResolve)
    await onUpdateTicket(pendingResolve, 'Resolved', resolutionNote)
    setPendingResolve(null)
    setResolutionNote('')
    setUpdatingId(null)
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden p-6">

      {/* Resolution Note Modal */}
      {pendingResolve && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
          <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 w-full max-w-md">
            <h2 className="text-sm font-semibold text-white mb-1">Resolve Ticket</h2>
            <p className="text-xs text-slate-400 mb-4">
              Add a resolution note before closing <span className="text-emerald-400 font-mono">{pendingResolve}</span>
            </p>
            <textarea
              value={resolutionNote}
              onChange={e => setResolutionNote(e.target.value)}
              placeholder="Describe what fixed the issue..."
              rows={3}
              className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-sm text-white placeholder-slate-500 resize-none focus:outline-none focus:border-emerald-500 mb-4"
            />
            <div className="flex gap-3">
              <button
                onClick={() => { setPendingResolve(null); setResolutionNote('') }}
                className="flex-1 py-2 rounded-lg border border-slate-600 text-sm text-slate-400 hover:bg-slate-700 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmResolve}
                disabled={!resolutionNote.trim()}
                className="flex-1 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:opacity-40 text-sm text-white font-semibold transition-colors"
              >
                Mark Resolved
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Toolbar */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter size={14} className="text-slate-500" />
          <select
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
          >
            <option value="">All Status</option>
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Resolved">Resolved</option>
          </select>
          <select
            value={priorityFilter}
            onChange={e => setPriorityFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
          >
            <option value="">All Priority</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500">{filtered.length} tickets</span>
          <button onClick={onRefresh} className="p-1.5 rounded-lg hover:bg-slate-800 transition-colors">
            <RefreshCw size={13} className={`text-slate-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="flex-1 overflow-auto rounded-xl border border-slate-800">
        <table className="w-full text-sm">
          <thead className="bg-slate-800/60 sticky top-0">
            <tr>
              {['Ticket ID', 'Title', 'Employee', 'Category', 'Priority', 'Status', 'Assigned To', 'Created', 'Action'].map(h => (
                <th key={h} className="text-left px-4 py-3 text-xs font-medium text-slate-400">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={9} className="text-center py-8 text-slate-500 text-xs">Loading tickets...</td></tr>
            )}
            {!loading && filtered.length === 0 && (
              <tr><td colSpan={9} className="text-center py-8 text-slate-500 text-xs">No tickets found</td></tr>
            )}
            {!loading && filtered.map((ticket, i) => (
              <tr key={ticket.ticket_id} className={`border-t border-slate-800/60 hover:bg-slate-800/30 transition-colors ${i % 2 === 0 ? '' : 'bg-slate-800/10'}`}>
                <td className="px-4 py-3 font-mono text-xs text-emerald-400">{ticket.ticket_id}</td>
                <td className="px-4 py-3 text-slate-200 max-w-[200px] truncate">{ticket.title}</td>
                <td className="px-4 py-3 text-xs text-slate-400">{ticket.employee_id}</td>
                <td className="px-4 py-3 text-xs text-slate-400">{ticket.category}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs px-2 py-0.5 rounded border ${PRIORITY_STYLES[ticket.priority] || ''}`}>
                    {ticket.priority}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className={`text-xs px-2 py-0.5 rounded border ${STATUS_STYLES[ticket.status] || ''}`}>
                    {ticket.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-xs text-slate-400">{ticket.assigned_agent_name}</td>
                <td className="px-4 py-3 text-xs text-slate-500">{ticket.created}</td>
                <td className="px-4 py-3">
                  <select
                    value={ticket.status}
                    disabled={updatingId === ticket.ticket_id}
                    onChange={e => handleStatusChange(ticket.ticket_id, e.target.value)}
                    className="bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-300 focus:outline-none focus:border-emerald-500 disabled:opacity-50"
                  >
                    <option value="Open">Open</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Resolved">Resolved</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}