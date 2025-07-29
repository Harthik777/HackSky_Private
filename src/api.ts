// src/api.ts

const API_BASE_URL = '/api';

/**
 * A helper function to handle fetch requests and standardized error handling.
 * @param endpoint The API endpoint to call (e.g., '/alerts').
 * @returns The JSON response from the API.
 * @throws An error if the network response is not ok.
 */
async function apiFetch(endpoint: string) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (!response.ok) {
    const errorInfo = await response.text();
    throw new Error(`API Error: ${response.status} ${response.statusText} on ${endpoint} - ${errorInfo}`);
  }
  return response.json();
}

// --- Exported API functions for each component's data needs ---

export const fetchAlerts = () => apiFetch('/alerts');

export const fetchSystemStatus = () => apiFetch('/system-status');

export const fetchPowerData = () => apiFetch('/power-data');

export const fetchAttackAnalysis = () => apiFetch('/attack-analysis');

export const fetchStatistics = () => apiFetch('/statistics');

export const fetchHealth = () => apiFetch('/health');
