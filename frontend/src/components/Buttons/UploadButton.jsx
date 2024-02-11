import { useRef } from 'react';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import UploadFileIcon from '@mui/icons-material/UploadFile';

const UploadButton = () => {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    // Trigger the click event of the hidden file input
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    // Handle the file selection here
    const selectedFile = event.target.files[0];
    // console.log('Selected file:', selectedFile);

    if (selectedFile) {
      try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        // TODO: Replace endpoint URL
        const response = await fetch('http://localhost:9999/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const responseData = await response.json();
          // console.log('Response data:', responseData);
          localStorage.setItem('uploadedData', JSON.stringify(responseData));
          alert('File uploaded successfully!')
        }
      } catch (error) {
        alert('Error uploading file! Try again!');
      }
    } else {
      alert('No file was selected.');
    }
  };

  return (
    <List>
      <ListItem disablePadding>
        <ListItemButton onClick={handleButtonClick}>
          <ListItemIcon style={{ minWidth: '40px' }}>
            <UploadFileIcon />
          </ListItemIcon>
          <ListItemText primary="Upload" />
        </ListItemButton>
      </ListItem>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </List>
  );
};

export default UploadButton;