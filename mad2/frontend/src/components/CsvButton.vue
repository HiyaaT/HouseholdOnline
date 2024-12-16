<template>
    <div>
      <button @click="createCsv" class="btn btn-lilac">Get closed request by professional Data</button>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '@/stores/auth_store'; 
  const authStore = useAuthStore();
  const backendURL = authStore.getBackendServerURL();
  
  const createCsv = async () => {
    try {
      const res = await fetch(`${backendURL}/create-csv`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.auth_token, 
        },
      });
  
      if (!res.ok) {
        alert('error occured');
      }
  
      const { task_id } = await res.json(); 
  
      console.log(`Task created with ID: ${task_id}`);
  
      
      const interval = setInterval(async () => {
        const res = await fetch(`${backendURL}/get-csv/${task_id}`, {
          headers: {
            'Authentication-Token': authStore.auth_token, 
          },
        });
  
        if (res.ok) {
          console.log('Data is ready');
          window.open(`${backendURL}/get-csv/${task_id}`); 
          clearInterval(interval); 
        } else {
          const { message } = await res.json();
          console.log(message); 
        }
      }, 1000); 
    } catch (error) {
      console.error('Error creating CSV:', error);
    }
  };
  </script>
  
  