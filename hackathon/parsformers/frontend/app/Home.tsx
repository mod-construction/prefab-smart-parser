'use client';

import { Box,Button, Typography, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import { useState } from 'react';
// import LoadingScreen from './LoadingScreen'; // Import the LoadingScreen component
import { validatePrefabElement } from './services/validation';
import type { ChangeEvent } from 'react';
import CircularProgress from '@mui/material/CircularProgress'; // Import a loader component

export const maxDuration = 30;

export default function Home() {
  // const [loading, setLoading] = useState<boolean>(true); // Loading state
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [dialogMessage, setDialogMessage] = useState<string>('');
  const [serverResponse, setServerResponse] = useState<string>(''); // New state for server response
  const [loading, setLoading] = useState<boolean>(false); // New state for loading

  // useEffect(() => {
  //   const timer = setTimeout(() => {
  //     setLoading(false); // Set loading to false after 3 seconds
  //   }, 3000);

  //   return () => clearTimeout(timer); // Cleanup the timer on component unmount
  // }, []);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    setLoading(true); // Set loading to true before processing
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const fileContent = reader.result;
        console.log('Encoded file content:',  JSON.stringify({ 'pdf_content':fileContent }));

        // Send the file content to the server
        fetch('http://127.0.0.1:8080/process_pdf', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ fileContent }),
        })
        .then(response => response.json())
        .then(data => {
          console.log('Server response:', data);
          setServerResponse(data); // Update state with server response
        })
        .catch(error => {
          console.error('Error sending file:', error);
          setDialogMessage('Error sending file to server');
          setDialogOpen(true);
        })
        .finally(() => {
          setLoading(false); // Set loading to false when request completes
        });
        // You can now use the encoded file content as needed
      };

      reader.onerror = (error) => {
        console.error('Error reading file:', error);
      };

      reader.readAsDataURL(file); // This will encode the file as a base64 string
    } else {
      setLoading(false); // Ensure loading is false if no file is selected
    }
  };

  const handleButtonClick = () => {
    document.getElementById('fileInput')?.click();
  };

  const handleValidation = (json: any) => {
    const result = validatePrefabElement(json);
    if (result.success) {
      //console.log(result.data)
      setDialogMessage(`Validation successful!`); // Include server response
    } else {
      setDialogMessage(`Validation failed: ${result.error}`); // Include server response ? \nServer Response: ${serverResponse}
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  // if (loading) {
  //   return <LoadingScreen message={'Parser'}/>; // Display the loading screen if loading is true
  // }

  return (
    <>
      <Box
        sx={{
          width: '100dvw',
          overflow: 'auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'white',
          minHeight: '90dvh',
          backgroundImage: 'radial-gradient(lightgray 1px, transparent 1px)',
          backgroundSize: '30px 30px',
        }}
      >
        {!serverResponse ? ( // Display initial content if no server response
        <Box sx={{ display: 'flex', flexDirection:'column', alignItems: 'center', mt: 2, width: '100%' }}>
          <Typography variant="overline" sx={{ color:'black', marginBottom:'60px', width:'600px', textAlign:'center', lineHeight:'1.5'}}>
            Parser is the project created during Open source construction hackathon in Munich, using Langchain and LLM.
          </Typography>
          <input
            id="fileInput"
            type="file"
            accept=".pdf"
            style={{ display: 'none' }}
            onChange={handleFileChange}
            disabled={loading} // Optionally disable input while loading
          />
          <Button
            variant="contained"
            color="primary"
            sx={{
              backgroundColor: 'black',
              color: 'white',
              borderRadius: '30px',
              mb: 2
            }}
            onClick={handleButtonClick}
          >
            Upload PDF
          </Button>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 2, width: '100%' }}>
            {loading && <CircularProgress size={24} sx={{ color: 'black' }} thickness={6}/>}
          </Box>

          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 2, width: '100%' }}>
            <Typography variant="caption" sx={{ color: 'black', marginTop: '0px' }}>
              Uploaded pdf is processed using LLM and matched with the library of MOD components
            </Typography>
          </Box>
        </Box>
        ) : ( // Display server response and validate button if response is received
          <Box sx={{ display: 'flex', flexDirection:'column', alignItems: 'center', mt: 2, width: '100%', borderRadius:'10px', p:2 }}>
            <Box sx={{ height: '400px', overflow: 'auto', flexGrow: 1, border:'1px solid black', borderRadius:'10px', width:'80%', color:'black' }}>
              <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                {JSON.stringify(serverResponse, null, 2)}
              </pre>
            </Box>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleValidation(serverResponse)}
              sx={{
                backgroundColor: 'black',
                color: 'white',
                borderRadius: '30px',
                marginTop: '20px',
                mb: 2,  // Add margin bottom of 2 units (16px)
                mr: 2   // Add margin right of 2 units (16px) for spacing
              }}
            >
              Validate
            </Button>
          </Box>
        )}
      </Box>
      <Box sx={{ height: '60px', marginTop: '60px' }}>
        {loading && (
          <Button
            variant="contained"
            color="primary"
            disabled
            sx={{
              backgroundColor: 'black',
              color: 'white',
              borderRadius: '30px',
              mb: 2  // Add margin bottom of 2 units (16px)
            }}
          >
            Processing...
          </Button>
        )}
      </Box>

      <Dialog open={dialogOpen} onClose={handleCloseDialog}>
        <DialogTitle sx={{ textAlign: 'center' }}><Typography variant="body1">Result</Typography></DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {dialogMessage === 'Validation successful!' ? (
            <>
              <Typography sx={{ textAlign: 'center' }}>{dialogMessage}</Typography>
              <ThumbUpIcon sx={{ color: 'success.main' }} />
            </>
          ) : (
            <Typography sx={{ textAlign: 'center', whiteSpace: 'pre-line' }}>{dialogMessage}</Typography>
          )}
        </DialogContent>
        <DialogActions sx={{ justifyContent: 'center', marginBottom:'10px' }}>
          <Button
            size='small'
            onClick={handleCloseDialog}
            sx={{
              backgroundColor: 'black',
              color: 'white',
              borderRadius: '20px',
              pddingBottom: '20px',
              '&:hover': {
                backgroundColor: 'darkgray',
              },
            }}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
