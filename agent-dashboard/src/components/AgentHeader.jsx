import { Shield, Wifi, WifiOff, LogOut } from 'lucide-react'

export default function AgentHeader({ agent, stats, health, onLogout }) {
  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-slate-800 bg-slate-950/80 flex-shrink-0">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center">
          <Shield size={16} className="text-white" />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-white leading-none">AEGIS Agent Dashboard</h1>
          <p className="text-xs text-slate-500 mt-0.5">IT Support Queue</p>
        </div>
      </div>

      <div className="flex items-center gap-6 text-xs text-slate-400">
        <span><span className="text-white font-semibold">{stats.total}</span> total</span>
        <span><span className="text-blue-400 font-semibold">{stats.open}</span> open</span>
        <span><span className="text-amber-400 font-semibold">{stats.inProgress}</span> in progress</span>
        <span><span className="text-emerald-400 font-semibold">{stats.resolved}</span> resolved</span>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          {health
            ? <><Wifi size={12} className="text-emerald-400" /><span className="text-xs text-emerald-400">Live</span></>
            : <><WifiOff size={12} className="text-red-400" /><span className="text-xs text-red-400">Offline</span></>
          }
        </div>
        {agent && (
          <div className="flex items-center gap-2 pl-3 border-l border-slate-700">
            <div className="w-6 h-6 rounded-full bg-emerald-600/20 border border-emerald-600/30 flex items-center justify-center">
              <span className="text-xs text-emerald-400 font-bold">{agent.name[0]}</span>
            </div>
            <span className="text-xs text-slate-300">{agent.name}</span>
            <button onClick={onLogout} className="p-1.5 rounded-lg hover:bg-slate-800 transition-colors">
              <LogOut size={13} className="text-slate-500 hover:text-slate-300" />
            </button>
          </div>
        )}
      </div>
    </header>
  )
}