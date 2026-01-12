import { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    MenuItem,
    Alert,
    CircularProgress,
    Snackbar
} from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import { useNavigate } from 'react-router-dom';

function CreateTransaction() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        user_id: '',
        amount: '',
        type: 'charge'
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const transactionTypes = [
        { value: 'charge', label: 'Charge' },
        { value: 'refund', label: 'Refund' }
    ];

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Generamos UUID al vuelo para idempotencia
        const idempotencyId = uuidv4();

        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

            const payload = {
                user_id: formData.user_id,
                amount: parseFloat(formData.amount),
                type: formData.type
            };

            const response = await fetch(`${apiUrl}/api/v1/transactions/create/${idempotencyId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': ''
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create transaction');
            }

            setSuccess(true);
            // Redirigir después de un breve momento
            setTimeout(() => {
                navigate('/');
            }, 1500);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            width="100%"
        >
            <Card sx={{ width: '100%', maxWidth: 500, p: 2 }}>
                <CardContent>
                    <Typography variant="h4" component="h2" gutterBottom align="center" sx={{ mb: 3 }}>
                        New Transaction
                    </Typography>

                    {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

                    <form onSubmit={handleSubmit}>
                        <TextField
                            fullWidth
                            label="User ID"
                            name="user_id"
                            value={formData.user_id}
                            onChange={handleChange}
                            required
                            margin="normal"
                            placeholder="e.g. user_123"
                        />

                        <TextField
                            fullWidth
                            label="Amount"
                            name="amount"
                            type="number"
                            value={formData.amount}
                            onChange={handleChange}
                            required
                            margin="normal"
                            placeholder="0000"
                            inputProps={{ min: "0", step: "0.01" }}
                        />

                        <TextField
                            fullWidth
                            select
                            label="Type"
                            name="type"
                            value={formData.type}
                            onChange={handleChange}
                            margin="normal"
                        >
                            {transactionTypes.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.label}
                                </MenuItem>
                            ))}
                        </TextField>

                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            size="large"
                            sx={{ mt: 4, mb: 2, height: 48 }}
                            disabled={loading}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Create Transaction'}
                        </Button>

                        <Button
                            fullWidth
                            variant="outlined"
                            color="secondary"
                            onClick={() => navigate('/')}
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                    </form>
                </CardContent>
            </Card>

            <Snackbar
                open={success}
                autoHideDuration={6000}
                onClose={() => setSuccess(false)}
            >
                <Alert severity="success" sx={{ width: '100%' }}>
                    Transaction created successfully! Redirecting...
                </Alert>
            </Snackbar>
        </Box>
    );
}

export default CreateTransaction;
