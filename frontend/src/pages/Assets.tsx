import { useEffect, useState } from "react";
import api from "../api";

interface Asset {
  id: number;
  asset_number: string;
  asset_type: string;
  name: string;
  assigned_employee_id: number | null;
  purchase_date: string | null;
  status: string;
}

function Assets() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    asset_number: "",
    asset_type: "",
    name: "",
    purchase_date: "",
    status: "active",
  });

  const fetchAssets = async () => {
    const res = await api.get("/api/assets");
    setAssets(res.data);
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/api/assets", formData);
    setFormData({ asset_number: "", asset_type: "", name: "", purchase_date: "", status: "active" });
    setShowForm(false);
    fetchAssets();
  };

  const handleDelete = async (id: number) => {
    await api.delete(`/api/assets/${id}`);
    fetchAssets();
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Assets</h1>
          <div className="subtitle">{assets.length} assets tracked</div>
        </div>
        <button className="btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Add Asset"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card form-card">
          <input className="input" placeholder="Asset number" value={formData.asset_number}
            onChange={(e) => setFormData({ ...formData, asset_number: e.target.value })} required />
          <input className="input" placeholder="Type (Laptop, Monitor...)" value={formData.asset_type}
            onChange={(e) => setFormData({ ...formData, asset_type: e.target.value })} required style={{ flex: 1, minWidth: "160px" }} />
          <input className="input" placeholder="Name" value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })} required style={{ flex: 1, minWidth: "160px" }} />
          <input className="input" type="date" value={formData.purchase_date}
            onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })} />
          <button type="submit" className="btn">Save</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Asset #</th>
              <th>Type</th>
              <th>Name</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {assets.map((asset) => (
              <tr key={asset.id}>
                <td className="mono" style={{ color: "var(--text-dim)" }}>{asset.asset_number}</td>
                <td>{asset.asset_type}</td>
                <td>{asset.name}</td>
                <td>
                  <span className={`status status-${asset.status}`}>
                    <span className="dot" />
                    {asset.status}
                  </span>
                </td>
                <td style={{ textAlign: "right" }}>
                  <button className="btn-ghost" onClick={() => handleDelete(asset.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Assets;