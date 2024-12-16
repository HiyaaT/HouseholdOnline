<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Looking For?</h2>

    <!-- Service Cards -->
    <div class="row">
      <div v-for="service in services" :key="service.id" class="col-md-3 mb-3">
        <div 
          class="card text-center service-card" 
          @click="openModal(service)"
        >
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">Price: ${{ service.base_price }}</p> 
          </div>
        </div>
      </div>
    </div>

    <!-- Customer History Section -->
    <div class="container mt-5">
      <CustomerHistory />
    </div>

    <!-- Professional Modal -->
    <div 
      class="modal fade" 
      id="professionalModal" 
      tabindex="-1" 
      aria-labelledby="professionalModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <h6 class="text-muted">Professionals available for {{ selectedService?.name }}</h6>
            <template v-if="professionals.length > 0">
              <table class="table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>City</th>
                    <th>Average Rating</th>
                    <th>Remarks</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="professional in professionals" :key="professional.id">
                    <td>{{ professional.name }}</td>
                    <td>{{ professional.city }}</td>
                    <td>{{ professional.avg_rating }}</td>
                    <td>
                      <input 
                        type="text" 
                        v-model="remarks[professional.id]" 
                        placeholder="Enter remarks" 
                        class="form-control mb-1"
                      />
                    </td>
                    <td>
                      <button 
                        class="btn btn-primary" 
                        @click="bookService(professional.id)" 
                        :disabled="professional.isBooked"
                      >
                        {{ professional.isBooked ? 'Booked' : 'Book' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </template>
            <template v-else>
              <p>None in your area(city).</p>
            </template>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth_store';
import CustomerHistory from '@/components/CustomerHistory.vue';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();
const user = computed(() => authStore.getUserData())

// State variables
const services = ref([]);
const selectedService = ref(null);
const professionals = ref([]);
const remarks = ref({});

// Fetch services from the backend API
const fetchServices = async () => {
  try {
    const response = await fetch(`${backendURL}/api/v1/service`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
    if (!response.ok) throw new Error('Failed to fetch services');
    services.value = await response.json();
  } catch (error) {
    console.error(error);
  }
};


const openModal = async (service) => {
  selectedService.value = service;
  try {
    const response = await fetch(`${backendURL}/api/v1/profs_service/${service.name}/${user.value.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to fetch professionals.');
    professionals.value = await response.json();
    for (let professional of professionals.value) {
      professional.isBooked = await checkIfBooked(professional.id);
    }
    
    const modal = new bootstrap.Modal(document.getElementById('professionalModal'));
    modal.show();
  } catch (error) {
    console.error('Error fetching professionals:', error);
    alert('Unable to load professionals. Please try again.');
  }
};


const bookService = async (professionalId) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/service_request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify({
        service_id: selectedService.value.id,
        professional_id: professionalId,
        email: user.value.email,
        remark: remarks.value[professionalId] || '', 
      }),
    });
    if (!response.ok) throw new Error('Failed to book service.');
    const data = await response.json();
    window.location.reload();
    alert('service booked!')
    
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('professionalModal'));
    modal.hide();
  } catch (error) {
    console.error('Error booking service:', error);
    alert('Failed to book service. Please try again.');
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


fetchServices();
</script>

<style scoped>
.service-card {
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 10px;
  transition: 0.3s;
}
.service-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.table {
  margin-top: 10px;
}
</style>
