<template>
    <div class="container py-5">
      <div class="row justify-content-center">
        <!-- Pie Chart Box -->
        <div class="col-md-6 col-lg-5 mb-4">
          <div class="card h-100">
            <div class="card-body d-flex flex-column">
              <h3 class="card-title text-center">Ratings </h3>
              <canvas ref="pieChartCanvas" class="chart-canvas"></canvas>
            </div>
          </div>
        </div>
  
        <!-- Bar Chart Box -->
        <div class="col-md-6 col-lg-5 mb-4">
          <div class="card h-100">
            <div class="card-body d-flex flex-column">
              <h3 class="card-title text-center">Service Requests </h3>
              <canvas ref="barChartCanvas" class="chart-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed} from 'vue';
  import { Chart, PieController, ArcElement, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';
  const user=computed(()=>authStore.getUserData())
  Chart.register(
    PieController,
    ArcElement,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend
  );
  
  const pieChartCanvas = ref(null);
  const barChartCanvas = ref(null);
  const pieChart = ref(null); // Pie chart instance
  const barChart = ref(null); // Bar chart instance
  
  import { useAuthStore } from '@/stores/auth_store';
  const authStore = useAuthStore();
  const backendURL = authStore.getBackendServerURL();
  
  const fetchDataAndRenderCharts = async () => {
    try {
      const response = await fetch(`${backendURL}/api/v1/rating_summary/${user.value.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': authStore.getToken(),
        },
      });

  
      const result = await response.json();
  
      const labels = result.label;
      const data = result.data;

      const response1 = await fetch(`${backendURL}/api/v1/professional_status_count/${user.value.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': authStore.getToken(),
        },
      });
      const result1 = await response1.json();

      const labels1 = result1.label;
      const data1 = result1.data;
      // Create Pie Chart
      pieChart.value = new Chart(pieChartCanvas.value, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'User Distribution (Pie)',
              data: data,
              backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)','rgba(54, 162, 235, 0.6)', 'rgba(255, 205, 86, 0.6)'],
              borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)','rgba(255, 205, 86, 1)' ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
            },
          },
        },
      });
  
      // Create Bar Chart
      barChart.value = new Chart(barChartCanvas.value, {
        type: 'bar',
        data: {
          labels: labels1,
          datasets: [
            {
              label: 'status',
              data: data1,
              backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)','rgba(54, 162, 235, 0.6)', 'rgba(255, 205, 86, 0.6)'],
              borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)','rgba(255, 205, 86, 1)' ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  
  onMounted(() => {
    fetchDataAndRenderCharts();
  });
  </script>
  
  