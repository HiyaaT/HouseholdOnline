<template>
    <div class="container">
      <h1 class="my-4">Profile</h1>
  
      <div class="row profile-details mb-4">
        <div class="col-md-6">
          <p><strong>Name:</strong> {{ profileData.name }}</p>
          <p><strong>Email:</strong>  {{ profileData.email }}</p>
          <p  v-if="role==='professional'"><strong>Description:</strong>  {{ profileData.description }}</p>
        </div>
        <div v-if="role==='professional'"class="col-md-6">
          <p><strong>Experience:</strong>  {{ profileData.experience }} years</p>
          <p><strong>Service:</strong>  {{ profileData.service }}</p>
          <p><strong>Average Rating:</strong> {{ profileData.avg_rating }}</p>
          <p><strong>Total services completed:</strong> {{ profileData.total_ratings }}</p>
        </div>
      </div>
  
      <div class="address-section mb-4">
        <h2>Address</h2>
        <div class="row">
          <div class="col-md-6">
            <p><strong>Address Line:</strong> {{ addressData.address_line }}</p>
            <p><strong>City:</strong> {{ addressData.city }}</p>
          </div>
          <div class="col-md-6">
            <p><strong>State:</strong> {{ addressData.state }}</p>
            <p><strong>Pincode:</strong> {{ addressData.pincode }}</p>
          </div>
        </div>
        <button class="btn btn-primary" @click="showModal = true">Update Address</button>
      </div>
  
      <!-- Modal for Updating Address -->
      <div v-if="showModal" class="modal fade show" tabindex="-1" aria-labelledby="updateAddressModal" aria-hidden="true" style="display: block;">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="updateAddressModal">Update Address</h5>
              <button type="button" class="btn-close" @click="showModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateAddress(addressData.id)">
                <div class="mb-3">
                  <label for="address_line" class="form-label">Address Line:</label>
                  <input type="text" class="form-control" id="address_line" v-model="addressData.address_line" required />
                </div>
                <div class="mb-3">
                  <label for="city" class="form-label">City:</label>
                  <input type="text" class="form-control" id="city" v-model="addressData.city" required />
                </div>
                <div class="mb-3">
                  <label for="state" class="form-label">State:</label>
                  <input type="text" class="form-control" id="state" v-model="addressData.state" required />
                </div>
                <div class="mb-3">
                  <label for="pincode" class="form-label">Pincode:</label>
                  <input type="text" class="form-control" id="pincode" v-model="addressData.pincode" required />
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
                <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '@/stores/auth_store';
  import { useMessageStore } from '@/stores/message_store';
  const authStore=useAuthStore();
  const messageStore = useMessageStore();
  const backendURL = authStore.getBackendServerURL();

  const user =computed(()=>authStore.getUserData())
  const role=computed(()=>user.value.roles[0])
  
  const profileData = ref({});
  
  const addressData = ref({});
  
  const showModal = ref(false);
  
  //the button when clicked for update, updates value of show modal to true
  // Fetch user profile data
  async function fetchProfile() {
  try {
    const response = await fetch(`${backendURL}/api/v1/prof_profile/${user.value.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to fetch');
    profileData.value = await response.json();
  } catch (error) {
    console.error(error);
  }
}
  
  // Fetch user address data
  const fetchAddress = async () => {
    try {
      const response = await fetch(`${backendURL}/api/v1/get_address/${user.value.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': authStore.getToken(),
      },
    });
      if (response.ok) {
        const data = await response.json();
        addressData.value = data;
      } else {
        console.log('Failed to fetch address data');
      }
    } catch (error) {
       console.log('Error fetching address data');
    }
  };
  
  // Update the address
  const updateAddress = async (id) => {
    try {
      const response = await fetch(`${backendURL}/api/v1/get_address/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': authStore.getToken(),
        },
        body: JSON.stringify(addressData.value),
      });
  
      if (response.ok) {
        messageStore.setFlashMessage('Address updated successfully!')
        
        showModal.value = false;
        fetchAddress(); // Refresh address data
      } else {
        const errorData = await response.json();
        messageStore.setFlashMessage('Failed to update address.')
      }
    } catch (error) {
        messageStore.setFlashMessage('An error occurred. Please try again later.')
    }
  };
  
  // Fetch data when the component is mounted
  onMounted(() => {
    fetchProfile();
    fetchAddress();
  });
  </script>
  
  <style scoped>
  .modal {
    display: block;
  }
  </style>
  