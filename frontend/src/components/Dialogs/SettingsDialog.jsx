import PropTypes from 'prop-types';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { useTheme } from '@mui/material/styles';

function SettingsDialog({ open, onClose }) {
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
        <p>Text</p>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}

SettingsDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default SettingsDialog;