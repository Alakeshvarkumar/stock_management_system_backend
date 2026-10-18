import React, { useState, useEffect } from 'react';
import axios from 'axios';
export const AddCategory = () => {
  const [Name, setName] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    console.log(Name);
    setName("");
  }
  function handleChange(){
    setName(e.target.value)
    console.log(Name)
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
