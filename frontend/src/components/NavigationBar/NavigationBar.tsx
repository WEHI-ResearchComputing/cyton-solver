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
import SettingsButton from '../Buttons/SettingsButton';
import FitButton from '../Buttons/FitButton';
import UploadButton from '../Buttons/UploadButton';
import HelpButton from '../Buttons/HelpButton';
import { EvolutionLive } from '../Plots/EvolutionLive';
import { ProbabilityDist } from '../Plots/ProbabilityDist';
import { CellsVsGens } from '../Plots/CellsVsGens';
import { CytonClient, Parameters, ExperimentData_Output } from "../../client"
import { useAsync } from 'react-async-hook';
import ParameterForm from "../Form/Parameters"
import { FormProvider, useForm } from 'react-hook-form';
import { List, ListItem, MenuItem, TextField, Select } from "@mui/material";
import { useSnackbar } from 'notistack';
import {makeErrorMsg} from "../../utils";

const drawerWidth = 240;
// Wait 5 seconds between each request
const fitCheckInterval = 5000;

function NavigationBar() {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const checkFitStatus = async (taskId: string) => {
    try {
      const result = await client.default.checkStatusApiCheckStatusPost({
        taskId
      });
      if (result) {
        // If we received a valid object, then we can stop waiting
        closeSnackbar();
        enqueueSnackbar({
          variant: "success",
          message: "Fit successfully completed. Parameters have been updated.",
          preventDuplicate: true
        })
        methods.reset(result, {
          keepDefaultValues: true,
          keepDirty: true
        })
      }
      else {
        // If we received "undefined", then retry in another 5 seconds
        setTimeout(checkFitStatus, fitCheckInterval, taskId);
      }
    }
    catch(e){
      enqueueSnackbar({
        variant: "error",
        message: makeErrorMsg(e)
      })
    }
  };

  const client = new CytonClient({
    BASE: "http://localhost:9999"
  });
  const theme = useTheme();
  const methods = useForm<Parameters>({
    mode: "onChange"
  })
  const defaults = useAsync(async () => {
    const ret = await client.default.defaultSettingsApiDefaultSettingsGet();
    // Update the form default values
    methods.reset(ret.parameters, { keepDefaultValues: false });
    return ret;
  }, []);
  const formData = methods.watch();
  const extrapolated = useAsync(async (parameters: string) => {
    // Don't extrapolate until we have parameters
    if (!formData.b) {
      return;
    }
    return client.default.extrapolateApiExtrapolatePost({
      requestBody: {
        parameters: formData
      }
    })
    // Stringify here prevents excessive re-renders due to a bad comparison
  }, [JSON.stringify(formData)]);
  const [open, setOpen] = useState(true);
  const [experimentData, setExperimentData] = useState<ExperimentData_Output>();
  const [condition, setCondition] = useState<string>();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  let plots: React.JSX.Element[];
  let cvgPlots: React.JSX.Element[];
  if (typeof extrapolated.result != "undefined") {
    cvgPlots = extrapolated.result.hts.cells_gen[0].map((_, timepoint) =>
      <CellsVsGens extrapolationData={extrapolated.result} timepoint={timepoint} />
    )
    plots = [
      <EvolutionLive extrapolationData={extrapolated.result} />,
      <ProbabilityDist extrapolationData={extrapolated.result} />
    ]
  }
  else {
    cvgPlots = [];
    plots = [];
  }

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
          <ParameterForm />
          <Box sx={{ marginTop: 'auto' }}>
            <Divider />
            <List>
              <UploadButton client={client} onUpload={result => {
                setExperimentData(result)
                setCondition(result.conditions[0])
              }} />
              <FitButton experimentData={experimentData} client={client} settings={defaults.result} condition={condition} onSuccess={result => {
                closeSnackbar();
                const snackId = enqueueSnackbar({
                  variant: "success",
                  message: "Fit request successfully submitted. Please wait for parameter fitting...",
                  autoHideDuration: 1000 * 100,
                  // persist: true,
                  preventDuplicate: true
                })
                setTimeout(checkFitStatus, fitCheckInterval, result.task_id)
              }} />
              <ListItem>
                <Select
                  label="Select"
                  fullWidth={true}
                  value={condition || ""}
                  onChange={condition => {
                    setCondition(condition.target.value)
                  }}
                >
                  {experimentData?.conditions.map((cond) => (
                    <MenuItem key={cond} value={cond}>
                      {cond}
                    </MenuItem>
                  ))}
                </Select>
              </ListItem>
              <SettingsButton />
              <HelpButton />
            </List>
          </Box>
        </Drawer>
        <Main open={open}>
          <DrawerHeader />
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', width: '100%' }}>
            {cvgPlots}
          </div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', paddingTop: '20px', width: '100%' }}>
            {plots}
          </div>
        </Main>
      </Box>
    </FormProvider>
  );
}
export default NavigationBar;
