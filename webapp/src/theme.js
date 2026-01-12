import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#3b82f6',
        },
        background: {
            default: '#0f172a',
            paper: 'rgba(30, 41, 59, 0.7)',
        },
        text: {
            primary: '#f8fafc',
            secondary: '#94a3b8',
        },
        success: {
            main: '#22c55e',
        },
        error: {
            main: '#ef4444',
        },
        warning: {
            main: '#eab308',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontSize: '2.5rem',
            fontWeight: 700,
            background: 'linear-gradient(to right, #60a5fa, #a855f7)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            color: 'transparent',
            textAlign: 'center',
            marginBottom: '2rem',
        },
    },
    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backdropFilter: 'blur(12px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '16px',
                },
            },
        },
        MuiTableCell: {
            styleOverrides: {
                root: {
                    borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                },
                head: {
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    fontSize: '0.75rem',
                    letterSpacing: '0.05em',
                    color: '#94a3b8',
                },
            },
        },
    },
});

export default theme;
