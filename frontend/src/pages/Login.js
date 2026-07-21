// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUsers } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const [loading, setLoading]   = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      const { data: users } = await getUsers();
      const match = users.find(u => u.email === email);
      if (!match) { setError('No account found with that email.'); setLoading(false); return; }
      if (match.status !== 'ACTIVE') { setError('This account is not active.'); setLoading(false); return; }
      // In a real app: validate password on backend; for now we accept any non-empty password
      if (!password) { setError('Please enter your password.'); setLoading(false); return; }
      login(match);
      navigate('/dashboard');
    } catch {
      setError('Could not connect to the server. Make sure the backend is running on port 8000.');
    }
    setLoading(false);
  };

  const demo = async (role) => {
    setLoading(true); setError('');
    try {
      const { data: users } = await getUsers(role);
      if (users.length > 0) { login(users[0]); navigate('/dashboard'); return; }
      setError(`No ${role} accounts found. Register one first.`);
    } catch { setError('Backend not reachable.'); }
    setLoading(false);
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          <div className="logo-icon" style={{ width: 40, height: 40, fontSize: 20 }}>🎓</div>
          <h1>Research Platform</h1>
        </div>
        <h2 className="login-title">Welcome back</h2>
        <p className="login-sub">Sign in to your account to continue</p>

        {error && <div className="alert alert-error">⚠ {error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email address</label>
            <input className="form-input" type="email" placeholder="you@university.ac.za"
              value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" placeholder="••••••••"
              value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: 8 }}
            type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <div style={{ marginTop: 24, paddingTop: 20, borderTop: '1px solid var(--border)' }}>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 10 }}>Quick demo login</p>
          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={() => demo('supervisor')}>Supervisor</button>
            <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={() => demo('student')}>Student</button>
            <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={() => demo('admin')}>Admin</button>
          </div>
        </div>
      </div>
    </div>
  );
}
