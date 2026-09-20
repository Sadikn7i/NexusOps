import { useEffect, useState } from "react";
import api from "../api";

interface Employee {
  id: number;
  employee_number: string;
  name: string;
  email: string;
  department_id: number | null;
  position: string | null;
  hire_date: string | null;
  status: string;
}

function Employees() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    employee_number: "",
    name: "",
    email: "",
    position: "",
    hire_date: "",
    status: "active",
  });

  const fetchEmployees = async () => {
    const res = await api.get("/api/employees");
    setEmployees(res.data);
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/api/employees", formData);
    setFormData({ employee_number: "", name: "", email: "", position: "", hire_date: "", status: "active" });
    setShowForm(false);
    fetchEmployees();
  };

  const handleDelete = async (id: number) => {
    await api.delete(`/api/employees/${id}`);
    fetchEmployees();
  };

  const filtered = employees.filter((emp) =>
    emp.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Employees</h1>
          <div className="subtitle">{employees.length} on record</div>
        </div>
        <button className="btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Add Employee"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card form-card">
          <input className="input" placeholder="Employee number" value={formData.employee_number}
            onChange={(e) => setFormData({ ...formData, employee_number: e.target.value })} required />
          <input className="input" placeholder="Full name" value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })} required style={{ flex: 1, minWidth: "160px" }} />
          <input className="input" placeholder="Email" value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })} required style={{ flex: 1, minWidth: "160px" }} />
          <input className="input" placeholder="Position" value={formData.position}
            onChange={(e) => setFormData({ ...formData, position: e.target.value })} />
          <input className="input" type="date" value={formData.hire_date}
            onChange={(e) => setFormData({ ...formData, hire_date: e.target.value })} />
          <button type="submit" className="btn">Save</button>
        </form>
      )}

      <input
        className="input"
        placeholder="Search by name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: "16px", width: "280px" }}
      />

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Position</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((emp) => (
              <tr key={emp.id}>
                <td className="mono" style={{ color: "var(--text-dim)" }}>{emp.employee_number}</td>
                <td>{emp.name}</td>
                <td style={{ color: "var(--text-dim)" }}>{emp.email}</td>
                <td>{emp.position}</td>
                <td>
                  <span className={`status status-${emp.status}`}>
                    <span className="dot" />
                    {emp.status}
                  </span>
                </td>
                <td style={{ textAlign: "right" }}>
                  <button className="btn-ghost" onClick={() => handleDelete(emp.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Employees;