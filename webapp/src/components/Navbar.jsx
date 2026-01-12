import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <Box sx={{ flexGrow: 1, mb: 4 }}>
            <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(10px)' }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
                        Payments
                    </Typography>
                    <Button
                        variant="contained"
                        color="primary"
                        startIcon={<AddIcon />}
                        component={Link}
                        to="/new"
                        sx={{ fontWeight: 'bold' }}
                    >
                        New
                    </Button>
                </Toolbar>
            </AppBar>
        </Box>
    );
}

export default Navbar;
