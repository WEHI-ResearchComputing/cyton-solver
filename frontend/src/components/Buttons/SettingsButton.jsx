import { useState } from 'react';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import SettingsIcon from '@mui/icons-material/Settings';
import SettingsDialog from "../Dialogs/SettingsDialog";

const SettingsButton = () => {
  const [openModal, setOpenModal] = useState(false);

  const handleButtonClick = () => {
    setOpenModal(true);
  };

  const handleModalClose = () => {
    setOpenModal(false);
  };
  return (
    <ListItem disablePadding>
      <ListItemButton onClick={handleButtonClick}>
        <ListItemIcon style={{ minWidth: '40px' }}>
          <SettingsIcon />
        </ListItemIcon>
        <ListItemText primary="Settings" />
      </ListItemButton>
      <SettingsDialog open={openModal} onClose={handleModalClose} />
    </ListItem>
  )
};

export default SettingsButton;
