import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import UploadFileIcon from '@mui/icons-material/UploadFile';

const UploadButton = () => {
    return (
        <List>
          <ListItem  disablePadding>
            <ListItemButton>
              <ListItemIcon style={{minWidth: '40px'}}>
                <UploadFileIcon />
              </ListItemIcon>
              <ListItemText primary="Upload" />
            </ListItemButton>
          </ListItem>
        </List>
    )
};

export default UploadButton;
