
import { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

export const Products = () => {
    const [formData, setFormData] = useState({
        p_name: "",
        quantity: "",
        price: "",
        min_stock_level: "",
    });

    const [categories, setCategories] = useState([]);
    const [select_c_id, setSelect_C_id] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [listProducts, setlistProducts] = useState([])
    const nameRegex = /^[a-zA-Z0-9_ ]+$/;
    const quantityRegex = /^\d+$/;
    const priceRegex = /^\d+(\.\d{1,2})?$/;
    const stockRegex = /^\d+$/;

    useEffect(() => {
        axios
            .get(`${API_BASE}/categories`)
            .then((res) => setCategories(res.data))
            .catch((err) => {
                console.error(err.response?.data || err.message);
            });
            fetchProducts();

        axios
            .get(`${API_BASE}/products`)
            .then((res) => setlistProducts(res.data))
            .catch((err) => {
                console.error(err.response?.data || err.message);
            });

    }, []);

    const fetchProducts = () => {
        axios
            .get(`${API_BASE}/products`)
            .then((res) => setlistProducts(res.data))
            .catch((err) => {
            console.error(err.response?.data || err.message);
            });
    };
    const isValidName = (value) => {
        setFormData((prev) => ({ ...prev, p_name: value }));
        setError(
            value && !nameRegex.test(value)
                ? "Use only letters, numbers, spaces, and underscores."
                : ""
        );
    };

    const isValidQuantity = (value) => {
        setFormData((prev) => ({ ...prev, quantity: value }));
        setError(
            value !== "" && !quantityRegex.test(value)
                ? "Quantity must be a whole number."
                : ""
        );
    };

    const isValidPrice = (value) => {
        setFormData((prev) => ({ ...prev, price: value }));
        setError(
            value !== "" && !priceRegex.test(value)
                ? "Enter a valid price, e.g. 199.99."
                : ""
        );
    };

    const isValidStock = (value) => {
        setFormData((prev) => ({
            ...prev,
            min_stock_level: value,
        }));
        setError(
            value !== "" && !stockRegex.test(value)
                ? "Minimum stock level must be a whole number."
                : ""
        );
    };

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!nameRegex.test(formData.p_name)) {
            setError("Invalid product name.");
            return;
        }

        if (
            !quantityRegex.test(formData.quantity) ||
            Number(formData.quantity) < 0
        ) {
            setError("Enter a valid non-negative quantity.");
            return;
        }

        if (
            !priceRegex.test(formData.price) ||
            Number(formData.price) < 0
        ) {
            setError("Enter a valid non-negative price.");
            return;
        }

        if (
            !stockRegex.test(formData.min_stock_level) ||
            Number(formData.min_stock_level) < 0
        ) {
            setError("Enter a valid minimum stock level.");
            return;
        }

        if (!select_c_id) {
            setError("Please select a category.");
            return;
        }

        try {
            const res = await axios.post(`${API_BASE}/products`, {
                p_name: formData.p_name,
                quantity: Number(formData.quantity),
                price: Number(formData.price),
                min_stock_level: Number(formData.min_stock_level),
                c_id: Number(select_c_id),
            });
            await fetchProducts();

            console.log(res.data);

            setFormData({
                p_name: "",
                quantity: "",
                price: "",
                min_stock_level: "",
            });

            setSelect_C_id("");
            setSuccess("Product added successfully!");
        } catch (err) {
            console.error(err.response?.data || err.message);
            setError(
                err.response?.data?.detail
                    ? JSON.stringify(err.response.data.detail)
                    : "Failed to add product."
            );
        }
    }

    return (
        <div>
            <h2>Add Products</h2>
            <div>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Enter product name"
                        value={formData.p_name}
                        onChange={(e) => isValidName(e.target.value)}
                        required
                    />

                    <input
                        type="number"
                        min="0"
                        step="1"
                        placeholder="Enter quantity"
                        value={formData.quantity}
                        onChange={(e) => isValidQuantity(e.target.value)}
                        required
                    />

                    <input
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="Enter price"
                        value={formData.price}
                        onChange={(e) => isValidPrice(e.target.value)}
                        required
                    />

                    <input
                        type="number"
                        min="0"
                        step="1"
                        placeholder="Enter minimum stock level"
                        value={formData.min_stock_level}
                        onChange={(e) => isValidStock(e.target.value)}
                        required
                    />

                    <select
                        value={select_c_id}
                        onChange={(e) => setSelect_C_id(e.target.value)}
                        required
                    >
                        <option value="">Select category</option>

                        {categories.map((category) => (
                            <option key={category.c_id} value={category.c_id}>
                                {category.c_name}
                            </option>
                        ))}
                    </select>

                    {error && <p style={{ color: "red" }}>{error}</p>}
                    {success && <p style={{ color: "green" }}>{success}</p>}

                    <button type="submit">Add Product</button>
                </form>
            </div>

            <div>
                <h2>List Of Products</h2>
                <table>


                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Minimum Stock Level</th>
                            <th>Category ID</th>
                            <th> C_name</th>
                        </tr>
                    </thead>

                    <tbody>
                        {listProducts.map((prod) => (
                            <tr key={prod.p_id}>
                                <td>{prod.p_id}</td>
                                <td>{prod.p_name}</td>
                                <td>{prod.quantity}</td>
                                <td>{prod.price}</td>
                                <td>{prod.min_stock_level}</td>
                                <td>{prod.c_id}</td>
                                <td> {prod.category.c_name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>


        </div>
    );
};
