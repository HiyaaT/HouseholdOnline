<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth_store'; // Import Pinia store
import { useMessageStore } from '@/stores/message_store';
import { useRouter } from 'vue-router';

const name = ref('');
const email = ref('');
const password = ref('');
const confirm_password = ref('');
const role = ref('');
const service_id = ref('');
const description = ref('');
const experience = ref('');
const address_line = ref('');
const city = ref('');
const state = ref('');
const pincode = ref('');

// Stores and router setup
const authStore = useAuthStore();
const messageStore = useMessageStore();
const router = useRouter();

const backendURL = computed(() => authStore.getBackendServerURL());

const check_for_email=ref('')

function check_email(){
  const input_data={
    email:email.value,
  }

  fetch(`${backendURL.value}/api/v1/valid_user`,{
    method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Acess-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(input_data)
  }).then(
    response=> response.json()
  ).then(
    (data)=> {
      check_for_email.value=data.message;
    }
  )
}

function valid_input() {
  if (password.value !== confirm_password.value) {
    messageStore.setFlashMessage('Password and Confirm Password should be the same');
    return false;
  }
  return true;
}

async function register(input_data) {
  try {
    const response = await fetch(`${backendURL.value}/api/v1/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(input_data),
    });

    const data = await response.json();
    if (!response.ok) {
      return { status: false, message: data.message };
    }
    return { status: true, message: data.message };
  } catch (error) {
    console.error(error);
    return { status: false, message: 'Oops! Something went wrong' };
  }
}

async function onSubmit() {
  if (valid_input()) {
    const data = {
      name: name.value,
      email: email.value,
      password: password.value,
      role: role.value,
      service_id: service_id.value,
      description: description.value,
      experience: experience.value,
      address_line: address_line.value,
      city: city.value,
      state: state.value,
      pincode: pincode.value,
    };

    const res = await register(data);
    messageStore.setFlashMessage(res.message);
    if (res.status) {
      router.push({ path: '/' });
    }
  }
}

// Modal and service handling
const services = ref([]);
const serviceLoadingError = ref(false);
const isAddressModalOpen = ref(false);
const isProfessionalModalOpen = ref(false);

function openAddressModal() {
  isAddressModalOpen.value = true;
}
function closeAddressModal() {
  isAddressModalOpen.value = false;
}
function openProfessionalModal() {
  fetchServices();
  isProfessionalModalOpen.value = true;
}
function closeProfessionalModal() {
  isProfessionalModalOpen.value = false;
}

const addressSummary = computed(() => 
  `${address_line.value}, ${city.value}, ${state.value}, ${pincode.value}`
);

const selectedRole = ref('');
function handleRoleChange(newRole) {
  selectedRole.value = newRole;
  if (newRole === 'professional') openProfessionalModal();
}

async function fetchServices() {
  try {
    const response = await fetch(`${backendURL.value}/api/v1/service`, {
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
    serviceLoadingError.value = true;
  }
}
</script>



<template>
  <div class="container-fluid mt-2 p-3">
    <h1 class="text-center">Register</h1>
    <div class="d-flex justify-content-center">
      <form class="w-50" @submit.prevent="onSubmit">
        <div class="mb-3">
          <label for="name" class="form-label"><strong>Name</strong></label>
          <input type="text" class="form-control" id="name" v-model="name" required />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label"><strong>Email Address</strong></label>
          <input type="email" class="form-control" id="email" v-model="email" @keyup="check_email" required />
        </div>
        <div id="usernameHelp" class="form-text">{{check_for_email}}</div>

        <div class="row">
          <div class="mb-3 col-6">
            <label for="password" class="form-label"><strong>Password</strong></label>
            <input type="password" class="form-control" id="password" v-model="password" required />
          </div>
          <div class="mb-3 col-6">
            <label for="confirmPassword" class="form-label"><strong>Confirm Password</strong></label>
            <input type="password" class="form-control" id="confirmPassword" v-model="confirm_password" required />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label"><strong>Address</strong></label>
          <button type="button" class="btn btn-outline-secondary w-100" @click="openAddressModal">
            Add Address
          </button>
          <div v-if="addressSummary" class="form-text mt-2">
            <strong>Address:</strong> {{ addressSummary }}
          </div>
        </div>

        <div class="mb-3">
  <label class="form-label"><strong>Role</strong></label>
  <div class="d-flex align-items-center">
    <div class="form-check me-4">
      <input type="radio" id="customer" value="customer" v-model="role" @change="handleRoleChange('customer')" class="form-check-input" required />
      <label for="customer" class="form-check-label">Customer</label>
    </div>
    <div class="form-check">
      <input type="radio" id="professional" value="professional" v-model="role" @change="handleRoleChange('professional')" class="form-check-input" required />
      <label for="professional" class="form-check-label">Professional</label>
    </div>
  </div>
</div>


        <div class="d-flex justify-content-center mb-3">
          <button type="submit" class="btn btn-primary">Register</button>
        </div>

        <div class="d-flex justify-content-center mt-2">
          <span>Already a user? </span>
          <RouterLink to="/login" class="ms-1">Login</RouterLink>
        </div>
      </form>
    </div>

    <!-- Address Modal -->
    <div v-if="isAddressModalOpen" class="modal show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Enter Address</h5>
            <button type="button" class="btn-close" @click="closeAddressModal"></button>
          </div>
          <div class="modal-body">
            <input v-model="address_line" class="form-control mb-2" placeholder="Address Line" required />
            <input v-model="city" class="form-control mb-2" placeholder="City" required />
            <input v-model="state" class="form-control mb-2" placeholder="State" required />
            <input v-model="pincode" class="form-control mb-2" placeholder="Pincode" required />
          </div>
        </div>
      </div>
    </div>

    <!-- Professional Modal -->
    <div v-if="isProfessionalModalOpen" class="modal show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Professional Details</h5>
            <button type="button" class="btn-close" @click="closeProfessionalModal"></button>
          </div>
          <div class="modal-body">
            <textarea v-model="description" class="form-control mb-3" placeholder="Description" required></textarea>
            <select v-model="service_id" class="form-control mb-3" required>
              <option value="" disabled>Select a Service</option>
              <option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
            </select>
            <input v-model="experience" type="number" class="form-control" placeholder="Experience (in years)" required />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
