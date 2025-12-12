<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg border-0" style="max-width: 550px; width: 100%">
      <div class="card-header bg-success text-white text-center fs-4 fw-bolder rounded-top py-3">
        Patient Login
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-4 fw-bold">Access Your Patient Portal</h4>

        <form @submit.prevent="loginPatient">
          <div class="mb-3">
            <label class="form-label fw-bold" for="patientEmail">Email</label>
            <input
              id="patientEmail"
              v-model="email"
              class="form-control form-control-lg rounded-3"
              required
              type="email"
            />
          </div>

          <div class="mb-5">
            <label class="form-label fw-bold" for="patientPassword">Password</label>
            <input
              id="patientPassword"
              v-model="password"
              class="form-control form-control-lg rounded-3"
              required
              type="password"
            />
          </div>

          <div v-if="errorMessage" class="text-danger mb-3">{{ errorMessage }}</div>

          <div class="d-grid">
            <button class="btn btn-success btn-lg rounded-3 py-3 text-white" type="submit">
              Log In
            </button>
          </div>
        </form>

        <div class="text-center mt-4">
          <router-link class="text-success text-decoration-none fw-bold" to="/patient-signup">
            New Patient? Register Here
          </router-link>
        </div>

        <!-- Back to Role Selection Link -->
        <div class="text-center mt-3">
          <router-link class="text-secondary text-decoration-none small" to="/">
            <i class="fas fa-arrow-left me-1"></i>← Back to Role Selection
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    }
  },
  methods: {
    loginPatient: async function () {
      this.errorMessage = null
      const payload = {
        email: this.email,
        password: this.password,
      }

      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        const result = await response.json()

        if (!response.ok) {
          this.errorMessage = result.message || 'Login failed. Please check your credentials.'
        } else if (result.role !== 'Patient') {
          this.errorMessage = 'Access denied. You must log in as a patient.'
        } else {
          alert('Login successful!')
          localStorage.setItem('patientToken', result.token)
          this.$router.push('/patient-dashboard') // redirect to Patient Dashboard
        }
      } catch (error) {
        this.errorMessage = 'Unable to connect to the server.'
      }
    },
  },
}
</script>
