import { useEffect, useState } from "react";
import api from "../api";

interface Department {
  id: number;
  name: string;
  manager: string | null;
}

function Departments() {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: "", manager: "" });

  const fetchDepartments = async () => {
    const res = await api.get("/api/departments");
    setDepartments(res.data);
  };

  useEffect(() => {
    fetchDepartments();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/api/departments", formData);
    setFormData({ name: "", manager: "" });
    setShowForm(false);
    fetchDepartments();
  };

  const handleDelete = async (id: number) => {
    await api.delete(`/api/departments/${id}`);
    fetchDepartments();
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Departments</h1>
          <div className="subtitle">{departments.length} departments</div>
        </div>
        <button className="btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Add Department"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card form-card">
          <input className="input" placeholder="Name" value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })} required style={{ flex: 1 }} />
          <input className="input" placeholder="Manager" value={formData.manager}
            onChange={(e) => setFormData({ ...formData, manager: e.target.value })} style={{ flex: 1 }} />
          <button type="submit" className="btn">Save</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Manager</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {departments.map((dept) => (
              <tr key={dept.id}>
                <td className="mono" style={{ color: "var(--text-dim)" }}>{String(dept.id).padStart(3, "0")}</td>
                <td>{dept.name}</td>
                <td style={{ color: "var(--text-dim)" }}>{dept.manager || "—"}</td>
                <td style={{ textAlign: "right" }}>
                  <button className="btn-ghost" onClick={() => handleDelete(dept.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Departments;