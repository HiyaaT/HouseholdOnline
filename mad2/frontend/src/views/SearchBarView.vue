<template>
    <div id="app" class="container mt-4">
    
  
      <!-- Search Form Section -->
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="input-group mb-3">
            <label class="input-group-text" for="searchType">Search by</label>
            <select
              class="form-select"
              v-model="searchType"
              id="searchType"
              @change="resetSearch"
            >
              <option value="customer">Customer</option>
              <option value="professional">Professional</option>
              <option value="servicerequests">ServiceRequests</option>
            </select>
          </div>
  
          <!-- Customer Search Fields -->
          <div v-if="searchType === 'customer'">
            <input
              v-model="searchFields.name"
              type="text"
              class="form-control mb-2"
              placeholder="Enter Customer Name"
            />
            <input
              v-model="searchFields.city"
              type="text"
              class="form-control mb-2"
              placeholder="Enter City"
            />
            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-primary me-2" @click="searchCustomerByInputs">
                Search by Inputs
              </button>
              <button class="btn btn-outline-secondary" @click="searchAllCustomers">
                Search All Customers
              </button>
            </div>
          </div>
           
          <!-- Service Request Search Fields -->
          <div v-if="searchType === 'servicerequests'">
            <select
            v-model="searchFields.status"
            class="form-control mb-2"
            >
            <option disabled value="">Status</option>
            <option value="closed">closed</option>
            <option value="requested">requested</option>
            <option value="accepted">accepted</option>
            </select>

            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-primary me-2" @click="searchRequestByInputs">
                Search by Inputs
              </button>
              <button class="btn btn-outline-secondary" @click="searchAllRequests">
                Search All Requests
              </button>
            </div>
          </div>
  
          <!-- Professional Search Fields -->
          <div v-if="searchType === 'professional'">
            <input
              v-model="searchFields.name"
              type="text"
              class="form-control mb-2"
              placeholder="Enter Professional Name"
            />
            <input
              v-model="searchFields.city"
              type="text"
              class="form-control mb-2"
              placeholder="Enter City"
            />
            <input
              v-model="searchFields.service"
              type="text"
              class="form-control mb-2"
              placeholder="Enter Service Provided"
            />
            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-primary me-2" @click="searchProfessionalByInputs">
                Search by Inputs
              </button>
              <button class="btn btn-outline-secondary" @click="searchAllProfessionals">
                Search All Professionals
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Modal for Profile Details -->
<div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="profileModalLabel">Profile Details</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p><strong>Name:</strong> {{ profileData.name }}</p>
        <p v-if="searchType === 'professional'"><strong>Description:</strong> {{ profileData.description }}</p>
        <p v-if="searchType === 'professional'"><strong>Experience:</strong> {{ profileData.experience }} years</p>
        <p v-if="searchType === 'professional'"><strong>Service:</strong> {{ profileData.service }}</p>
        <p v-if="searchType === 'professional'"><strong>Average Rating:</strong> {{ profileData.avg_rating }}</p>
        <p><strong>Address:</strong> {{ profileData.address_line }}, {{ profileData.city }}, {{ profileData.state }}, {{ profileData.pincode }}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

      <!-- Results Section -->
      <div v-if="results.length" class="container mt-5">
        <h4 class="text-center">Search Results ({{ searchType }})</h4>
        <table v-if="searchType!='servicerequests'" class="table table-hover mt-3">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th v-if="searchType === 'customer'">City</th>
              <th v-if="searchType === 'professional'">City</th>
              <th v-if="searchType === 'professional'">Description</th>
              <th v-if="searchType === 'professional'">Experience</th>
              <th v-if="searchType === 'professional'">Service</th>
          
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in results" :key="result.id">
              <td>{{ result.id }}</td>
              <td>{{ result.name }}</td>
              <td>{{ result.city }}</td>
              <td v-if="searchType === 'professional'">{{ result.description }}</td>
              <td v-if="searchType === 'professional'">{{ result.experience }} years</td>
              <td v-if="searchType === 'professional'">{{ result.service }}</td>
              <td class="table-actions">
              <button v-if="result.blocked" 
                class="btn btn-lilac"
                @click="blockUnblock(result)">
                Unblock
              </button>
              <button v-else
                class="btn btn-light-blue"
                @click="blockUnblock(result)">
                block
              </button>
              <button class="btn btn-light-green"  @click="viewProfile(result.id)">
              view profile
              </button>
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="searchType==='servicerequests'" class="table table-hover mt-3">
          <thead>
            <tr>
              <th>Service ID</th>
              <th>Serive of</th>
              <th>Status</th>
              <th>by professional</th>
              <th>for customer</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in results" :key="result.id">
              <td>{{ result.id }}</td>
              <td>{{ result.service }}</td>
              <td v-if="result.status==='closed_p' || result.status==='closed_c'">closed</td>
              <td v-else>{{ result.status }}</td>
              <td>{{ result.professional }}</td>
              <td>{{ result.customer }}</td>
              
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
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/auth_store';
  
  const authStore = useAuthStore();
  const backendURL = authStore.getBackendServerURL();
  const profileData = ref({});
  const searchType = ref('customer');
  const searchFields = ref({ name: '', city: '', service: '', status:'' });
  const results = ref([]);
  const searchPerformed = ref(false);
  
  const resetSearch = () => {
    searchFields.value = { name: '', city: '', service: '', status:'' };
    results.value = [];
    searchPerformed.value = false;
  };

  const blockUnblock= async(result)=>{
    const apiUrl = `${backendURL}/api/v1/block_unblock/${result.id}`;
    try {
      const response = await fetch(apiUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.getToken(), 
        },
      });
      if(response.ok){
        if(result.blocked===true){
            result.blocked=false
        }
        else{
            result.blocked=true
        }
      }
      if (!response.ok) throw new Error('Network response was not ok');
  
    } catch (error) {
      console.error('Error:', error);
    }

  }
  
  const searchCustomerByInputs = async () => {
    const { name, city } = searchFields.value;
    const apiUrl = `${backendURL}/api/v1/customer_input_based?name=${name}&city=${city}`;
    await fetchData(apiUrl);
  };

  const searchRequestByInputs = async () => {
   
    const { status } = searchFields.value;
    console.log(status)
    const apiUrl = `${backendURL}/api/v1/statusbasedservicerequests/${status}`;
    await fetchData(apiUrl);
  };
  
  const searchAllRequests = async () => {
    const apiUrl = `${backendURL}/api/v1/allservicerequest`;
    await fetchData(apiUrl);
  };

  const searchAllCustomers = async () => {
    const apiUrl = `${backendURL}/api/v1/customers`;
    await fetchData(apiUrl);
  };
  
  const searchProfessionalByInputs = async () => {
    const { name, service, city } = searchFields.value;
    const apiUrl = `${backendURL}/api/v1/professional_input_based?name=${name}&service=${service}&city=${city}`;
    await fetchData(apiUrl);
  };
  
  const searchAllProfessionals = async () => {
    const apiUrl = `${backendURL}/api/v1/professionals`;
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
      results.value = data;
      console.log(data)
    } catch (error) {
      console.error('Error fetching data:', error);
      results.value = [];
    }
  };



const viewProfile = async (id) => {
  const apiUrl = `${backendURL}/api/v1/prof_profile/${id}`;
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });

    if (!response.ok) throw new Error('Failed to fetch profile data');

    profileData.value = await response.json();
    const modal = new bootstrap.Modal(document.getElementById('profileModal'));
    modal.show();
  } catch (error) {
    console.error('Error fetching profile data:', error);
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
  