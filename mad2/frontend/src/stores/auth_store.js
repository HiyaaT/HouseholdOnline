import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', () => {
    const backend_server = 'http://127.0.0.1:5000';

    const token =ref(localStorage.getItem('auth_token'))
    const logged_user=ref(JSON.parse(localStorage.getItem('user_data')))

    const isAuthenticated=computed(()=>{
        return token.value!==null
    })

    function getToken(){
        return token.value
    }
    function setToken(new_token){
        token.value=new_token;
        //localStorage.setItem('auth_token', new_token)

    }

    function setUserData(new_user_data){
        logged_user.value=new_user_data;
        //localStorage.setItem('user_data', JSON.stringify(new_user_data))
    }

    function removeAuthUser(){
        token.value=null;
        logged_user.value=null
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data')
    }
    function getUserData(){
        return logged_user.value
    }

    function getBackendServerURL() {
        return backend_server;
    }

    return {
        getBackendServerURL,
        getToken,
        isAuthenticated,
        getUserData,
        setUserData,
        setToken,
        removeAuthUser
    };
});
