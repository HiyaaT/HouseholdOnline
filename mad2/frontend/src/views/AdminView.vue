<template>
  <div class="container mt-5">
    <ServiceTable />
  </div>
  <div class="container mt-5">
    <ServiceCsvButton />
  </div>

  <div class="container mt-5">
    <ProfessionalTable />
  </div>

  <div class="container mt-5">
    <ServiceRequestTable />
  </div>
</template>

<script setup>
import ServiceTable from '@/components/ServiceTable.vue';
import ProfessionalTable from '@/components/ProfessionalTable.vue';
import ServiceRequestTable from '@/components/ServiceRequestTable.vue';
import ServiceCsvButton from '@/components/CsvButton.vue';
</script>

<style scoped>
/* Any styles for your AdminView */
</style>
