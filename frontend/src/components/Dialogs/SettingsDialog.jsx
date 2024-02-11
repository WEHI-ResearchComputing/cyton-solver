import { useState } from 'react';
import PropTypes from 'prop-types';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Select, FormControl, MenuItem } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import './Dialogs.css';

function SettingsDialog({ open, onClose}) {

  const [selectedValue, setSelectedValue] = useState("lm");

  const handleSelectChange = (event) => {
    setSelectedValue(event.target.value);
  };

  return (
    <Dialog fullWidth open={open} onClose={onClose}>
      <DialogTitle
        sx={{
          backgroundColor: useTheme().palette.primary.main,
          textAlign: 'center',
          color: 'white',
          fontSize: 24,
          padding: '2px',
        }}
      >
        Settings
      </DialogTitle>
      <DialogContent>
      <div className= 'settingsContent'>
          <p className='settingsAlgorithm'>Optimization Algorithm</p>
          <FormControl fullWidth>
            <Select
              value={selectedValue}
              onChange={handleSelectChange}
              sx={{ maxHeight: '36px' }}
            >
              <MenuItem value="lm">Levenberg-Marquardt</MenuItem>
              <MenuItem value="de">Differential Evolution</MenuItem>
            </Select>
          </FormControl>
        </div>
      </DialogContent>
      <DialogActions className='settingsActions'>
      <Button
          // onClick={handleSave}
          size="small"
          disableElevation
          variant="contained"
          sx={{
            minWidth: '120px',
            backgroundColor: '#EEF1F4',
            color: 'black',
            textTransform: 'none',
            margin:'auto'
          }}
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}

SettingsDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  mode: PropTypes.string.isRequired,
};

export default SettingsDialog;