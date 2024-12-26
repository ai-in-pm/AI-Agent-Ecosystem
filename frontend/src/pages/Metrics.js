import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Metrics() {
  const [loading, setLoading] = useState(true);
  const [metricsData, setMetricsData] = useState({});
  const [selectedAgent, setSelectedAgent] = useState('');
  const [selectedMetric, setSelectedMetric] = useState('');

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get('http://localhost:8000/metrics');
        setMetricsData(response.data);
        if (Object.keys(response.data).length > 0) {
          setSelectedAgent(Object.keys(response.data)[0]);
        }
      } catch (error) {
        console.error('Error fetching metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedAgent && metricsData[selectedAgent]?.metrics) {
      const metrics = Object.keys(metricsData[selectedAgent].metrics);
      if (metrics.length > 0) {
        setSelectedMetric(metrics[0]);
      }
    }
  }, [selectedAgent, metricsData]);

  const getChartData = () => {
    if (!selectedAgent || !selectedMetric) return null;

    const metricData = metricsData[selectedAgent]?.metrics?.[selectedMetric];
    if (!metricData) return null;

    // Convert metric data into chart format
    // This is a simplified example - adjust based on your actual data structure
    const labels = Object.keys(metricData);
    const data = Object.values(metricData);

    return {
      labels,
      datasets: [
        {
          label: selectedMetric,
          data,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Agent Metrics Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
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
      <Typography variant="h4" gutterBottom>
        Metrics
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Select Agent</InputLabel>
            <Select
              value={selectedAgent}
              label="Select Agent"
              onChange={(e) => setSelectedAgent(e.target.value)}
            >
              {Object.keys(metricsData).map((agent) => (
                <MenuItem key={agent} value={agent}>
                  {agent}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Select Metric</InputLabel>
            <Select
              value={selectedMetric}
              label="Select Metric"
              onChange={(e) => setSelectedMetric(e.target.value)}
            >
              {selectedAgent &&
                Object.keys(metricsData[selectedAgent]?.metrics || {}).map(
                  (metric) => (
                    <MenuItem key={metric} value={metric}>
                      {metric}
                    </MenuItem>
                  )
                )}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              {getChartData() ? (
                <Line data={getChartData()} options={chartOptions} />
              ) : (
                <Typography variant="body1" align="center">
                  No metric data available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Raw Metrics Data
              </Typography>
              <pre style={{ overflow: 'auto' }}>
                {JSON.stringify(metricsData, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Metrics;
