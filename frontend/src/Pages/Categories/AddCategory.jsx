
import { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

export const AddCategory = () => {
  const [Name, setName] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await axios.post(`${API_BASE}/categories`, {
        c_name: Name,
      });

      console.log(res.data);
      setName("");
    } catch (error) {
      console.error(error.response?.data || error.message);
    }
  }

  return (
    <div>
      <h2>Add Category</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Category Name"
          value={Name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <button type="submit">Add</button>
      </form>
    </div>
  );
};
