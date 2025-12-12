<template>
  <div class="home-page">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold fs-3" href="#">
          <i class="fas fa-heartbeat text-danger me-2"></i> City Hospital
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="#roles">Login</a></li>
            <li class="nav-item"><a class="nav-link" href="#services">Services</a></li>
            <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section d-flex align-items-center text-white">
      <div class="container text-center">
        <h1 class="display-3 fw-bold mb-3 animate-fade-in">Compassionate Care, Advanced Medicine</h1>
        <p class="lead mb-5 fs-4">Your health is our priority. Connect with the best specialists in the city.</p>
        <a href="#roles" class="btn btn-primary btn-lg rounded-pill px-5 fw-bold shadow">Get Started</a>
      </div>
    </header>

    <!-- Role Selection Section -->
    <section id="roles" class="py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold text-dark">Choose Your Portal</h2>
          <p class="text-muted">Please select your role to proceed to the dashboard.</p>
        </div>

        <div class="row g-4 justify-content-center">
          <!-- Patient Card -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card text-center py-4">
              <div class="card-body">
                <div class="icon-box bg-success-subtle text-success mb-4 mx-auto rounded-circle d-flex align-items-center justify-content-center">
                  <i class="fas fa-user-injured fa-2x"></i>
                </div>
                <h4 class="card-title fw-bold">Patient</h4>
                <p class="card-text text-muted mb-4">Book appointments, view medical history, and manage your profile.</p>
                <router-link class="btn btn-outline-success rounded-pill px-4 fw-bold" to="/patient-login">
                  Patient Login
                </router-link>
              </div>
            </div>
          </div>

          <!-- Doctor Card -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card text-center py-4">
              <div class="card-body">
                <div class="icon-box bg-info-subtle text-info mb-4 mx-auto rounded-circle d-flex align-items-center justify-content-center">
                  <i class="fas fa-user-md fa-2x"></i>
                </div>
                <h4 class="card-title fw-bold">Doctor</h4>
                <p class="card-text text-muted mb-4">Manage schedules, view patient records, and update treatments.</p>
                <router-link class="btn btn-outline-info rounded-pill px-4 fw-bold text-dark" to="/doctor-login">
                  Doctor Login
                </router-link>
              </div>
            </div>
          </div>

          <!-- Admin Card -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card text-center py-4">
              <div class="card-body">
                <div class="icon-box bg-primary-subtle text-primary mb-4 mx-auto rounded-circle d-flex align-items-center justify-content-center">
                  <i class="fas fa-user-shield fa-2x"></i>
                </div>
                <h4 class="card-title fw-bold">Admin</h4>
                <p class="card-text text-muted mb-4">Manage departments, doctors, and oversee hospital operations.</p>
                <router-link class="btn btn-outline-primary rounded-pill px-4 fw-bold" to="/admin-login">
                  Admin Login
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services / Features Snippet -->
    <section id="services" class="py-5 bg-white">
      <div class="container">
        <div class="row text-center g-4">
          <div class="col-md-4">
            <i class="fas fa-ambulance fa-3x text-danger mb-3"></i>
            <h5 class="fw-bold">24/7 Emergency</h5>
            <p class="text-muted small">Immediate care for critical conditions round the clock.</p>
          </div>
          <div class="col-md-4">
            <i class="fas fa-dna fa-3x text-primary mb-3"></i>
            <h5 class="fw-bold">Modern Lab</h5>
            <p class="text-muted small">Advanced diagnostic laboratory for accurate results.</p>
          </div>
          <div class="col-md-4">
            <i class="fas fa-user-nurse fa-3x text-success mb-3"></i>
            <h5 class="fw-bold">Expert Staff</h5>
            <p class="text-muted small">Highly qualified doctors and nursing staff.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer id="contact" class="bg-dark text-white py-4">
      <div class="container text-center">
        <div class="mb-3">
          <i class="fab fa-facebook fa-lg mx-2 pointer"></i>
          <i class="fab fa-twitter fa-lg mx-2 pointer"></i>
          <i class="fab fa-instagram fa-lg mx-2 pointer"></i>
        </div>
        <p class="mb-0 small">&copy; 2025 City Hospital Management System. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
/* Hero Section with a professional gradient overlay */
.hero-section {
  background: linear-gradient(rgba(0, 50, 100, 0.7), rgba(0, 50, 100, 0.7)), 
              url('https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
  background-size: cover;
  background-position: center;
  height: 80vh; /* Takes up 80% of the viewport height */
  min-height: 500px;
}

/* Icon Circles */
.icon-box {
  width: 80px;
  height: 80px;
}

.bg-primary-subtle { background-color: rgba(13, 110, 253, 0.1); }
.bg-success-subtle { background-color: rgba(25, 135, 84, 0.1); }
.bg-info-subtle { background-color: rgba(13, 202, 240, 0.1); }

/* Card Hover Effect */
.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.pointer {
  cursor: pointer;
}
</style>