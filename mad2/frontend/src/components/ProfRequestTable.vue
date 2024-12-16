<script setup>
import { ref, onMounted, computed} from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const requests = ref([]);
const user=computed(()=>authStore.getUserData())

async function fetchServiceRequests() {
  try {
    const response = await fetch(`${backendURL}/api/v1/requested_request/${user.value.id}`, {
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

const acceptRequest = async (id) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/acceptrequest/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (response.ok) {
      alert('Request Accepted successfully!');
      fetchServiceRequests();
     
      window.location.reload();

    } else {
      console.error('Failed to accept request', response.statusText);
    }
  } catch (error) {
    console.error('Error accepting request', error);
  }
};

const rejectRequest = async (id) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/rejectrequest/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (response.ok) {
      alert('Request rejected successfully!');
      fetchServiceRequests();
     
      window.location.reload();

    } else {
      console.error('Failed to reject request', response.statusText);
    }
  } catch (error) {
    console.error('Error rejecting request', error);
  }
};
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
            <th>Customer</th>
            <th>Customer email</th>
            <th>Date of request</th>
            <th>Location to reach</th>
            <th>Accept/Reject</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">

            <td>{{ request.customer }}</td>
            <td>{{ request.email }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td>{{ request.address_line }}, {{ request.city }}, {{ request.pincode }}</td>
            <td class="table-actions">
              <button 
                class="btn btn-lilac btn-sm me-2"
                @click="acceptRequest(request.id)">
                accept
              </button>
              <button 
                class="btn btn-light-blue btn-sm"
                @click="rejectRequest(request.id)">
                reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="text-center mt-3">No requests.</p> <!-- Must be directly after v-if -->
    </div>
  </template>
  