import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { AppBar, Toolbar, Typography, Container, Paper, Button, Box, Stack, Alert, LinearProgress, Chip, Divider, List, ListItem, ListItemText } from '@mui/material';
import ShieldOutlined from '@mui/icons-material/ShieldOutlined';
import CloudUploadOutlined from '@mui/icons-material/CloudUploadOutlined';
import VideoFileOutlined from '@mui/icons-material/VideoFileOutlined';
import WarningAmberOutlined from '@mui/icons-material/WarningAmberOutlined';
import axios from 'axios';
import './style.css';
const theme = createTheme({ palette:{ mode:'light', primary:{main:'#2563eb'}, background:{default:'#f4f7fb'} }, typography:{fontFamily:'Inter, system-ui, Arial'} , shape:{borderRadius:14}});
const configuredApiHost = import.meta.env.VITE_API_HOST;
const apiBaseUrl = configuredApiHost
 ? (configuredApiHost.startsWith('http') ? configuredApiHost : `https://${configuredApiHost}`)
 : 'http://localhost:8000';
function App(){
 const [file,setFile]=useState(null), [busy,setBusy]=useState(false), [result,setResult]=useState(null), [error,setError]=useState('');
 const analyze=async()=>{ if(!file)return; setBusy(true);setError('');setResult(null); const form=new FormData();form.append('video',file);try{const r=await axios.post(`${apiBaseUrl}/api/analyze`,form,{headers:{'Content-Type':'multipart/form-data'}});setResult(r.data)}catch(e){setError(e.response?.data?.detail||'Could not reach backend. Start FastAPI on port 8000 and try again.')}finally{setBusy(false)}};
 return <><AppBar position="static" elevation={0} color="inherit"><Toolbar><ShieldOutlined color="primary" sx={{mr:1}}/><Typography variant="h6" fontWeight={800} color="text.primary">Sentinel AI</Typography><Box sx={{flex:1}}/><Chip label="Video analysis" color="primary" variant="outlined"/></Toolbar></AppBar>
 <Container maxWidth="md" sx={{py:5}}><Stack spacing={3}><Box><Typography variant="h4" fontWeight={800}>Suspicious Activity Detection</Typography><Typography color="text.secondary" sx={{mt:1}}>Upload surveillance footage for AI-assisted review.</Typography></Box>
 <Paper sx={{p:{xs:2,sm:4}}}><Stack spacing={2} alignItems="center"><Box className="upload-icon"><CloudUploadOutlined fontSize="large" color="primary"/></Box><Typography variant="h6" fontWeight={700}>Upload a video</Typography><Typography color="text.secondary" textAlign="center">Supported formats: MP4, AVI, MOV, MKV</Typography><Button component="label" variant="outlined">Choose video<input hidden type="file" accept="video/mp4,video/avi,video/quicktime,video/x-matroska,.avi,.mkv" onChange={e=>{setFile(e.target.files?.[0]||null);setResult(null);setError('')}}/></Button>{file&&<Alert severity="info" icon={<VideoFileOutlined/>}>{file.name} · {(file.size/1024/1024).toFixed(1)} MB</Alert>}<Button disabled={!file||busy} onClick={analyze} variant="contained" size="large">{busy?'Analyzing…':'Upload and analyze'}</Button>{busy&&<LinearProgress sx={{width:'100%'}}/>}</Stack></Paper>
 {error&&<Alert severity="error">{error}</Alert>}
 {result&&<Paper sx={{p:3}}><Stack spacing={2}><Stack direction="row" alignItems="center" spacing={1}><VideoFileOutlined color="primary"/><Typography variant="h6" fontWeight={700}>Analysis summary</Typography><Box sx={{flex:1}}/><Chip label={result.summary?.label||'Analyzed'} color={result.summary?.label==='SUSPICIOUS'?'warning':'success'}/></Stack><Divider/><Typography><b>File:</b> {result.filename}</Typography><Typography><b>Duration:</b> {result.metadata?.duration_seconds??'Unknown'} seconds</Typography><Typography><b>Resolution:</b> {result.metadata?.width} × {result.metadata?.height}</Typography><Typography><b>Suspicious windows:</b> {result.summary?.clips_suspicious??0} of {result.summary?.clips_total??0} · <b>Confidence:</b> {((result.summary?.confidence||0)*100).toFixed(1)}%</Typography><Alert severity={result.summary?.label==='SUSPICIOUS'?'warning':'success'} icon={<WarningAmberOutlined/>}>{result.message}</Alert>{result.detections?.length>0?<Box><Typography fontWeight={700}>Flagged intervals</Typography><List dense>{result.detections.map(clip=><ListItem key={clip.clip_index} disableGutters><ListItemText primary={`${clip.start_seconds.toFixed(2)}–${clip.end_seconds.toFixed(2)} seconds`} secondary={`Suspicious probability: ${(clip.suspicious_probability*100).toFixed(1)}%`}/></ListItem>)}</List></Box>:<Typography color="text.secondary">No clip exceeded the suspicious-activity threshold. This result is an AI-assisted screening, not proof of criminal activity.</Typography>}</Stack></Paper>}
 <Typography variant="caption" color="text.secondary">Prototype · AI output should be reviewed by a human and is not proof of criminal activity.</Typography></Stack></Container></>;
}
createRoot(document.getElementById('root')).render(<ThemeProvider theme={theme}><App/></ThemeProvider>);
