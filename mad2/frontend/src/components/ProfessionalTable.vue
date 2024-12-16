<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const professionals = ref([]);

async function fetchProfessionals() {
  try {
    const response = await fetch(`${backendURL}/api/v1/unapproved_professionals`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to fetch professionals');
    professionals.value = await response.json();
  } catch (error) {
    console.error(error);
  }
}

const approveProfessional = async (id) => {
  if (!confirm('Are you sure you want to approve this professional?')) return;

  try {
    const response = await fetch(`${backendURL}/api/v1/approve/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (response.ok) {
      alert('Professional approved successfully!');
      fetchProfessionals();
    } else {
      console.error('Failed to approve professional:', response.statusText);
    }
  } catch (error) {
    console.error('Error approving professional:', error);
  }
};

onMounted(fetchProfessionals);
</script>

<template>
  <div class="table-responsive shadow-sm rounded">
    <h3 class="mb-3">Unapproved Professionals</h3>
    <table v-if="professionals.length" class="table align-middle text-center">
      <thead class="table-primary">
        <tr>
          <th>Name</th>
          <th>Experience</th>
          <th>Service</th>
          <th>City</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>{{ professional.name }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.service }}</td>
          <td>{{ professional.city }}</td>
          <td>
            <button 
              class="btn btn-success btn-sm"
              @click="approveProfessional(professional.id)">
              Approve
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="text-center mt-3">No unapproved professionals found.</p>
  </div>
</template>
