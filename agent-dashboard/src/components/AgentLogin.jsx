import { useState } from 'react'
import { Shield, Loader2 } from 'lucide-react'
import { agentLogin } from '../api/agent'

export default function AgentLogin({ onLogin }) {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)

  async function handleLogin() {
    if (!email || !password) { setError('Please enter email and password.'); return }
    setLoading(true)
    setError(null)
    try {
      const data = await agentLogin(email, password)
      if (data.role !== 'agent') {
        setError('This dashboard is for IT agents only. Employees please use the Employee Portal.')
        return
      }
      localStorage.setItem('aegis_agent_token', data.access_token)
      localStorage.setItem('aegis_agent_user', JSON.stringify({ id: data.id, name: data.name, role: data.role }))
      onLogin(data)
    } catch {
      setError('Invalid email or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex items-center justify-center bg-slate-900">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-emerald-600 flex items-center justify-center mb-3">
            <Shield size={24} className="text-white" />
          </div>
          <h1 className="text-xl font-bold text-white">AEGIS Agent Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">IT Support Team Portal</p>
        </div>

        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">Agent Email</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLogin()}
                placeholder="kiran.pillai@techcorp.com"
                className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">Password</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLogin()}
                placeholder="••••••••"
                className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>
            {error && (
              <div className="text-red-400 text-xs bg-red-400/10 border border-red-400/20 rounded-lg px-3 py-2">
                {error}
              </div>
            )}
            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg text-sm transition-colors flex items-center justify-center gap-2"
            >
              {loading ? <><Loader2 size={15} className="animate-spin" /> Signing in...</> : 'Sign In'}
            </button>
          </div>
        </div>

        <div className="mt-4 p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
          <p className="text-xs text-slate-500 font-medium mb-1">Demo credentials</p>
          <p className="text-xs text-slate-400">Email: <span className="text-emerald-400">kiran.pillai@techcorp.com</span></p>
          <p className="text-xs text-slate-400">Password: <span className="text-emerald-400">aegis1234</span></p>
        </div>
      </div>
    </div>
  )
}