<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg border-0" style="max-width: 550px; width: 100%">
      <!-- Card Header with Icon - Color Changed to Primary -->
      <div class="card-header bg-primary text-white text-center fs-4 fw-bolder rounded-top py-3">
        <i class="fas fa-user-doctor me-2"></i> Doctor Sign Up
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-4 fw-bold">Create Your Doctor Account</h4>

        <!-- Form with Input Groups and Icons -->
        <form @submit.prevent="signupDoctor">
          <!-- Name Input -->
          <div class="input-group mb-4">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-user"></i>
            </span>
            <input
              id="doctorName"
              v-model="name"
              class="form-control form-control-lg border-start-0"
              placeholder="Full Name"
              required
              type="text"
            />
          </div>

          <!-- Email Input -->
          <div class="input-group mb-4">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-envelope"></i>
            </span>
            <input
              id="doctorEmail"
              v-model="email"
              class="form-control form-control-lg border-start-0"
              placeholder="Email Address"
              required
              type="email"
            />
          </div>

          <!-- Password Input -->
          <div class="input-group mb-4">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-lock"></i>
            </span>
            <input
              id="doctorPassword"
              v-model="password"
              class="form-control form-control-lg border-start-0"
              placeholder="Password"
              required
              type="password"
            />
          </div>

          <!-- Date of Birth Input -->
          <div class="input-group mb-4">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-calendar-alt"></i>
            </span>
            <input
              id="doctorDOB"
              v-model="date_of_birth"
              class="form-control form-control-lg border-start-0"
              required
              type="date"
            />
          </div>

          <!-- Phone Number Input -->
          <div class="input-group mb-5">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-phone"></i>
            </span>
            <input
              id="doctorPhone"
              v-model="phone"
              class="form-control form-control-lg border-start-0"
              placeholder="Phone Number"
              required
              type="tel"
            />
          </div>

          <!-- Styled Error and Success Messages -->
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
          <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

          <div class="d-grid">
            <!-- Button Color Changed to Primary -->
            <button class="btn btn-primary btn-lg rounded-3 py-3 text-white fw-bold" type="submit">
              Sign Up
            </button>
          </div>
        </form>

        <!-- Link to Login Page - Color Changed to Primary -->
        <div class="text-center mt-4">
          <p>
            Already have an account?
            <router-link class="text-primary" to="/doctor-login">Login here</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- The <script> section remains the same as the improved version -->
<script>
export default {
  name: 'DoctorSignUp',
  data() {
    return {
      email: '',
      password: '',
      name: '',
      phone: '',
      date_of_birth: '',
      errorMessage: null,
      successMessage: null,
    }
  },
  methods: {
    signupDoctor: async function () {
      this.errorMessage = null
      this.successMessage = null
      const payload = {
        email: this.email,
        password: this.password,
        name: this.name,
        date_of_birth: this.date_of_birth,
        phone: this.phone,
        role: 'Doctor',
      }
      try {
        const response = await fetch('/api/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        const result = await response.json()

        if (!response.ok) {
          this.errorMessage = result.message || 'SignUp failed. Please check your credentials.'
        } else {
          this.successMessage = result.message
          setTimeout(() => {
            this.$router.push('/doctor-login')
          }, 2000)
        }
      } catch (error) {
        this.errorMessage = 'Unable to connect to the server.'
      }
    },
  },
}
</script>
