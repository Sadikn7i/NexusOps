import { useEffect, useState } from "react";
import api from "../api";

interface Ticket {
  id: number;
  employee_id: number;
  title: string;
  description: string | null;
  priority: string;
  status: string;
  created_at: string;
}

function Tickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState("all");
  const [formData, setFormData] = useState({
    employee_id: 1,
    title: "",
    description: "",
    priority: "medium",
  });

  const fetchTickets = async () => {
    const res = await api.get("/api/tickets");
    setTickets(res.data);
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/api/tickets", formData);
    setFormData({ employee_id: 1, title: "", description: "", priority: "medium" });
    setShowForm(false);
    fetchTickets();
  };

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/api/tickets/${id}`, { status });
    fetchTickets();
  };

  const filtered = filter === "all" ? tickets : tickets.filter((t) => t.status === filter);
  const tabs = ["all", "open", "in_progress", "resolved"];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>IT Support Tickets</h1>
          <div className="subtitle">{tickets.filter((t) => t.status !== "resolved").length} open</div>
        </div>
        <button className="btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Create Ticket"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card form-card">
          <input className="input" type="number" placeholder="Employee ID" value={formData.employee_id}
            onChange={(e) => setFormData({ ...formData, employee_id: Number(e.target.value) })} required style={{ width: "110px" }} />
          <input className="input" placeholder="Title" value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })} required style={{ flex: 1, minWidth: "180px" }} />
          <input className="input" placeholder="Description" value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })} style={{ flex: 1, minWidth: "180px" }} />
          <select className="input" value={formData.priority}
            onChange={(e) => setFormData({ ...formData, priority: e.target.value })}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <button type="submit" className="btn">Save</button>
        </form>
      )}

      <div className="tab-row">
        {tabs.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`tab ${filter === s ? "active" : ""}`}
          >
            {s === "all" ? "All" : s.replace("_", " ")}
          </button>
        ))}
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Ticket</th>
              <th>Title</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((ticket) => (
              <tr key={ticket.id}>
                <td className="mono" style={{ color: "var(--text-dim)" }}>#{String(ticket.id).padStart(3, "0")}</td>
                <td>{ticket.title}</td>
                <td>
                  <span className={`priority-tag priority-${ticket.priority}`}>{ticket.priority}</span>
                </td>
                <td>
                  <select
                    className="input"
                    value={ticket.status}
                    onChange={(e) => handleStatusChange(ticket.id, e.target.value)}
                    style={{ fontSize: "13px", padding: "5px 8px" }}
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                  </select>
                </td>
                <td className="mono" style={{ color: "var(--text-dim)", fontSize: "13px" }}>
                  {new Date(ticket.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Tickets;