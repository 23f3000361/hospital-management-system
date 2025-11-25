<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg" style="max-width: 550px; width: 100%">
      <div class="card-header bg-primary text-white text-center fs-4 fw-bolder rounded-top py-3">
        Welcome to the City Hospital App
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-5 fw-bold">Choose your role:</h4>

        <div class="d-grid gap-4">
          <router-link class="btn btn-primary btn-lg rounded-3 py-3" to="/admin-login"
            >Admin</router-link
          >
          <router-link class="btn btn-secondary btn-lg rounded-3 py-3" to="/patient-login"
            >Patient</router-link
          >
          <router-link class="btn btn-danger btn-lg rounded-3 py-3" to="/doctor-login"
            >Doctor</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>
