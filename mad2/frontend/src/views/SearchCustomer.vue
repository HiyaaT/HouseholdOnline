<template>
  <div id="app" class="container mt-4">
  
    <!-- Search Form Section -->
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="input-group mb-3">
          <h3 class="input-group-text">Search Professional by</h3>
        </div>
  
        <!-- Professional Search Fields -->
        <div>
          <input
            v-model="searchFields.name"
            type="text"
            class="form-control mb-2"
            placeholder="Enter Professional Name"
          />
          <input
            v-model="searchFields.service"
            type="text"
            class="form-control mb-2"
            placeholder="Enter Service Provided"
          />
          <input
            v-model="searchFields.city"
            type="text"
            class="form-control mb-2"
            placeholder="Enter City"
          />
          <div class="d-flex justify-content-end">
            <button class="btn btn-outline-primary me-2" @click="searchProfessionalByInputs">
              Search by Inputs
            </button>
            <button class="btn btn-outline-secondary" @click="searchNearProfessionals">
              Search Professionals near me
            </button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Results Section -->
    <div v-if="results.length" class="container mt-5">
      <h4 class="text-center">Search Results</h4>
      <table class="table table-hover mt-3">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>City</th>
            <th>Description</th>
            <th>Experience</th>
            <th>Average Rating</th>
            <th>Service</th>
            <th>book</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in results" :key="result.id">
            <td>{{ result.id }}</td>
            <td>{{ result.name }}</td>
            <td>{{ result.city }}</td>
            <td>{{ result.description }}</td>
            <td>{{ result.experience }} years</td>
            <td>{{ result.avg_rating }}</td>
            <td>{{ result.service }}</td>
            <td>
              <button 
                class="btn btn-primary" 
                @click="bookService(result.id, result.service_id)" 
                :disabled="result.isBooked">
                {{ result.isBooked ? 'Booked' : 'Book' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  
    <div v-else-if="!results.length && searchPerformed" class="text-center mt-5">
      <p>No results found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth_store';
import { useMessageStore } from '@/stores/message_store';

const authStore = useAuthStore();
const messageStore=useMessageStore()
const backendURL = authStore.getBackendServerURL();
const user = computed(() => authStore.getUserData())

const searchFields = ref({ name: '', city: '', service: '' });
const results = ref([]);
const searchPerformed = ref(false);

const resetSearch = () => {
  searchFields.value = { name: '', city: '', service: '' };
  results.value = [];
  searchPerformed.value = false;
};


const searchProfessionalByInputs = async () => {
  const { name, service, city } = searchFields.value;
  const apiUrl = `${backendURL}/api/v1/professional_input_based?name=${name}&service=${service}&city=${city}`;
  await fetchData(apiUrl);
};


const searchNearProfessionals = async () => {
  const apiUrl = `${backendURL}/api/v1/nearprofessionals/${user.value.id}`;
  await fetchData(apiUrl);
};


const fetchData = async (apiUrl) => {
  searchPerformed.value = true;
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    
    
    for (let professional of data) {
      professional.isBooked = await checkIfBooked(professional.id); 
    }

    results.value = data;
    console.log(data);
  } catch (error) {
    console.error('Error fetching data:', error);
    results.value = [];
  }
};


const checkIfBooked = async (professionalId) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/isbooked/${user.value.id}/${professionalId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    return data.check; 
  } catch (error) {
    console.error('Error checking if booked:', error);
    return false; 
  }
};


const bookService = async (professionalId, service_id) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/service_request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify({
        service_id: service_id,
        professional_id: professionalId,
        email: user.value.email,
      }),
    });
    if (!response.ok) throw new Error('Failed to book service.');
    const data = await response.json();
    window.location.reload()
    alert(data.message || 'Service booked successfully!');
  } catch (error) {
    console.error('Error booking service:', error);
    alert('Failed to book service. Please try again.');
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}

input {
  margin-bottom: 10px;
}
</style>
