<script setup>
import './assets/main.css'
import { useRouter, RouterLink, RouterView } from 'vue-router'
import {useAuthStore} from './stores/auth_store'
import { useMessageStore } from './stores/message_store'
import { computed, ref } from 'vue';
const messageStore=useMessageStore()
const message=computed(()=>messageStore.getFlashMessage());
const authStore=useAuthStore();
const user=computed(()=>authStore.getUserData())
const isAuthenticated=computed(()=>authStore.isAuthenticated)
const router=useRouter()
function logout(){
  fetch(`${authStore.getBackendServerURL()}/api/v1/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token':authStore.getToken()
      }
    }).then(response=>response.json()).then(data=> {
      console.log(data)
      messageStore.setFlashMessage(data.message)
    })
  router.push('/')
  authStore.removeAuthUser()
  messageStore.setFlashMessage("logged out")
  
}

const isAdmin=computed(()=>{
  if (isAuthenticated.value){
    console.log(user)
    if (user.value.roles.includes('admin')){
    return true
  }
  }
  
  return false
})

const isCustomer=computed(()=>{
  if (isAuthenticated.value){
    if (user.value.roles.includes('customer')){
    return true
  }
  }
  
  return false
})
const isProfessional=computed(()=>{
  if (isAuthenticated.value){
    if (user.value.roles.includes('professional')){
    return true
  }
  }
  
  return false
})
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <div class="navbar-brand">Household online</div>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if ="!isAuthenticated">
            <RouterLink to="/" class="nav-link">Login</RouterLink>
          </li>
          <li class="nav-item" v-if ="!isAuthenticated">
            <RouterLink to="/register" class="nav-link">Register</RouterLink>
          </li> 
          <li class="nav-item" v-if="isAuthenticated">
            <button @click="logout" class="nav-link" type="button">Logout</button>
          </li>
          <li class="nav-item" v-if ="isAuthenticated">
            <button  class="nav-link" disable>{{user.name}}</button>
          </li>
          <li class="nav-item" v-if ="isAdmin">
            <RouterLink to="/createservice" class="nav-link">Create Service</RouterLink>
          </li>
          <li class="nav-item" v-if ="isAdmin">
            <RouterLink to="/admin-dash" class="nav-link">Home</RouterLink>
          </li>
          <li class="nav-item" v-if ="isAdmin">
            <RouterLink to="/search_admin" class="nav-link">Search</RouterLink>
          </li>
          <li class="nav-item" v-if ="isCustomer">
            <RouterLink to="/customer-dash" class="nav-link">Home</RouterLink>
          </li>
          <li class="nav-item" v-if ="isCustomer">
            <RouterLink to="/search_customer" class="nav-link">Search</RouterLink>
          </li>
          <li class="nav-item" v-if ="isProfessional">
            <RouterLink to="/professional-dash" class="nav-link">Home</RouterLink>
          </li>
          <li class="nav-item" v-if ="isProfessional">
            <RouterLink to="/profile" class="nav-link">Profile</RouterLink>
          </li>
          <li class="nav-item" v-if ="isCustomer">
            <RouterLink to="/profile" class="nav-link">Profile</RouterLink>
          </li>
          <li class="nav-item" v-if ="isAdmin">
            <RouterLink to="/admin_summary" class="nav-link">Summary</RouterLink>
          </li>
          <li class="nav-item" v-if ="isProfessional">
            <RouterLink to="/professional_summary" class="nav-link">Summary</RouterLink>
          </li>
          
        </ul>
        
      </div>
    </div>
  </nav>
  <div v-if="message" class = "container-fluid text-bg-primary p-2">
    <p>{{ message }}</p>
  </div>
  <RouterView />
</template>


