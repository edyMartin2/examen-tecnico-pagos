import { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Chip,
    CircularProgress,
    Grid,
    Alert,
    Typography,
    Box
} from '@mui/material';

function TransactionList() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const httpUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
    useEffect(() => {
        // Obtenemos la URL base (http://localhost:8000 -> ws://localhost:8000)

        const wsUrl = httpUrl.replace(/^http/, 'ws');

        const socket = new WebSocket(`${wsUrl}/api/v1/transactions/ws`);

        socket.onopen = () => {
            console.log('Connected to WebSocket');
            setError(null);
        };

        socket.onmessage = (event) => {
            try {
                const result = JSON.parse(event.data);
                if (result.data) {
                    setData(result.data);
                    setLoading(false);
                }
            } catch (err) {
                console.error("Error parsing WebSocket message:", err);
            }
        };

        socket.onerror = (error) => {
            console.error('WebSocket Error:', error);
            setError('Connection failed');
            setLoading(false);
        };

        socket.onclose = () => {
            console.log('Disconnected from WebSocket');
        };

        // Cleanup on unmount
        return () => {
            socket.close();
        };
    }, []);

    const processTransaction = async (transactionId) => {
        try {
            const response = await fetch(`${httpUrl}/api/v1/transactions/async-process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': ''
                },
                body: JSON.stringify({ id: transactionId }),
            });

            if (!response.ok) {
                throw new Error('Failed to process transaction');
            }

            console.log('Transaction processed successfully');
        } catch (error) {
            console.error('Error processing transaction:', error);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'success': return 'success';
            case 'failed': return 'error';
            case 'pending': return 'warning';
            default: return 'default';
        }
    };

    if (loading) return (
        <Grid container justifyContent="center" alignItems="center" style={{ minHeight: '200px' }}>
            <CircularProgress />
        </Grid>
    );

    if (error) return (
        <Grid container justifyContent="center" alignItems="center" style={{ minHeight: '200px' }}>
            <Alert severity="error">Error: {error}</Alert>
        </Grid>
    );

    return (
        <Grid
            container
            spacing={3}
            direction="column"
            alignItems="center"
            justifyContent="center"
            sx={{ width: '100%', minHeight: '80vh' }}
        >
            <Grid item sx={{ width: '100%', maxWidth: 1200 }}>
                <TableContainer component={Paper} elevation={3}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>ID</TableCell>
                                <TableCell>User</TableCell>
                                <TableCell>Type</TableCell>
                                <TableCell align="right">Amount</TableCell>
                                <TableCell align="center">Status</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((transaction) => (
                                <TableRow
                                    key={transaction.idempotency_key}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row" sx={{ fontFamily: 'monospace', color: 'text.secondary' }}>
                                        {transaction.idempotency_key}
                                    </TableCell>
                                    <TableCell>{transaction.user_id}</TableCell>
                                    <TableCell sx={{ textTransform: 'capitalize' }}>{transaction.type}</TableCell>
                                    <TableCell align="right" sx={{ fontFamily: 'monospace', fontWeight: 'bold' }}>
                                        ${transaction.amount.toFixed(2)}
                                    </TableCell>
                                    <TableCell align="center">
                                        <Chip
                                            label={transaction.status}
                                            color={getStatusColor(transaction.status)}
                                            variant="outlined"
                                            size="small"
                                            sx={{ textTransform: 'uppercase', fontWeight: 600 }}
                                        />
                                    </TableCell>
                                    <TableCell align="center">
                                        <button type="button" onClick={
                                            () => {
                                                processTransaction(transaction.idempotency_key);
                                            }
                                        }>Process</button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Grid>
        </Grid>
    );
}

export default TransactionList;
