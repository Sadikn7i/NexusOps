import { useEffect, useState } from "react";
import api from "../api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface Machine {
  id: number;
  machine_number: string;
  department: string;
  status: string;
  hours_run: number;
}

// Simulated downtime data for demonstration — not from real sensors.
const downtimeData = [
  { month: "Jan", hours: 12 },
  { month: "Feb", hours: 34 },
  { month: "Mar", hours: 18 },
  { month: "Apr", hours: 41 },
  { month: "May", hours: 9 },
  { month: "Jun", hours: 26 },
];

const maxDowntime = Math.max(...downtimeData.map((d) => d.hours));

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div
      style={{
        background: "#1b1e26",
        border: "1px solid #2a2e39",
        borderRadius: "6px",
        padding: "8px 12px",
      }}
    >
      <div style={{ fontSize: "12px", color: "#8b90a0", marginBottom: "2px" }}>{label}</div>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "15px", color: "#e8eaf0" }}>
        {payload[0].value}h downtime
      </div>
    </div>
  );
}

function Machines() {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    machine_number: "",
    department: "",
    status: "running",
    hours_run: 0,
  });

  const fetchMachines = async () => {
    const res = await api.get("/api/machines");
    setMachines(res.data);
  };

  useEffect(() => {
    fetchMachines();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/api/machines", formData);
    setFormData({ machine_number: "", department: "", status: "running", hours_run: 0 });
    setShowForm(false);
    fetchMachines();
  };

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/api/machines/${id}`, { status });
    fetchMachines();
  };

  const running = machines.filter((m) => m.status === "running").length;
  const maintenance = machines.filter((m) => m.status === "maintenance").length;
  const offline = machines.filter((m) => m.status === "offline").length;
  const total = machines.length || 1;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Production Floor</h1>
          <div className="subtitle">{machines.length} machines registered</div>
        </div>
        <button className="btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Register Machine"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card form-card">
          <input className="input" placeholder="Machine number (CNC-004)" value={formData.machine_number}
            onChange={(e) => setFormData({ ...formData, machine_number: e.target.value })} required />
          <input className="input" placeholder="Department" value={formData.department}
            onChange={(e) => setFormData({ ...formData, department: e.target.value })} required style={{ flex: 1, minWidth: "160px" }} />
          <input className="input" type="number" placeholder="Hours run" value={formData.hours_run}
            onChange={(e) => setFormData({ ...formData, hours_run: Number(e.target.value) })} style={{ width: "120px" }} />
          <button type="submit" className="btn">Save</button>
        </form>
      )}

      {/* Fleet status bar — a single stacked bar showing the whole floor at a glance */}
      <div className="card" style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "14px" }}>
          <h3>Fleet status</h3>
          <span className="mono" style={{ fontSize: "13px", color: "var(--text-dim)" }}>
            {machines.length} units
          </span>
        </div>

        <div style={{ display: "flex", height: "10px", borderRadius: "5px", overflow: "hidden", background: "#232733" }}>
          {running > 0 && <div style={{ width: `${(running / total) * 100}%`, background: "#3ecf8e" }} />}
          {maintenance > 0 && <div style={{ width: `${(maintenance / total) * 100}%`, background: "#f5a623" }} />}
          {offline > 0 && <div style={{ width: `${(offline / total) * 100}%`, background: "#e5484d" }} />}
        </div>

        <div style={{ display: "flex", gap: "28px", marginTop: "16px" }}>
          <div className="status status-active">
            <span className="dot" />
            Running <span className="mono" style={{ color: "var(--text)" }}>{running}</span>
          </div>
          <div className="status status-maintenance">
            <span className="dot" />
            Maintenance <span className="mono" style={{ color: "var(--text)" }}>{maintenance}</span>
          </div>
          <div className="status status-offline">
            <span className="dot" />
            Offline <span className="mono" style={{ color: "var(--text)" }}>{offline}</span>
          </div>
        </div>
      </div>

      <div className="table-wrap" style={{ marginBottom: "24px" }}>
        <table>
          <thead>
            <tr>
              <th>Machine</th>
              <th>Department</th>
              <th>Hours run</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((m) => (
              <tr key={m.id}>
                <td className="mono">{m.machine_number}</td>
                <td>{m.department}</td>
                <td className="mono" style={{ color: "var(--text-dim)" }}>{m.hours_run.toLocaleString()}</td>
                <td>
                  <select
                    className="input"
                    value={m.status}
                    onChange={(e) => handleStatusChange(m.id, e.target.value)}
                    style={{ fontSize: "13px", padding: "5px 8px" }}
                  >
                    <option value="running">Running</option>
                    <option value="maintenance">Maintenance</option>
                    <option value="offline">Offline</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "20px" }}>
          <div>
            <h3>Downtime by month</h3>
            <div className="subtitle" style={{ marginTop: "2px" }}>Simulated data for demonstration</div>
          </div>
          <span className="mono" style={{ fontSize: "13px", color: "var(--text-dim)" }}>
            peak {maxDowntime}h
          </span>
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={downtimeData} barCategoryGap="28%">
            <CartesianGrid vertical={false} stroke="#2a2e39" strokeDasharray="0" />
            <XAxis
              dataKey="month"
              stroke="#8b90a0"
              fontSize={12.5}
              tickLine={false}
              axisLine={{ stroke: "#2a2e39" }}
            />
            <YAxis
              stroke="#8b90a0"
              fontSize={12.5}
              tickLine={false}
              axisLine={false}
              width={28}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(245,166,35,0.06)" }} />
            <Bar dataKey="hours" radius={[3, 3, 0, 0]} maxBarSize={36}>
              {downtimeData.map((entry, index) => (
                <Cell
                  key={index}
                  fill={entry.hours === maxDowntime ? "#f5a623" : "#4a4530"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Machines;