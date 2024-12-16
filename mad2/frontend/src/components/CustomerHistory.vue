<template>
  <!-- Request History -->
  <div class="container mt-5">
    <h2 class="text-center mb-4">Request History</h2>
    <div class="table-responsive shadow-sm rounded">
      <table class="table align-middle text-center">
        <thead class="table-primary">
          <tr>
            <th>ServiceID</th>
            <th>Service</th>
            <th>Professional</th>
            <th>Status</th>
            <th>Actions</th>
           
          </tr>
        </thead>
        <tbody>
          <tr v-for="(request, index) in requests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.service }}</td>
            <td>{{ request.professional }}</td>
            <td>{{ request.status }}</td>
            <td>
              <span v-if="request.status==='rejected' || request.status==='closed_c'|| request.reviewed===true">
                no actions
              </span>
              <div v-else-if="request.status === 'closed_p' && request.reviewed===false">
              <button class="btn btn-lilac btn-sm"@click="openCloseRequestModal(request, true)">Review</button>
              </div>
             
              <div v-else-if="request.status === 'requested'">
              <button class="btn btn-light-green btn-sm me-2" @click="EditRequestModal(request)"> edit</button>
              <button class="btn btn-lilac btn-sm"@click="DeleteRequest(request.id)">delete</button>
              </div>
              <button v-else-if="request.status === 'accepted'" class="btn btn-light-blue btn-sm" @click="openCloseRequestModal(request)">Close</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Close Request Modal -->
    <div 
      class="modal fade" 
      id="closeRequestModal" 
      tabindex="-1" 
      aria-labelledby="closeRequestModalLabel" 
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="closeRequestModalLabel">Close Request</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitCloseRequest">
              <div class="mb-3">
                <label for="serviceName" class="form-label">Service Name</label>
                <input 
                  type="text" 
                  v-model="closeRequestServiceName" 
                  class="form-control" 
                  id="serviceName" 
                  readonly
                />
              </div>
              <div class="mb-3">
                <label for="professionalName" class="form-label">Professional Name</label>
                <input 
                  type="text" 
                  v-model="closeRequestProfessionalName" 
                  class="form-control" 
                  id="professionalName" 
                  readonly
                />
              </div>
              <div class="mb-3">
                <label for="rating" class="form-label">Rating (1-5)</label>
                <input 
                  type="number" 
                  v-model="closeRequestRating" 
                  class="form-control" 
                  id="rating" 
                  min="1" 
                  max="5" 
                  required
                />
              </div>
              <div class="mb-3">
                <label for="comment" class="form-label">Comment</label>
                <textarea 
                  v-model="closeRequestComment" 
                  class="form-control" 
                  id="comment" 
                  rows="3" 
                  placeholder="Enter your comments"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="closeDate" class="form-label">Date</label>
                <input 
                  type="date" 
                  v-model="closeRequestDate" 
                  class="form-control" 
                  id="closeDate" 
                  required
                />
              </div>
              <input type="hidden" v-model="currentRequestId" />
              <input type="hidden" v-model="currentProfessionalId" />
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Close Request</button>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Edit Request Modal -->
<div 
  class="modal fade" 
  id="editRequestModal" 
  tabindex="-1" 
  aria-labelledby="editRequestModalLabel" 
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="editRequestModalLabel">Edit Request</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submitEditRequest">
          <div class="mb-3">
            <label for="editRequestDate" class="form-label">Date of Request</label>
            <input 
              type="date" 
              v-model="editRequestDate" 
              class="form-control" 
              id="editRequestDate" 
              required
            />
          </div>
          <div class="mb-3">
            <label for="remark" class="form-label">Remark</label>
            <textarea 
              v-model="editRequestRemark" 
              class="form-control" 
              id="remark" 
              rows="3" 
              placeholder="Enter your remarks"
            ></textarea>
          </div>
          <input type="hidden" v-model="currentRequestId" />
          <div class="modal-footer">
            <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth_store';

const authStore = useAuthStore();
const backendURL = authStore.getBackendServerURL();
const user=computed(()=>authStore.getUserData())


const requests = ref([]);
const closeRequestRating = ref(0);
const closeRequestComment = ref('');
const closeRequestServiceName = ref('');
const closeRequestProfessionalName = ref('');
const closeRequestDate = ref(new Date().toISOString().substr(0, 10));
const currentRequestId = ref(null);
const currentProfessionalId = ref(null); 

const editRequestDate = ref('');
const editRequestRemark = ref('');




const fetchRequest = async () => {
  try {
    const response = await fetch(`${backendURL}/api/v1/servicerequestcustomer/${user.value.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
    });
    if (!response.ok) throw new Error('Failed to fetch requests');
    requests.value = await response.json();
    console.log(requests.value)
  } catch (error) {
    console.error(error);
  }
};

let isReviewAction = ref(false);

const openCloseRequestModal = (request, isReview = false) => {
  closeRequestServiceName.value = request.service;
  closeRequestProfessionalName.value = request.professional;
  closeRequestRating.value = 0;
  closeRequestComment.value = '';
  closeRequestDate.value = new Date().toISOString().substr(0, 10);

  currentRequestId.value = request.id;
  currentProfessionalId.value = request.professional_id;
  isReviewAction.value = isReview;

  const modal = bootstrap.Modal.getInstance(document.getElementById('closeRequestModal'));
  if (modal) {
    modal.hide();
  }

  const newModal = new bootstrap.Modal(document.getElementById('closeRequestModal'));
  newModal.show();
};


const closeServiceRequestStatus = async (requestId) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/closerequest/${requestId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify({ status: 'closed_c' }),
    });
    if (!response.ok) throw new Error('Failed to update service request status.');
  } catch (error) {
    console.error('Error updating service request status:', error);
    alert('Failed to update service request status. Please try again.');
  }
};

const insertServiceRating = async (data) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/review`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to insert service rating.');
  } catch (error) {
    console.error('Error inserting service rating:', error);
    alert('Failed to insert service rating. Please try again.');
  }
};

const submitCloseRequest = async () => {
  const serviceRatingData = {
    professional_id: currentProfessionalId.value,
    customer_id: user.value.id,
    service_request_id: currentRequestId.value,
    rating: closeRequestRating.value,
    comment: closeRequestComment.value,
    date: closeRequestDate.value,
  };

  try {
    // Perform only rating insertion if it's a review
    if (isReviewAction.value) {
      await insertServiceRating(serviceRatingData);
      alert('Review submitted successfully.');
    } else {
      // Perform both actions for closing the request
      await closeServiceRequestStatus(currentRequestId.value);
      await insertServiceRating(serviceRatingData);
      alert('Request closed and rating submitted successfully.');
    }

    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('closeRequestModal'));
    modal.hide();

    // Refresh the request list
    fetchRequest();
  } catch (error) {
    console.error('Error submitting request:', error);
    alert('Failed to submit request. Please try again.');
  }
};


const EditRequestModal = (request) => {
  const parsedDate = new Date(request.date_of_request);
  editRequestDate.value = parsedDate.toISOString().split('T')[0]; 
  editRequestRemark.value = request.remarks || '';
  currentRequestId.value = request.id;

  const modal = new bootstrap.Modal(document.getElementById('editRequestModal'));
  modal.show();
};

const submitEditRequest = async () => {
  const data = {
    date_of_request: editRequestDate.value,
    remark: editRequestRemark.value,
  };

  try {
    const response = await fetch(`${backendURL}/api/v1/editrequest/${currentRequestId.value}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update request.');

    alert('Request updated successfully.');
    fetchRequest(); 
    const modal = bootstrap.Modal.getInstance(document.getElementById('editRequestModal'));
    modal.hide();
  } catch (error) {
    console.error('Error updating request:', error);
    alert('Failed to update request. Please try again.');
  }
};

const DeleteRequest = async (id) => {
  try {
    const response = await fetch(`${backendURL}/api/v1/editrequest/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getToken(),
      }
    });
    if (!response.ok) throw new Error('Failed to delete request.');

    alert('Request deleted successfully.');
    fetchRequest(); 
  } catch (error) {
    console.error('Error deleting request:', error);
    alert('Failed to update request. Please try again.');
  }
};

onMounted(fetchRequest);
</script>

<style scoped>
.service-card {
  cursor: pointer;
  transition: transform 0.2s;
}
.service-card:hover {
  transform: scale(1.05);
}
</style>
