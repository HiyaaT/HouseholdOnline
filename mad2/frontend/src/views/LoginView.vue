<script setup>
import { ref, computed } from 'vue';
import { useMessageStore } from '@/stores/message_store';
import { useAuthStore } from '@/stores/auth_store';

import {useRouter} from 'vue-router';

const router =useRouter();
const email = ref('');
const name= ref('');
const password = ref('');

const messageStore = useMessageStore();
const authStore = useAuthStore();

const backend_url = computed(() => authStore.getBackendServerURL());

async function login() {
    const input_data = {
        email: email.value,
        password: password.value
    };

    console.log("Input Data:", input_data);
    console.log("Backend URL:", backend_url.value);

    const response = await fetch(`${backend_url.value}/api/v1/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        body: JSON.stringify(input_data)
    });

    if(response.ok){
       const data=await response.json();
       console.log(data);
       messageStore.setFlashMessage(data.message);
       localStorage.setItem('auth_token', data.login_credentials.auth_token);
       authStore.setToken(data.login_credentials.auth_token)
       
       const user_data = {
       id: data.login_credentials.id,
       email: data.login_credentials.email,
       name: data.login_credentials.name,
       roles: data.login_credentials.roles,
       service_id: data.login_credentials.roles.includes('professional') ? data.login_credentials.service_id : null
       };

       localStorage.setItem('user_data', JSON.stringify(user_data));
       authStore.setUserData(user_data)
       console.log(authStore.isAuthenticated)
       console.log(data.login_credentials.roles)
       if (data.login_credentials.roles=='admin'){
        router.push('/admin-dash')
       }
       else if(data.login_credentials.roles=='customer'){
        router.push('/customer-dash');
       }
       else{
        router.push('/professional-dash');
       }
       

    }else{
        const data =await response.json();
        messageStore.setFlashMessage(data.message);
    }

       
}
</script>

<template>
    <div class="container-fluid mt-2 p-3">
        <h1 class="text-center">Login</h1>
        <div class="d-flex justify-content-center">
            <form class="w-50 justify-content-center" @submit.prevent="login">
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Email address</label>
                    <input
                        type="email"
                        class="form-control"
                        id="exampleInputEmail1"
                        v-model="email"
                        required
                    />
                    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Password</label>
                    <input
                        type="password"
                        class="form-control"
                        id="exampleInputPassword1"
                        v-model="password"
                        required
                    />
                </div>
                <div class="d-flex justify-content-center mb-3">
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
                <div class="d-flex justify-content-center mt-2">
                    <span>Don't have an account? &ensp;</span>
                    <RouterLink to='/register'>Register</RouterLink>
                </div>
            </form>
        </div>
    </div>
</template>
