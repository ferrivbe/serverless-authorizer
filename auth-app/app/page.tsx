"use-client"

import { useState } from 'react';
import { Box, AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText, Divider } from '@mui/material';

const drawerWidth = 240;

const Home = () => {
    const [open, setOpen] = useState(false);

    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    return (
        <div className="root">
            {/* Top bar */}
            <AppBar position="fixed" className={open ? 'appBarShift' : 'appBar'}>
                <Toolbar>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        onClick={handleDrawerOpen}
                        edge="start"
                        className={open ? 'hide' : 'menuButton'}
                    >
                        <span className="menuIcon"></span>
                    </IconButton>
                    <Typography variant="h6" noWrap>
                        Your App Name
                    </Typography>
                </Toolbar>
            </AppBar>

            {/* Left side menu */}
            <Drawer
                className="drawer"
                variant="persistent"
                anchor="left"
                open={open}
                classes={{
                    paper: 'drawerPaper',
                }}
            >
                <div className="drawerHeader">
                    <IconButton onClick={handleDrawerClose} className="menuCloseIcon">
                        <span className="chevronLeftIcon"></span>
                    </IconButton>
                </div>
                <Divider />
                <List>
                    {/* Add your menu items here */}
                    <ListItem button>
                        <ListItemIcon>
                            {/* Add your menu item icon here */}
                        </ListItemIcon>
                        <ListItemText primary="Menu Item 1" />
                    </ListItem>
                    <ListItem button>
                        <ListItemIcon>
                            {/* Add your menu item icon here */}
                        </ListItemIcon>
                        <ListItemText primary="Menu Item 2" />
                    </ListItem>
                    {/* Add more menu items if needed */}
                </List>
            </Drawer>

            {/* Main content area */}
            <main className={`content ${open ? 'contentShift' : ''}`}>
                <div className="drawerHeader" />

                {/* Center content */}
                <Box textAlign="center">
                    <Typography variant="h4" gutterBottom>
                        Welcome to Your Dashboard
                    </Typography>
                    <Typography variant="body1">
                        This is your beautifully designed and interactive dashboard.
                    </Typography>
                </Box>
            </main>
        </div>
    );
};

export default Home;
