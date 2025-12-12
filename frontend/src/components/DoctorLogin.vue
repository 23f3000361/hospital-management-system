<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg border-0" style="max-width: 550px; width: 100%">
      <div class="card-header bg-info text-white text-center fs-4 fw-bolder rounded-top py-3">
        Doctor Login
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-4 fw-bold">Access Doctor Dashboard</h4>

        <form @submit.prevent="loginDoctor">
          <div class="mb-3">
            <label class="form-label fw-bold" for="doctorEmail">Email</label>
            <input
              id="doctorEmail"
              v-model="email"
              class="form-control form-control-lg rounded-3"
              required
              type="email"
            />
          </div>
          <div class="mb-5">
            <label class="form-label fw-bold" for="doctorPassword">Password</label>
            <input
              id="doctorPassword"
              v-model="password"
              class="form-control form-control-lg rounded-3"
              required
              type="password"
            />
          </div>

          <div v-if="errorMessage" class="text-danger mb-3">{{ errorMessage }}</div>

          <div class="d-grid">
            <button class="btn btn-info btn-lg rounded-3 py-3 text-white" type="submit">
              Log In
            </button>
          </div>
        </form>

        <div class="text-center mt-4">
          <router-link class="text-info text-decoration-none fw-bold" to="/doctor-signup">
            New Doctor? Register Here
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
  name: 'DoctorLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    }
  },
  methods: {
    loginDoctor: async function () {
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
        } else if (result.role !== 'Doctor') {
          this.errorMessage = 'Access denied. You must log in as a doctor.'
        } else {
          alert('Login successful!')
          localStorage.setItem('doctorToken', result.token)
          this.$router.push('/doctor-dashboard') // redirect to Doctor Dashboard
        }
      } catch (error) {
        this.errorMessage = 'Unable to connect to the server.'
      }
    },
  },
}
</script>
