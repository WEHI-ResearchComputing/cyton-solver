import * as React from "react";
import { useRef, useState } from 'react';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { CytonClient, Parameters, ExperimentData_Output, ApiError } from "../../client"
import { VariantType, useSnackbar } from 'notistack';

const UploadButton = ({ client, onUpload }: { client: CytonClient, onUpload: (data: ExperimentData_Output) => void }) => {
  const { enqueueSnackbar } = useSnackbar();
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    // Trigger the click event of the hidden file input
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    // Handle the file selection here
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      try {
        const response = await client.root.uploadApiUploadPost({
          formData: {
            file: selectedFile
          }
        });
        enqueueSnackbar("File processed successfully", {
          variant: "success"
        });
        onUpload(response);
      } catch (error) {
        if (error instanceof ApiError) {
          enqueueSnackbar(`Error processing file: ${error.statusText}. ${error.body.detail}`, {
            variant: "error"
          });
        }
        else {
          enqueueSnackbar(`Error processing file: ${error}`, {
            variant: "error"
          });
        }
      }
    } else {
      enqueueSnackbar('No file was selected', {
        variant: "error"
      });
    }
  };

  return (
      <ListItem disablePadding>
        <ListItemButton onClick={handleButtonClick}>
          <ListItemIcon style={{ minWidth: '40px' }}>
            <UploadFileIcon />
          </ListItemIcon>
          <ListItemText primary="Upload" />
        </ListItemButton>
      {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </ListItem>
  );
};

export default UploadButton;
