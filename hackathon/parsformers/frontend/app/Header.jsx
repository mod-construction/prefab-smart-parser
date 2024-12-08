import React from 'react';
import { Link, Stack, Box } from '@mui/material';

export async function Header() {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 bg-white">
        <Link href="/" rel="nofollow" variant="overline" sx={{ color: 'black', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}>
          <Box sx={{width:'20px',height:'20px',backgroundColor:'black',color:'white', border:'3px solid black', borderRadius:'2px'}}/>
        </Link>
        <Stack direction="row" spacing={2}>

          <Link href="/" variant="overline" sx={{ color: 'black', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}>
            Langchain
          </Link>
          <Link href="/assistant" className="font-small" variant="overline" sx={{ color: 'black', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}>
            Assistant
          </Link>
          <Link href="/three" className="font-small" variant="overline" sx={{ color: 'black', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}>
            3D model
          </Link>
        </Stack>
        <Box sx={{width:'20px',height:'20px',color:'white', border:'2px solid black', borderRadius:'2px'}}/>
    </header>
  )
}
