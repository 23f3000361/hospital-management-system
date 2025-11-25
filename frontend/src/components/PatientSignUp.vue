<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg border-0" style="max-width: 550px; width: 100%">
      <div class="card-header bg-info text-white text-center fs-4 fw-bolder rounded-top py-3">
        <i class="fas fa-user-plus me-2"></i> Patient Sign Up
      </div>

      <div class="card-body p-5">
        <h4 class="card-title text-center text-dark mb-4 fw-bold">Create Your Patient Account</h4>

        <!-- Improved Form with Input Groups and Icons -->
        <form @submit.prevent="signupPatient">
          <!-- Name Input -->
          <div class="input-group mb-4">
            <span class="input-group-text bg-light border-end-0">
              <i class="fas fa-user"></i>
            </span>
            <input
              id="patientName"
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
              id="patientEmail"
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
              id="patientPassword"
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
              id="patientDOB"
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
              id="patientPhone"
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
            <!-- Button Color Changed to Teal (info) -->
            <button class="btn btn-info btn-lg rounded-3 py-3 text-white fw-bold" type="submit">
              Create Account
            </button>
          </div>
        </form>

        <!-- Link to Login Page - Color Changed to a darker teal for readability -->
        <div class="text-center mt-4">
          <p>
            Already have an account?
            <router-link class="text-info" style="font-weight: 500" to="/patient-login"
              >Login here</router-link
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- The <script> section remains the same as the improved version -->
<script>
export default {
  name: 'PatientSignUp',
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
    signupPatient: async function () {
      this.errorMessage = null
      this.successMessage = null
      const payload = {
        email: this.email,
        password: this.password,
        name: this.name,
        date_of_birth: this.date_of_birth,
        phone: this.phone,
        role: 'Patient',
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
            this.$router.push('/patient-login')
          }, 2000)
        }
      } catch (error) {
        this.errorMessage = 'Unable to connect to the server.'
      }
    },
  },
}
</script>
