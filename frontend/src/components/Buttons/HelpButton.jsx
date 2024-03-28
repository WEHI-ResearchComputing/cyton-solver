import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";

const HelpButton = () => {
  return (
    <ListItem disablePadding>
      <ListItemButton>
        <ListItemIcon style={{ minWidth: '40px' }}>
          <HelpOutlineIcon />
        </ListItemIcon >
        <ListItemText primary="Help" />
      </ListItemButton>
    </ListItem>
  )
};

export default HelpButton;
