<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const requests = ref([]);

async function fetchServiceRequests() {
  try {
    const response = await fetch(`${backendURL}/api/v1/allservicerequest`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to fetch service requests');
    requests.value = await response.json();
  } catch (error) {
    console.error(error);
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}
onMounted(fetchServiceRequests);
</script>

<template>
    <div class="table-responsive shadow-sm rounded">
      <h3 class="mb-3">All Service Requests</h3>
      <table v-if="requests.length" class="table align-middle text-center">
        <thead class="table-primary">
          <tr>
            <th>Service of</th>
            <th>Provided by</th>
            <th>Provided to</th>
            <th>Date of request</th>
            <th>Date of completion</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.service }}</td>
            <td>{{ request.professional }}</td>
            <td>{{ request.customer }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td v-if="request.date_of_completion">{{ formatDate(request.date_of_completion) }}</td>
            <td v-else>null</td>
            <td>{{ request.status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="text-center mt-3">No requests.</p> <!-- Must be directly after v-if -->
    </div>
  </template>
  