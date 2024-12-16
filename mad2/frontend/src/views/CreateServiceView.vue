<script setup>
import { ref, computed } from 'vue';
import { useMessageStore } from '@/stores/message_store';
import { useAuthStore } from '@/stores/auth_store';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const messageStore = useMessageStore();
const router = useRouter();

// Form fields
const name = ref('');
const description = ref('');
const time_required = ref('');
const base_price = ref('');

const backendURL = computed(() => authStore.getBackendServerURL());

async function createService() {


  const input = {
    name: name.value,
    base_price: base_price.value,
    description: description.value,
    time_required: time_required.value,
  };

  try {
    const response = await fetch(`${backendURL.value}/api/v1/service`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token':authStore.getToken()
      },
      body: JSON.stringify(input),
    });

    // Check if the response is valid before parsing JSON
    if (!response.ok) {
      const errorText = await response.text(); // Get raw text to diagnose
      console.error('Error:', errorText); // Log the error text
      messageStore.setFlashMessage('Failed to create service: ' + errorText);
      return; // Stop further execution
    }

    const data = await response.json();
    messageStore.setFlashMessage(data.message || 'Service created successfully!');
    router.push('/admin-dash');
  } catch (error) {
    console.error('Request failed:', error);
    messageStore.setFlashMessage('An error occurred while submitting the form.');
  }
}
</script>

<template>
  <div class="form-container">
    <h4 class="text-center mb-4">Service Details</h4>
    <form @submit.prevent="createService">
      <div class="mb-3">
        <label for="serviceName" class="form-label">Service Name</label>
        <input
          type="text"
          class="form-control"
          id="serviceName"
          v-model="name"
          required
        />
      </div>

      <div class="mb-3">
        <label for="basePrice" class="form-label">Base Price ($)</label>
        <input
          type="number"
          class="form-control"
          id="basePrice"
          v-model="base_price"
          required
        />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          class="form-control"
          id="description"
          rows="3"
          v-model="description"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="timeRequired" class="form-label">Time Required</label>
        <input
          type="text"
          class="form-control"
          id="timeRequired"
          v-model="time_required"
          required
        />
      </div>

      <div class="d-grid">
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>
</template>
