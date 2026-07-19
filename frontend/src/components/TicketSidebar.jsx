import { Ticket, RefreshCw, Clock } from 'lucide-react'

const PRIORITY_STYLES = {
  HIGH:     { color: 'text-red-400',     bg: 'bg-red-400/10',     border: 'border-red-400/20',     dot: 'bg-red-400'     },
  CRITICAL: { color: 'text-red-300',     bg: 'bg-red-300/10',     border: 'border-red-300/20',     dot: 'bg-red-300'     },
  MEDIUM:   { color: 'text-amber-400',   bg: 'bg-amber-400/10',   border: 'border-amber-400/20',   dot: 'bg-amber-400'   },
  LOW:      { color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20', dot: 'bg-emerald-400' },
}

const STATUS_STYLES = {
  'Open':        'text-blue-400 bg-blue-400/10 border-blue-400/20',
  'In Progress': 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  'Resolved':    'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
}

function PriorityBadge({ priority }) {
  const cfg = PRIORITY_STYLES[priority] || PRIORITY_STYLES.MEDIUM
  return (
    <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-xs font-medium ${cfg.bg} ${cfg.color} border ${cfg.border}`}>
      <span className={`w-1 h-1 rounded-full ${cfg.dot}`} />
      {priority}
    </span>
  )
}

export default function TicketSidebar({ tickets, loading, onRefresh }) {
  const open       = tickets.filter(t => t.status === 'Open').length
  const inProgress = tickets.filter(t => t.status === 'In Progress').length
  const resolved   = tickets.filter(t => t.status === 'Resolved').length

  return (
    <aside className="w-64 flex flex-col border-r border-slate-800 bg-slate-950/60 flex-shrink-0">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Ticket size={14} className="text-indigo-400" />
          <span className="text-sm font-semibold text-white">My Tickets</span>
        </div>
        <button onClick={onRefresh} className="p-1 rounded hover:bg-slate-800 transition-colors">
          <RefreshCw size={12} className={`text-slate-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-px m-3 rounded-lg overflow-hidden border border-slate-800">
        {[
          { label: 'Open',     value: open,       color: 'text-blue-400'    },
          { label: 'Progress', value: inProgress,  color: 'text-amber-400'   },
          { label: 'Resolved', value: resolved,    color: 'text-emerald-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-800/60 px-2 py-2 text-center">
            <div className={`text-lg font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-slate-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Ticket list — all statuses */}
      <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-2">
        {loading && <div className="text-xs text-slate-500 text-center py-4">Loading...</div>}

        {!loading && tickets.length === 0 && (
          <div className="flex flex-col items-center gap-2 py-8 text-slate-600">
            <Ticket size={24} />
            <span className="text-xs">No tickets yet</span>
          </div>
        )}

        {!loading && tickets.map(ticket => (
          <div key={ticket.ticket_id} className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-slate-600 transition-colors">
            <div className="flex items-start justify-between gap-1 mb-1.5">
              <span className="text-xs font-mono text-indigo-400 font-medium">{ticket.ticket_id}</span>
              <PriorityBadge priority={ticket.priority} />
            </div>
            <p className="text-xs text-slate-300 leading-snug line-clamp-2 mb-1.5">{ticket.title}</p>
            <div className="flex items-center justify-between">
              <span className={`text-xs px-1.5 py-0.5 rounded border ${STATUS_STYLES[ticket.status] || ''}`}>
                {ticket.status}
              </span>
              <div className="flex items-center gap-1 text-slate-500">
                <Clock size={10} />
                <span className="text-xs">{ticket.created}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </aside>
  )
}