<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg border-0" style="max-width: 550px; width: 100%">
      <div class="card-header bg-dark text-white text-center fs-4 fw-bolder rounded-top py-3">
        Admin Login
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-4 fw-bold">Secure Administrator Access</h4>

        <form @submit.prevent="loginAdmin">
          <div class="mb-3">
            <label class="form-label fw-bold" for="adminEmail">Email</label>
            <input
              id="adminEmail"
              v-model="email"
              class="form-control form-control-lg rounded-3"
              required
              type="email"
            />
          </div>
          <div class="mb-5">
            <label class="form-label fw-bold" for="adminPassword">Password</label>
            <input
              id="adminPassword"
              v-model="password"
              class="form-control form-control-lg rounded-3"
              required
              type="password"
            />
          </div>
          <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
          <div class="d-grid">
            <button class="btn btn-dark btn-lg rounded-3 py-3" type="submit">Log In</button>
          </div>
        </form>

        <div class="text-center mt-4">
          <router-link class="text-muted text-decoration-none" to="/"
            >← Back to Role Selection</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    }
  },
  methods: {
    loginAdmin: async function () {
      this.errorMessage = null
      const payload = {
        email: this.email,
        password: this.password,
      }
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        })

        const result = await response.json()

        if (!response.ok) {
          this.errorMessage = result.message || 'Something went wrong. Please try again.'
        } else if (result.role !== 'Admin') {
          this.errorMessage = 'Access denied. You must log in as an admin.'
        } else {
          alert('Login successful!')
          localStorage.setItem('adminToken', result.token)
          this.$router.push('/admin-dashboard')
        }
      } catch (error) {
        this.errorMessage = 'Unable to connect to the server.'
      }
    },
  },
}
</script>
