import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import axios from 'axios';

function Agents() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const fetchAgents = async () => {
    try {
      const [healthResponse, metricsResponse] = await Promise.all([
        axios.get('http://localhost:8000/health'),
        axios.get('http://localhost:8000/metrics'),
      ]);

      const agentData = Object.entries(healthResponse.data).map(([name, health]) => ({
        name,
        health,
        metrics: metricsResponse.data[name] || {},
        status: health.status,
      }));

      setAgents(agentData);
    } catch (error) {
      console.error('Error fetching agent data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = () => {
    setLoading(true);
    fetchAgents();
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'initialized':
        return 'success';
      case 'idle':
        return 'info';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Agents</Typography>
        <IconButton onClick={handleRefresh} color="primary">
          <RefreshIcon />
        </IconButton>
      </Box>

      <Grid container spacing={3}>
        {agents.map((agent) => (
          <Grid item xs={12} sm={6} md={4} key={agent.name}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {agent.name}
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={() => {
                      setSelectedAgent(agent);
                      setDialogOpen(true);
                    }}
                  >
                    <InfoIcon />
                  </IconButton>
                </Box>
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip
                    label={agent.status}
                    color={getStatusColor(agent.status)}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Last Active: {new Date(agent.health.last_active).toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Uptime: {Math.round(agent.health.uptime)} seconds
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedAgent && (
          <>
            <DialogTitle>{selectedAgent.name} Details</DialogTitle>
            <DialogContent>
              <Typography variant="h6" gutterBottom>
                Metrics
              </Typography>
              <pre style={{ overflow: 'auto' }}>
                {JSON.stringify(selectedAgent.metrics, null, 2)}
              </pre>
              <Typography variant="h6" gutterBottom>
                Health
              </Typography>
              <pre style={{ overflow: 'auto' }}>
                {JSON.stringify(selectedAgent.health, null, 2)}
              </pre>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setDialogOpen(false)}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
}

export default Agents;
