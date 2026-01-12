import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Container, Box, Typography } from '@mui/material';
import TransactionList from './components/TransactionList';
import Navbar from './components/Navbar';
import CreateTransaction from './components/CreateTransaction';
import theme from './theme';
import './App.css';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box
          sx={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            bgcolor: 'background.default',
          }}
        >
          <Navbar />
          <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', py: 4 }}>
            <Container maxWidth="lg">
              <Routes>
                <Route path="/" element={<TransactionList />} />
                <Route path="/new" element={<CreateTransaction />} />
              </Routes>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
