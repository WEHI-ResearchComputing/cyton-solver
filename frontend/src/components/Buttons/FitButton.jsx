import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';

const FitButton = () => {
    return (
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon style={{minWidth: '40px'}}>
                <PlayCircleOutlineIcon />
              </ListItemIcon>
              <ListItemText primary="Fit" />
            </ListItemButton>
          </ListItem>
        </List>
    )
};

export default FitButton;
