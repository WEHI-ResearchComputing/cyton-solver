import * as React from 'react';
import { useState, useEffect } from 'react';
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
import {EvolutionLive} from '../Plots/EvolutionLive';
import TestPlot2 from '../Plots/TestPlot2';
import {CytonClient, ExperimentSettings_Output, Parameters} from "../../client"
import { useAsync } from 'react-async-hook';
import ParameterForm from "../Form/Parameters"
import { FormProvider, useForm } from 'react-hook-form';

const drawerWidth = 240;

function NavigationBar() {
  const client = new CytonClient({
    BASE: "http://localhost:9999"
  });
  const defaults = useAsync(client.root.defaultSettingsDefaultSettingsGet, []);
  const theme = useTheme();
  // const [defaults, setDefaults] = useState<ExperimentSettings_Output | undefined>(undefined);
  const methods = useForm<Parameters>({
    defaultValues: async () => (await defaults.currentPromise).parameters ,
    mode: "onChange",
  })
  const formData = methods.watch();
  const extrapolated = useAsync(async (parameters) =>{
    return client.root.extrapolateExtrapolatePost({
      requestBody: {
        parameters: formData
      }
    })
    // Stringify here prevents excessive re-renders due to a bad comparison
  }, [JSON.stringify(formData)]);
  const [open, setOpen] = useState(false);
  // const [parameters, setParameters] = useState<Parameters>(null);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  // useAsync(async () => {
  //   const defaults = await client.root.defaultSettingsDefaultSettingsGet();
  //   setDefaults(defaults);
  // }, []);

  return (
    <FormProvider {...methods}>
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
        <ParameterForm/>
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
          <EvolutionLive extrapolationData={extrapolated.result}/>
          {/* {JSON.stringify(extrapolated, null, 4)} */}
          {/* <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot />
          <TestPlot /> */}
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', paddingTop: '20px', width: '100%'}}>
        {/* <TestPlot2 />
        <TestPlot2 /> */}
      </div>
      </Main>
    </Box>
    </FormProvider>
  );
}
export default NavigationBar;
