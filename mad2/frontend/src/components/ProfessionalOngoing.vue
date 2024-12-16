<script setup>
import { ref, onMounted, computed} from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const requests = ref([]);
const user=computed(()=>authStore.getUserData())

async function fetchServiceRequests() {
  try {
    const response = await fetch(`${backendURL}/api/v1/acceptedrequest/${user.value.id}`, {
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

const closeServiceRequestStatus = async (requestId) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/closerequestp/${requestId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to update service request status.');
    fetchServiceRequests()
  } catch (error) {
    console.error('Error updating service request status:', error);
    alert('Failed to update service request status. Please try again.');
  }
};


onMounted(fetchServiceRequests);
</script>

<template>
    <div class="table-responsive shadow-sm rounded">
      <h3 class="mb-3">Work</h3>
      <table v-if="requests.length" class="table align-middle text-center">
        <thead class="table-primary">
          <tr>
            <th>Customer</th>
            <th>Email</th>
            <th>Location</th>
            <th>remark</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">

            <td>{{ request.customer }}</td>
            <td>{{ request.email }}</td>
            <td>{{ request.address_line }}, {{ request.city }}, {{ request.pincode }}</td>
            <td>{{ request.remarks }}</td>
            <td><button class="btn btn-light-green btn-sm me-2" @click="closeServiceRequestStatus(request.id)">close</button></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="text-center mt-3">No ongoing/accepted work.</p> <!-- Must be directly after v-if -->
    </div>
  </template>
  