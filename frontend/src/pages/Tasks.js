// src/pages/Tasks.js
import React, { useEffect, useState } from 'react';
import { getTasks, createTask, assignTask, startTask, completeTask, deleteTask, getProjects, getUsers } from '../services/api';
import { useAuth } from '../context/AuthContext';

const STATUS_BADGE = {
  CREATED: 'badge-blue', ASSIGNED: 'badge-purple',
  IN_PROGRESS: 'badge-yellow', COMPLETED: 'badge-green',
  OVERDUE: 'badge-red',
};

export default function Tasks() {
  const { currentUser } = useAuth();
  const [tasks, setTasks]       = useState([]);
  const [projects, setProjects] = useState([]);
  const [users, setUsers]       = useState([]);
  const [loading, setLoading]   = useState(true);
  const [filter, setFilter]     = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm]         = useState({ task_id: '', title: '', description: '', deadline: '', project_id: '' });
  const [error, setError]       = useState('');
  const [saving, setSaving]     = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([getTasks(), getProjects(), getUsers()])
      .then(([t, p, u]) => { setTasks(t.data); setProjects(p.data); setUsers(u.data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const filtered = tasks.filter(t => {
    const matchSearch = t.title.toLowerCase().includes(filter.toLowerCase());
    const matchStatus = statusFilter ? t.status === statusFilter : true;
    return matchSearch && matchStatus;
  });

  const canCreate = ['SUPERVISOR', 'RESEARCHER'].includes(currentUser?.role);
  const canAssign = ['SUPERVISOR', 'RESEARCHER'].includes(currentUser?.role);

  const handleCreate = async (e) => {
    e.preventDefault(); setSaving(true); setError('');
    try {
      await createTask({ ...form, creator_id: currentUser.user_id });
      setShowModal(false); setForm({ task_id: '', title: '', description: '', deadline: '', project_id: '' }); load();
    } catch (err) { setError(err.response?.data?.detail || 'Failed to create task.'); }
    setSaving(false);
  };

  const handleAssign = async (task_id) => {
    const studentId = prompt('Enter student user ID to assign:');
    if (!studentId) return;
    try { await assignTask(task_id, { assignee_id: studentId, requestor_id: currentUser.user_id }); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error assigning task.'); }
  };

  const handleStart = async (task_id) => {
    try { await startTask(task_id, currentUser.user_id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error starting task.'); }
  };

  const handleComplete = async (task_id) => {
    try { await completeTask(task_id, currentUser.user_id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error completing task.'); }
  };

  const handleDelete = async (task_id) => {
    if (!window.confirm('Delete this task?')) return;
    try { await deleteTask(task_id, currentUser.user_id); load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error deleting task.'); }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Tasks</h1>
          <p className="page-subtitle">{tasks.length} task{tasks.length !== 1 ? 's' : ''} total</p>
        </div>
        {canCreate && (
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
            New Task
          </button>
        )}
      </div>

      <div className="filter-bar">
        <div className="search-input-wrap" style={{ flex: 2 }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input className="form-input search-input" placeholder="Search tasks..."
            value={filter} onChange={e => setFilter(e.target.value)} />
        </div>
        <select className="form-input" style={{ maxWidth: 180 }} value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
          <option value="">All statuses</option>
          {['CREATED','ASSIGNED','IN_PROGRESS','COMPLETED','OVERDUE'].map(s =>
            <option key={s} value={s}>{s}</option>
          )}
        </select>
      </div>

      {loading
        ? <div className="loading-wrap"><div className="spinner" /></div>
        : filtered.length === 0
          ? <div className="empty-state card"><div className="empty-state-icon">✅</div><h3>No tasks found</h3><p>Create a task within a project to get started.</p></div>
          : (
            <div className="card" style={{ padding: 0 }}>
              <div className="table-wrap">
                <table>
                  <thead><tr>
                    <th>Title</th><th>Assigned To</th><th>Status</th>
                    <th>Deadline</th><th>Actions</th>
                  </tr></thead>
                  <tbody>
                    {filtered.map(t => {
                      const isAssignee = t.assigned_to === currentUser?.user_id;
                      return (
                        <tr key={t.task_id}>
                          <td>
                            <div style={{ fontWeight: 500 }}>{t.title}</div>
                            <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{t.description?.slice(0, 60)}{t.description?.length > 60 ? '…' : ''}</div>
                          </td>
                          <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                            {t.assigned_to || <span style={{ fontStyle: 'italic' }}>Unassigned</span>}
                          </td>
                          <td><span className={`badge ${STATUS_BADGE[t.status] || 'badge-gray'}`}>{t.status}</span></td>
                          <td style={{ fontSize: 13, color: t.status === 'OVERDUE' ? 'var(--danger)' : 'var(--text-muted)' }}>
                            {t.deadline}
                          </td>
                          <td>
                            <div style={{ display: 'flex', gap: 6 }}>
                              {canAssign && t.status === 'CREATED' && (
                                <button className="btn btn-ghost btn-sm" onClick={() => handleAssign(t.task_id)}>Assign</button>
                              )}
                              {isAssignee && t.status === 'ASSIGNED' && (
                                <button className="btn btn-ghost btn-sm" onClick={() => handleStart(t.task_id)}>Start</button>
                              )}
                              {isAssignee && t.status === 'IN_PROGRESS' && (
                                <button className="btn btn-primary btn-sm" onClick={() => handleComplete(t.task_id)}>Complete</button>
                              )}
                              {canAssign && !['IN_PROGRESS','COMPLETED'].includes(t.status) && (
                                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(t.task_id)}>Delete</button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )
      }

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">Create New Task</h3>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Task ID</label>
                <input className="form-input" placeholder="e.g. task-001" required
                  value={form.task_id} onChange={e => setForm({ ...form, task_id: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Title</label>
                <input className="form-input" placeholder="Task title" required
                  value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea className="form-input" rows={2}
                  value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Project</label>
                <select className="form-input" required value={form.project_id} onChange={e => setForm({ ...form, project_id: e.target.value })}>
                  <option value="">Select a project</option>
                  {projects.filter(p => p.status === 'ACTIVE').map(p =>
                    <option key={p.project_id} value={p.project_id}>{p.title}</option>
                  )}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Deadline</label>
                <input className="form-input" type="date" required
                  min={new Date().toISOString().split('T')[0]}
                  value={form.deadline} onChange={e => setForm({ ...form, deadline: e.target.value })} />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Creating...' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
