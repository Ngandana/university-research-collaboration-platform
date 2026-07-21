// src/pages/Users.js
import React, { useEffect, useState } from 'react';
import { getUsers, createUser, suspendUser, reactivateUser, deleteUser } from '../services/api';
import { useAuth } from '../context/AuthContext';

const ROLE_BADGE   = { STUDENT: 'badge-green', SUPERVISOR: 'badge-blue', RESEARCHER: 'badge-purple', ADMIN: 'badge-yellow' };
const STATUS_BADGE = { ACTIVE: 'badge-green', SUSPENDED: 'badge-yellow', REGISTERED: 'badge-blue', DEACTIVATED: 'badge-gray' };

export default function Users() {
  const { currentUser } = useAuth();
  const [users, setUsers]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch]   = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [showModal, setShowModal]   = useState(false);
  const [form, setForm] = useState({ user_id: '', name: '', email: '', password: '', role: 'student' });
  const [error, setError]   = useState('');
  const [saving, setSaving] = useState(false);

  const isAdmin = currentUser?.role === 'ADMIN';

  const load = () => {
    setLoading(true);
    getUsers(roleFilter || undefined)
      .then(r => setUsers(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };
  useEffect(load, [roleFilter]);

  const filtered = users.filter(u =>
    u.name.toLowerCase().includes(search.toLowerCase()) ||
    u.email.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = async (e) => {
    e.preventDefault(); setSaving(true); setError('');
    try {
      await createUser(form);
      setShowModal(false); setForm({ user_id: '', name: '', email: '', password: '', role: 'student' }); load();
    } catch (err) { setError(err.response?.data?.detail || 'Failed to create user.'); }
    setSaving(false);
  };

  const handleSuspend = async (id) => {
    try { await suspendUser(id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error suspending user.'); }
  };

  const handleReactivate = async (id) => {
    try { await reactivateUser(id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error reactivating user.'); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Deactivate this user?')) return;
    try { await deleteUser(id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error deactivating user.'); }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Users</h1>
          <p className="page-subtitle">{users.length} registered account{users.length !== 1 ? 's' : ''}</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
            Add User
          </button>
        )}
      </div>

      <div className="filter-bar">
        <div className="search-input-wrap" style={{ flex: 2 }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input className="form-input search-input" placeholder="Search by name or email..."
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <select className="form-input" style={{ maxWidth: 160 }} value={roleFilter} onChange={e => setRoleFilter(e.target.value)}>
          <option value="">All roles</option>
          {['student','supervisor','researcher','admin'].map(r =>
            <option key={r} value={r}>{r.charAt(0).toUpperCase() + r.slice(1)}</option>
          )}
        </select>
      </div>

      {loading
        ? <div className="loading-wrap"><div className="spinner" /></div>
        : filtered.length === 0
          ? <div className="empty-state card"><div className="empty-state-icon">👥</div><h3>No users found</h3><p>Register a new user to get started.</p></div>
          : (
            <div className="card" style={{ padding: 0 }}>
              <div className="table-wrap">
                <table>
                  <thead><tr>
                    <th>Name</th><th>Email</th><th>Role</th>
                    <th>Status</th><th>Joined</th>{isAdmin && <th>Actions</th>}
                  </tr></thead>
                  <tbody>
                    {filtered.map(u => (
                      <tr key={u.user_id}>
                        <td>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                            <div className="avatar" style={{ width: 28, height: 28, fontSize: 11 }}>
                              {u.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase()}
                            </div>
                            <span style={{ fontWeight: 500 }}>{u.name}</span>
                          </div>
                        </td>
                        <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>{u.email}</td>
                        <td><span className={`badge ${ROLE_BADGE[u.role] || 'badge-gray'}`}>{u.role}</span></td>
                        <td><span className={`badge ${STATUS_BADGE[u.status] || 'badge-gray'}`}>{u.status}</span></td>
                        <td style={{ fontSize: 13, color: 'var(--text-muted)' }}>{u.created_date}</td>
                        {isAdmin && (
                          <td>
                            <div style={{ display: 'flex', gap: 6 }}>
                              {u.status === 'ACTIVE' && u.user_id !== currentUser?.user_id && (
                                <button className="btn btn-ghost btn-sm" onClick={() => handleSuspend(u.user_id)}>Suspend</button>
                              )}
                              {u.status === 'SUSPENDED' && (
                                <button className="btn btn-ghost btn-sm" onClick={() => handleReactivate(u.user_id)}>Reactivate</button>
                              )}
                              {u.user_id !== currentUser?.user_id && (
                                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(u.user_id)}>Deactivate</button>
                              )}
                            </div>
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )
      }

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">Register New User</h3>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">User ID</label>
                <input className="form-input" placeholder="e.g. u-001" required
                  value={form.user_id} onChange={e => setForm({ ...form, user_id: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input className="form-input" placeholder="Full name" required
                  value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input className="form-input" type="email" placeholder="email@university.ac.za" required
                  value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Password</label>
                <input className="form-input" type="password" placeholder="Min 6 characters" required minLength={6}
                  value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Role</label>
                <select className="form-input" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}>
                  {['student','supervisor','researcher','admin'].map(r =>
                    <option key={r} value={r}>{r.charAt(0).toUpperCase() + r.slice(1)}</option>
                  )}
                </select>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Registering...' : 'Register User'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
