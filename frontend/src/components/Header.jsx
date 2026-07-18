import { Building2, Wifi, WifiOff, LogOut } from 'lucide-react'

export default function Header({ health, stats, user, onLogout }) {
  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm flex-shrink-0">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
          <Building2 size={16} className="text-white" />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-white leading-none">AEGIS</h1>
          <p className="text-xs text-slate-500 mt-0.5">Autonomous Enterprise Grid Intelligence System</p>
        </div>
      </div>

      <div className="hidden md:flex items-center gap-2">
        {['Groq LLaMA 3.3', 'FastAPI', 'PostgreSQL', 'Redis'].map(b => (
          <span key={b} className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 font-medium">
            {b}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-4 text-xs text-slate-400">
          <span><span className="text-white font-semibold">{stats.total}</span> total</span>
          <span><span className="text-amber-400 font-semibold">{stats.open}</span> open</span>
          <span><span className="text-red-400 font-semibold">{stats.high}</span> high</span>
        </div>

        <div className="flex items-center gap-1.5">
          {health
            ? <><Wifi size={12} className="text-emerald-400" /><span className="text-xs text-emerald-400 font-medium">Live</span></>
            : <><WifiOff size={12} className="text-red-400" /><span className="text-xs text-red-400 font-medium">Offline</span></>
          }
        </div>

        {user && (
          <div className="flex items-center gap-2 pl-3 border-l border-slate-700">
            <span className="text-xs text-slate-300">{user.name}</span>
            <button
              onClick={onLogout}
              className="p-1.5 rounded-lg hover:bg-slate-800 transition-colors"
              title="Sign out"
            >
              <LogOut size={13} className="text-slate-500 hover:text-slate-300" />
            </button>
          </div>
        )}
      </div>
    </header>
  )
}