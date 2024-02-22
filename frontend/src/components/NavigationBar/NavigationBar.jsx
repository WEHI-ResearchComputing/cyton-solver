import * as React from 'react';
import { Main, AppBar, DrawerHeader } from './Styles';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import InputSlider from '../Slider/Slider';
import SettingsButton from '../Buttons/SettingsButton';
import FitButton from '../Buttons/FitButton';
import UploadButton from '../Buttons/UploadButton';
import HelpButton from '../Buttons/HelpButton';
import TestPlot from '../Plots/TestPlot';
import TestPlot2 from '../Plots/TestPlot2';

const drawerWidth = 240;

function NavigationBar() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h4" fontSize="16px">
            Cyton Solver
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box'
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <InputSlider label="Parameter 1" min={0} max={100} step={10} />
        <InputSlider label="Parameter 2" min={0} max={200} step={10} />
        <InputSlider label="Parameter 3" min={0} max={300} step={10} />
        <InputSlider label="Parameter 4" min={0} max={400} step={10} />
        <InputSlider label="Parameter 5" min={0} max={500} step={10} />
        <Box sx={{ marginTop: 'auto' }}>
          <Divider />
          <UploadButton />
          <FitButton />
          <SettingsButton />
          <HelpButton />
        </Box>
      </Drawer>
      <Main open={open}>
        <DrawerHeader />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', width: '100%'}}>
          <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot />
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', paddingTop: '20px', width: '100%'}}>
        <TestPlot2 />
        <TestPlot2 />
      </div>
      </Main>
    </Box>
  );
}
export default NavigationBar;