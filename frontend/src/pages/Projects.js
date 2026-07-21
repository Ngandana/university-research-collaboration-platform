// src/pages/Projects.js
import React, { useEffect, useState } from 'react';
import { getProjects, createProject, completeProject, deleteProject, addMember } from '../services/api';
import { useAuth } from '../context/AuthContext';

const STATUS_BADGE = {
  ACTIVE: 'badge-green', CREATED: 'badge-blue', COMPLETED: 'badge-gray',
  CANCELLED: 'badge-red', ARCHIVED: 'badge-gray',
};

export default function Projects() {
  const { currentUser } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [search, setSearch]     = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm]         = useState({ project_id: '', title: '', description: '' });
  const [error, setError]       = useState('');
  const [saving, setSaving]     = useState(false);

  const load = () => {
    setLoading(true);
    getProjects().then(r => setProjects(r.data)).catch(() => {}).finally(() => setLoading(false));
  };
  useEffect(load, []);

  const filtered = projects.filter(p =>
    p.title.toLowerCase().includes(search.toLowerCase()) ||
    p.owner_name.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = async (e) => {
    e.preventDefault(); setSaving(true); setError('');
    try {
      await createProject({ ...form, owner_id: currentUser.user_id });
      setShowModal(false); setForm({ project_id: '', title: '', description: '' }); load();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create project.');
    }
    setSaving(false);
  };

  const handleComplete = async (id) => {
    if (!window.confirm('Mark this project as completed?')) return;
    try { await completeProject(id, currentUser.user_id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error completing project.'); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this project? This cannot be undone.')) return;
    try { await deleteProject(id, currentUser.user_id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error deleting project.'); }
  };

  const canCreate = ['SUPERVISOR', 'RESEARCHER'].includes(currentUser?.role);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Research Projects</h1>
          <p className="page-subtitle">{projects.length} project{projects.length !== 1 ? 's' : ''} on the platform</p>
        </div>
        {canCreate && (
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
            New Project
          </button>
        )}
      </div>

      <div className="filter-bar">
        <div className="search-input-wrap">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input className="form-input search-input" placeholder="Search projects..."
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
      </div>

      {loading
        ? <div className="loading-wrap"><div className="spinner" /></div>
        : filtered.length === 0
          ? <div className="empty-state card"><div className="empty-state-icon">📁</div><h3>No projects found</h3><p>Create a new project to get started.</p></div>
          : (
            <div className="card" style={{ padding: 0 }}>
              <div className="table-wrap">
                <table>
                  <thead><tr>
                    <th>Title</th><th>Owner</th><th>Members</th>
                    <th>Status</th><th>Created</th><th>Actions</th>
                  </tr></thead>
                  <tbody>
                    {filtered.map(p => (
                      <tr key={p.project_id}>
                        <td>
                          <div style={{ fontWeight: 500 }}>{p.title}</div>
                          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{p.description?.slice(0, 60)}{p.description?.length > 60 ? '…' : ''}</div>
                        </td>
                        <td style={{ color: 'var(--text-muted)' }}>{p.owner_name}</td>
                        <td>
                          <span className="badge badge-blue">{p.member_count} member{p.member_count !== 1 ? 's' : ''}</span>
                        </td>
                        <td><span className={`badge ${STATUS_BADGE[p.status] || 'badge-gray'}`}>{p.status}</span></td>
                        <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>{p.created_date}</td>
                        <td>
                          <div style={{ display: 'flex', gap: 6 }}>
                            {p.status === 'ACTIVE' && p.owner_id === currentUser?.user_id && (
                              <button className="btn btn-ghost btn-sm" onClick={() => handleComplete(p.project_id)}>Complete</button>
                            )}
                            {['COMPLETED','CANCELLED'].includes(p.status) && p.owner_id === currentUser?.user_id && (
                              <button className="btn btn-danger btn-sm" onClick={() => handleDelete(p.project_id)}>Delete</button>
                            )}
                          </div>
                        </td>
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
            <h3 className="modal-title">Create New Project</h3>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Project ID</label>
                <input className="form-input" placeholder="e.g. proj-001" required
                  value={form.project_id} onChange={e => setForm({ ...form, project_id: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Title</label>
                <input className="form-input" placeholder="Research project title" required
                  value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea className="form-input" rows={3} placeholder="Brief description..."
                  value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Creating...' : 'Create Project'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
