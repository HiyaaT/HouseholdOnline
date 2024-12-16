<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const requests = ref([]);
const user = computed(() => authStore.getUserData());

async function fetchServiceRequests() {
  try {
    const response = await fetch(`${backendURL}/api/v1/closedrequest/${user.value.id}`, {
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

onMounted(fetchServiceRequests);

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}
</script>

<template>
  <div class="table-responsive shadow-sm rounded">
    <h3 class="mb-3">Work History</h3>
    <table v-if="requests.length" class="table align-middle text-center">
      <thead class="table-primary">
        <tr>
          <th>Customer</th>
          <th>Date of review</th>
          <th>Location</th>
          <th>Rating</th>
          <th>Comment</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.customer }}</td>
          <td>{{ formatDate(request.date_of_review) }}</td> 
          <td>{{ request.address_line }}, {{ request.city }}, {{ request.pincode }}</td>
          <td>{{ request.rating }}</td>
          <td>{{ request.comment }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else class="text-center mt-3">No requests.</p> 
  </div>
</template>
