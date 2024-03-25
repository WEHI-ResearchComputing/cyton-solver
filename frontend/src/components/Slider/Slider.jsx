import * as React from 'react';
import PropTypes from 'prop-types';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Slider from '@mui/material/Slider';
import MuiInput from '@mui/material/Input';
import { useController, useForm } from "react-hook-form";

// Styling for Text Field
const Input = styled(MuiInput)`
  width: 52px;
`;

function InputSlider( {label}) {
  const controller = useController({
    name: label
  }).field;
  const min = 0;
  const max = 100;
  const step = 0.01;
  // We have to insert a fake default value so that React doesn't think it's an uncontrolled component
  const value = controller.value || 0;
  const onChange = controller.onChange;

  return (
    <Box sx={{ padding: '8px' }}>
      <Typography id="input-slider" gutterBottom>
        {label}
      </Typography>
      <Grid container spacing={2} alignItems="center">
        <Grid item>
        </Grid>
        <Grid item xs>
          <Slider
            value={value}
            onChange={onChange}
            aria-labelledby="input-slider"
            step={step}
            min={min}
            max={max}
          />
        </Grid>
        <Grid item>
          <Input
            value={value}
            onChange={onChange}
            size="small"
            inputProps={{
              step: step,
              min: min,
              max: max,
              type: 'number',
              'aria-labelledby': 'input-slider',
            }}
          />
        </Grid>
      </Grid>
    </Box>
  );
}

InputSlider.propTypes = {
  label: PropTypes.string.isRequired,
  min: PropTypes.number.isRequired,
  max: PropTypes.number.isRequired,
  step: PropTypes.number.isRequired,
};

export default InputSlider;
