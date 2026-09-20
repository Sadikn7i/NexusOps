import { Link, Outlet, useNavigate, useLocation } from "react-router-dom";
import { LayoutDashboard, Users, Building2, Monitor, Ticket, LogOut, Cog } from "lucide-react";

function Layout() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const links = [
    { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/employees", label: "Employees", icon: Users },
    { to: "/departments", label: "Departments", icon: Building2 },
    { to: "/assets", label: "Assets", icon: Monitor },
    { to: "/tickets", label: "IT Tickets", icon: Ticket },
    { to: "/machines", label: "Production", icon: Cog },
  ];

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <div
        style={{
          width: "240px",
          flexShrink: 0,
          background: "#1b1e26",
          borderRight: "1px solid #2a2e39",
          padding: "28px 14px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div style={{ padding: "0 12px", marginBottom: "36px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#f5a623" }} />
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "13px", color: "#8b90a0", letterSpacing: "0.02em" }}>
              SYS-01
            </span>
          </div>
          <h2 style={{ fontSize: "17px", marginTop: "6px" }}>Company System</h2>
        </div>

        <nav style={{ display: "flex", flexDirection: "column", gap: "2px", flex: 1 }}>
          {links.map(({ to, label, icon: Icon }) => {
            const active = location.pathname === to;
            return (
              <Link
                key={to}
                to={to}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "11px",
                  padding: "10px 12px",
                  borderLeft: active ? "2px solid #f5a623" : "2px solid transparent",
                  color: active ? "#e8eaf0" : "#8b90a0",
                  background: active ? "#232733" : "transparent",
                  textDecoration: "none",
                  fontSize: "14.5px",
                  fontWeight: active ? 600 : 400,
                  marginLeft: "-2px",
                }}
              >
                <Icon size={17} strokeWidth={2} />
                {label}
              </Link>
            );
          })}
        </nav>

        <button
          onClick={handleLogout}
          className="btn btn-secondary"
          style={{ display: "flex", alignItems: "center", gap: "8px", justifyContent: "center" }}
        >
          <LogOut size={15} />
          Log Out
        </button>
      </div>
      <div style={{ flex: 1, background: "#14161c" }}>
        <Outlet />
      </div>
    </div>
  );
}

export default Layout;