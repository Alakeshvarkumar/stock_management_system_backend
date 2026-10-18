
import { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

export const AddCategory = () => {
  const [Name, setName] = useState("");
  const [error, setError] = useState("");
  const nameRegex = /^[a-zA-Z0-9_]+$/
  const isValidName = (value) =>{
    if(nameRegex.test(value)){
        setName(value);
        setError("");
    }
    else{
        setName(value)
        setError("Use only letters, numbers, and underscores.");
    }
  }
  async function handleSubmit(e) {
    e.preventDefault();
    if(!nameRegex.test(Name)){
        setError("Use only letters, numbers, and underscores.")
        return;
    }

    try {
      const res = await axios.post(`${API_BASE}/categories`, {
        c_name: Name,
      });

      console.log(res.data);
      setName("");
      setError("")
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
          onChange={(e) => isValidName(e.target.value)}
          required
        />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Add</button>
      </form>
    </div>
  );
};
