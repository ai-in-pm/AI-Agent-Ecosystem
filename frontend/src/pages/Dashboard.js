import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import {
  Timeline,
  SmartToy,
  Speed,
  Memory,
} from '@mui/icons-material';
import axios from 'axios';

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    activeAgents: 0,
    totalTasks: 0,
    systemHealth: 0,
    resourceUsage: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthResponse, metricsResponse] = await Promise.all([
          axios.get('http://localhost:8000/health'),
          axios.get('http://localhost:8000/metrics'),
        ]);

        // Process the data
        const agents = Object.keys(healthResponse.data).length;
        const metrics = metricsResponse.data;
        
        setStats({
          activeAgents: agents,
          totalTasks: Object.values(metrics).reduce(
            (acc, agent) => acc + (agent.metrics?.length || 0),
            0
          ),
          systemHealth: 98, // Example value
          resourceUsage: 45, // Example value
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const statCards = [
    {
      title: 'Active Agents',
      value: stats.activeAgents,
      icon: <SmartToy sx={{ fontSize: 40, color: 'primary.main' }} />,
    },
    {
      title: 'Total Tasks',
      value: stats.totalTasks,
      icon: <Timeline sx={{ fontSize: 40, color: 'secondary.main' }} />,
    },
    {
      title: 'System Health',
      value: `${stats.systemHealth}%`,
      icon: <Speed sx={{ fontSize: 40, color: 'success.main' }} />,
    },
    {
      title: 'Resource Usage',
      value: `${stats.resourceUsage}%`,
      icon: <Memory sx={{ fontSize: 40, color: 'warning.main' }} />,
    },
  ];

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        {statCards.map((card) => (
          <Grid item xs={12} sm={6} md={3} key={card.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                p: 2,
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  mb: 2,
                }}
              >
                {card.icon}
              </Box>
              <CardContent>
                <Typography
                  variant="h4"
                  component="div"
                  align="center"
                  gutterBottom
                >
                  {card.value}
                </Typography>
                <Typography
                  variant="subtitle1"
                  color="text.secondary"
                  align="center"
                >
                  {card.title}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Dashboard;
