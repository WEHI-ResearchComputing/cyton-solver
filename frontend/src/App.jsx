import NavigationBar from './components/NavigationBar/NavigationBar';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import defaultTheme from "./themes/defaultTheme";
import CssBaseline from '@mui/material/CssBaseline';
import { SnackbarProvider } from 'notistack';

const theme = createTheme(defaultTheme);

function App() {
  return (
    <SnackbarProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="App">
          <div className="NavigationBar">
            <NavigationBar />
          </div>
        </div>
      </ThemeProvider>
    </SnackbarProvider>
  );
}

export default App;
