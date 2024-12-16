<template>
  <div id="app" class="container mt-2">
    <h3 class="mb-3">Service Management</h3>

    <!-- Service Table -->
    <div class="table-responsive shadow-sm rounded">
      <table class="table align-middle text-center">
        <thead class="table-primary">
          <tr>
            <th>Name</th>
            <th>Base Price</th>
            <th>Time Required</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(service, index) in services" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.base_price }}</td>
            <td>{{ service.time_required }}</td>
            <td>{{ service.description }}</td>
            <td class="table-actions">
              <button 
                class="btn btn-lilac btn-sm me-2"
                @click="openUpdateModal(service.id)">
                Update
              </button>
              <button 
                class="btn btn-light-blue btn-sm"
                @click="deleteService(service.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Update Service Modal -->
    <div 
      class="modal fade" 
      id="updateModal" 
      tabindex="-1" 
      aria-labelledby="updateModalLabel" 
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="updateModalLabel">Update Service</h5>
            <button 
              type="button" 
              class="btn-close" 
              data-bs-dismiss="modal" 
              aria-label="Close">
            </button>
          </div>
          <form @submit.prevent="updateService">
            <div class="modal-body">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input 
                  v-model="selectedService.name" 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  disabled />
              </div>
              <div class="mb-3">
                <label for="price" class="form-label">Base Price</label>
                <input 
                  v-model="selectedService.base_price" 
                  type="number" 
                  class="form-control" 
                  id="price" 
                  required />
              </div>
              <div class="mb-3">
                <label for="time" class="form-label">Time Required</label>
                <input 
                  v-model="selectedService.time_required" 
                  type="text" 
                  class="form-control" 
                  id="time" 
                  required />
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea 
                  v-model="selectedService.description" 
                  class="form-control" 
                  id="description" 
                  required>
                </textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                type="button" 
                class="btn btn-secondary" 
                data-bs-dismiss="modal">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <!--hello-->
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();

const services = ref([]);
const selectedService = ref({});

async function fetchServices() {
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
}

const openUpdateModal = (serviceId) => {
  const service = services.value.find(s => s.id === serviceId);
  selectedService.value = { ...service };
  const modal = new bootstrap.Modal(document.getElementById('updateModal'));
  modal.show();
};

const updateService = async () => {
  try {
    const response = await fetch(`${backendURL}/api/v1/services/${selectedService.value.id}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify(selectedService.value),
    });

    if (response.ok) {
      alert('Service updated successfully!');
      fetchServices();
      const modalElement = document.getElementById('updateModal');
      const modalInstance = bootstrap.Modal.getInstance(modalElement);
      modalInstance.hide();
    } else {
      console.error('Failed to update service:', response.statusText);
    }
  } catch (error) {
    console.error('Error updating service:', error);
  }
};

const deleteService = async (id) => {
  if (!confirm('Are you sure you want to delete this service?')) return;

  try {
    const response = await fetch(`${backendURL}/api/v1/services/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (response.ok) {
      alert('Service deleted successfully!');
      fetchServices();
    } else {
      console.error('Failed to delete service:', response.statusText);
    }
  } catch (error) {
    console.error('Error deleting service:', error);
  }
};

onMounted(fetchServices);
</script>
