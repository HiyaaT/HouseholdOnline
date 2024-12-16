<script setup>
import { ref, onMounted, computed } from 'vue';
import ProfRequestTable from '@/components/ProfRequestTable.vue';
import ProfHistoryTable from '@/components/ProfHistoryTable.vue';
import ProfessionalOngoing from '@/components/ProfessionalOngoing.vue';
import { useAuthStore } from '@/stores/auth_store'; 
const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();
const user = computed(() => authStore.getUserData());

// State variables
const serviceId = ref(user.value.service_id);
const showModal = ref(false);
const services = ref([]);
const selectedServiceId = ref(null);

// Fetch available services
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
    console.error('Error fetching services:', error);
  }
};

// Update professional's service_id
const updateService = async () => {
  try {
    const response = await fetch(`${backendURL}/api/v1/setservice/${user.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ service_id: selectedServiceId.value }),
    });

    if (response.ok) {
      alert('Service updated successfully!');
      showModal.value = false;
      serviceId.value = selectedServiceId.value;
    } else {
      throw new Error('Failed to update service');
    }
  } catch (error) {
    console.error('Error updating service:', error);
  }
};


onMounted(() => {
  if (serviceId.value === 0) {
    showModal.value = true;
    fetchServices();
  }
});
</script>

<template>
  <div class="container mt-5">
    <ProfRequestTable />
  </div>
  <div class="container mt-5">
    <ProfessionalOngoing />
  </div>
  <div class="container mt-5">
    <ProfHistoryTable />
  </div>

  <!-- Service Selection Modal -->
  <div v-if="showModal" class="modal d-block" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Select Your Service</h5>
        </div>
        <div class="modal-body">
          <select v-model="selectedServiceId" class="form-select">
            <option disabled value="">Please select a service</option>
            <option v-for="service in services" :key="service.id" :value="service.id">
              {{ service.name }}
            </option>
          </select>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" @click="updateService" :disabled="!selectedServiceId">
            Save Service
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Backdrop -->
  <div v-if="showModal" class="modal-backdrop fade show"></div>
</template>

