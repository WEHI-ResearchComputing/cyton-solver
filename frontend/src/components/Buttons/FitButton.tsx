import * as React from "react";
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import { CytonClient, Parameters, ExperimentData_Output, ExperimentSettings_Output, FitResult } from "../../client"

const FitButton = ({ client, experimentData, condition, settings, onSuccess }: { client: CytonClient, experimentData: ExperimentData_Output | undefined, condition: string | undefined, settings: ExperimentSettings_Output | undefined, onSuccess: (result: FitResult) => void }) => {
  const disabled = !(experimentData && condition && settings);
  return (
    <ListItem disablePadding>
      <ListItemButton disabled={disabled} onClick={async () => {
        if (!disabled){
        const result = await client.default.startFitApiStartFitPost({
          condition,
          requestBody: {
            data: experimentData,
            settings
          } 
        })
        onSuccess(result);
      }
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
