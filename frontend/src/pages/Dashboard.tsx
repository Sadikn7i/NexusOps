import { useEffect, useState } from "react";
import api from "../api";

function Dashboard() {
  const [employeeCount, setEmployeeCount] = useState(0);
  const [assetCount, setAssetCount] = useState(0);
  const [ticketCount, setTicketCount] = useState(0);

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const [employeesRes, assetsRes, ticketsRes] = await Promise.all([
          api.get("/api/employees"),
          api.get("/api/assets"),
          api.get("/api/tickets"),
        ]);
        setEmployeeCount(employeesRes.data.length);
        setAssetCount(assetsRes.data.length);
        setTicketCount(ticketsRes.data.filter((t: any) => t.status !== "resolved").length);
      } catch (err) {
        console.error("Failed to fetch dashboard data", err);
      }
    };
    fetchCounts();
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <div className="subtitle">Overview of company records</div>
        </div>
      </div>

      <div className="stat-strip">
        <div className="stat" style={{ ["--accent-color" as any]: "#5b9bf7" }}>
          <div className="label">Employees</div>
          <div className="value mono">{String(employeeCount).padStart(2, "0")}</div>
        </div>
        <div className="stat" style={{ ["--accent-color" as any]: "#3ecf8e" }}>
          <div className="label">Assets tracked</div>
          <div className="value mono">{String(assetCount).padStart(2, "0")}</div>
        </div>
        <div className="stat" style={{ ["--accent-color" as any]: "#f5a623" }}>
          <div className="label">Open tickets</div>
          <div className="value mono">{String(ticketCount).padStart(2, "0")}</div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;