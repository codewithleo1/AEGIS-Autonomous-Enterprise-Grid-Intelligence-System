import { useState } from 'react'
import { Building2, Loader2 } from 'lucide-react'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function LoginPage({ onLogin }) {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)

  async function handleLogin() {
    if (!email || !password) {
      setError('Please enter your email and password.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Invalid email or password.')
        return
      }

      if (data.role !== 'employee') {
        setError('This portal is for employees only. Agents please use the Agent Dashboard.')
        return
      }

      // Store token
      localStorage.setItem('aegis_token', data.access_token)
      localStorage.setItem('aegis_user', JSON.stringify({
        id: data.id,
        name: data.name,
        role: data.role,
      }))

      onLogin(data)
    } catch {
      setError('Connection error. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex items-center justify-center bg-slate-900">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-indigo-600 flex items-center justify-center mb-3">
            <Building2 size={24} className="text-white" />
          </div>
          <h1 className="text-xl font-bold text-white">AEGIS</h1>
          <p className="text-sm text-slate-500 mt-1">Employee Helpdesk Portal</p>
        </div>

        {/* Form */}
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">
                Work Email
              </label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLogin()}
                placeholder="raj.sharma@techcorp.com"
                className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-400 mb-1.5 block">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLogin()}
                placeholder="••••••••"
                className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
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
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-lg text-sm transition-colors flex items-center justify-center gap-2"
            >
              {loading
                ? <><Loader2 size={15} className="animate-spin" /> Signing in...</>
                : 'Sign In'
              }
            </button>
          </div>
        </div>

        {/* Demo credentials */}
        <div className="mt-4 p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
          <p className="text-xs text-slate-500 font-medium mb-1">Demo credentials</p>
          <p className="text-xs text-slate-400">Email: <span className="text-indigo-400">raj.sharma@techcorp.com</span></p>
          <p className="text-xs text-slate-400">Password: <span className="text-indigo-400">aegis1234</span></p>
        </div>
      </div>
    </div>
  )
}