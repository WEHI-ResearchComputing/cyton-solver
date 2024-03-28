import * as React from "react";
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import { CytonClient, Parameters, ExperimentData_Output } from "../../client"

const FitButton = ({ enabled, client, experimentData }: { enabled: boolean, client: CytonClient, experimentData: ExperimentData_Output }) => {
  return (
    <ListItem disablePadding>
      <ListItemButton onClick={() => {
        // client.root.startFitApiStartFitPost({})
      }}>
        <ListItemIcon style={{ minWidth: '40px' }}>
          <PlayCircleOutlineIcon />
        </ListItemIcon>
        <ListItemText primary="Fit" />
      </ListItemButton>
    </ListItem>
  )
};

export default FitButton;
