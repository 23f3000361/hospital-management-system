<template>
  <div class="dashboard-body">
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm sticky-top">
      <div class="container-fluid px-4">
        <span class="navbar-brand fw-bold fs-4">
          Welcome, {{ patientName }}
        </span>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-link text-decoration-none text-dark" @click="openProfileModal">
            Edit Profile
          </button>
          <span class="text-muted">|</span>
          <button class="btn btn-link text-decoration-none text-dark" @click="fetchHistory">
            History
          </button>
          <span class="text-muted">|</span>
          <button class="btn btn-link text-decoration-none text-danger fw-bold" @click="logout">
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container py-4">
      <div v-if="currentView === 'home'">
        <div class="card shadow-sm mb-4 border-dark">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0 fw-bold">Departments</h5>
          </div>
          <div class="card-body">
            <div class="list-group">
              <div v-for="dept in departments" :key="dept.department_id"
                   class="list-group-item d-flex justify-content-between align-items-center border mb-2 rounded">
                <span class="fw-bold text-secondary">{{ dept.department_name }}</span>
                <button class="btn btn-outline-primary btn-sm px-4 rounded-pill" @click="viewDepartment(dept)">
                  View Details
                </button>
              </div>
              <div v-if="departments.length === 0" class="text-center text-muted py-3">No departments found.</div>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-dark">
          <div class="card-header bg-white border-bottom">
            <h5 class="mb-0 fw-bold">Upcoming Appointments</h5>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-bordered mb-0 align-middle">
                <thead class="table-light">
                <tr>
                  <th class="ps-4">Sr No.</th>
                  <th>Doctor Name</th>
                  <th>Deptt</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th class="text-center">Action</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(appt, index) in upcomingAppointments" :key="appt.appointment_id">
                  <td class="ps-4 fw-bold text-muted">{{ index + 1 }}.</td>
                  <td>Dr. {{ appt.doctor_name }}</td>
                  <td>{{ appt.department }}</td>
                  <td>{{ appt.date }}</td>
                  <td>{{ appt.time }}</td>
                  <td class="text-center">
                    <button class="btn btn-outline-danger btn-sm px-3" @click="cancelAppointment(appt.appointment_id)">
                      Cancel
                    </button>
                  </td>
                </tr>
                <tr v-if="upcomingAppointments.length === 0">
                  <td class="text-center py-4 text-muted" colspan="6">No upcoming appointments.</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'department'">
        <div class="card shadow-sm border-dark">
          <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center">
            <h5 class="mb-0 fw-bold">Department of {{ selectedDepartment.department_name }}</h5>
            <div class="d-flex gap-2">
              <button class="btn btn-link text-decoration-none" @click="goHome">Back</button>
              <button class="btn btn-link text-decoration-none text-danger" @click="logout">Logout</button>
            </div>
          </div>
          <div class="card-body">
            <div class="mb-4">
              <h6 class="fw-bold">Overview</h6>
              <p class="text-muted small">{{ selectedDepartment.description || 'No description available for this department.' }}</p>
            </div>

            <h6 class="fw-bold mb-3">Doctors' list</h6>
            <div class="list-group">
              <div v-for="doc in departmentDoctors" :key="doc.user_id"
                   class="list-group-item d-flex justify-content-between align-items-center border mb-2 rounded">
                <span class="fw-bold text-secondary">Dr. {{ doc.name }}</span>
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-primary btn-sm px-3" @click="viewAvailability(doc)">
                    Check Availability
                  </button>
                  <button class="btn btn-outline-secondary btn-sm px-3" @click="viewDoctorProfile(doc.user_id)">
                    View Details
                  </button>
                </div>
              </div>
              <div v-if="departmentDoctors.length === 0" class="text-center text-muted py-3">
                No doctors found in this department.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'doctor'">
        <div class="card shadow-sm border-dark mx-auto" style="max-width: 800px;">
          <div class="card-body p-5 d-flex gap-4">
            <div class="flex-grow-1">
              <h3 class="fw-bold text-dark mb-1">Dr. {{ selectedDoctor.name }}</h3>
              <div class="text-muted mb-3">{{ selectedDoctor.qualification }}</div>

              <div class="mb-2">
                <strong>Department:</strong> {{ selectedDoctor.department }}
              </div>
              <div class="mb-3">
                <strong>Experience:</strong> {{ selectedDoctor.experience_years }} Years Overall
              </div>

              <p class="text-muted small">
                Dr. {{ selectedDoctor.name }} is a specialist in {{ selectedDoctor.department }}.
                Contact: {{ selectedDoctor.email }} | {{ selectedDoctor.phone }}
              </p>

              <div class="mt-4 d-flex gap-3">
                <button class="btn btn-outline-primary px-4" @click="viewAvailability(selectedDoctor)">
                  Check Availability
                </button>
                <button class="btn btn-outline-secondary px-4" @click="currentView = 'department'">
                  Go Back
                </button>
              </div>
            </div>

            <div class="d-flex align-items-start">
              <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center text-white"
                   style="width: 120px; height: 120px; font-size: 3rem;">
                <i class="fas fa-user"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <div id="availabilityModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-dark">
          <div class="modal-header bg-white border-bottom">
            <h5 class="modal-title fw-bold">Doctor's Availability</h5>
            <button class="btn-close" type="button" @click="hideModal('availabilityModal')"></button>
          </div>
          <div class="modal-body bg-light">
            <div v-if="availabilityList.length > 0">
              <div v-for="(day, idx) in availabilityList" :key="idx" class="row mb-2 align-items-center">
                <div class="col-4">
                  <div class="form-control text-center border-dark bg-white fw-bold">
                    {{ day.date }}
                  </div>
                </div>

                <div class="col-4">
                  <button :class="getSlotClass(day, 'morning')"
                          :disabled="!day.morning.available"
                          class="btn w-100 btn-sm"
                          @click="selectSlot(day, 'morning')"
                  >
                    {{ day.morning.time }}
                  </button>
                </div>
                <div class="col-4">
                  <button :class="getSlotClass(day, 'evening')"
                          :disabled="!day.evening.available"
                          class="btn w-100 btn-sm"
                          @click="selectSlot(day, 'evening')"
                  >
                    {{ day.evening.time }}
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-3">Loading schedule...</div>

            <div v-if="selectedSlot" class="mt-3 text-end">
               <span class="text-success fw-bold me-3">
                 Selected: {{ selectedSlot.date }} at {{ selectedSlot.time }}
               </span>
              <button class="btn btn-success px-4" @click="bookAppointment">Book</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="historyModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content border-dark">
          <div class="modal-header bg-white">
            <h5 class="modal-title fw-bold">Patient History</h5>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-success btn-sm" @click="exportCSV">Export as CSV</button>
              <button class="btn btn-outline-primary btn-sm" @click="hideModal('historyModal')">Back</button>
            </div>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <strong>Patient Name:</strong> {{ patientName }}
            </div>
            <div class="table-responsive border">
              <table class="table table-bordered mb-0">
                <thead class="table-light">
                <tr>
                  <th>Visit No.</th>
                  <th>Date</th>
                  <th>Doctor</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Medicines</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(visit, idx) in patientHistory" :key="idx">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ visit.date }}</td>
                  <td>{{ visit.doctor_name }}</td>
                  <td>{{ visit.diagnosis }}</td>
                  <td>{{ visit.prescription }}</td>
                  <td>{{ visit.notes }}</td>
                </tr>
                <tr v-if="patientHistory.length === 0">
                  <td class="text-center text-muted" colspan="6">No history records found.</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="profileModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Profile</h5>
            <button class="btn-close" type="button" @click="hideModal('profileModal')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input v-model="profileForm.name" class="form-control" required type="text">
              </div>
              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input v-model="profileForm.phone" class="form-control" type="text">
              </div>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <textarea v-model="profileForm.address" class="form-control" rows="2"></textarea>
              </div>
              <button class="btn btn-primary w-100" type="submit">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'PatientDashboard',
  data() {
    return {
      currentView: 'home',
      patientName: 'Patient',
      departments: [],
      upcomingAppointments: [],
      selectedDepartment: {},
      departmentDoctors: [],
      selectedDoctor: {},
      availabilityList: [],
      selectedSlot: null,
      patientHistory: [],
      profileForm: { name: '', phone: '', address: '' },
      modals: {}
    }
  },
  methods: {
    getToken() {
      return localStorage.getItem('patientToken')
    },
    async apiRequest(endpoint, method = 'GET', body = null) {
      try {
        const headers = { 'Authorization': `Bearer ${this.getToken()}`, 'Content-Type': 'application/json' }
        const options = { method, headers }
        if (body) options.body = JSON.stringify(body)
        const res = await fetch(`/api${endpoint}`, options)
        const data = await res.json()
        if (!res.ok) throw new Error(data.message || 'Request failed')
        return data
      } catch (error) {
        alert(error.message)
        return null
      }
    },
    async fetchDashboardData() {
      const profile = await this.apiRequest('/patient/profile')
      if (profile) {
        this.patientName = profile.name
        this.profileForm = { ...profile }
      }
      const depts = await this.apiRequest('/departments')
      if (depts) this.departments = depts.departments
      const appts = await this.apiRequest('/patient/appointments?upcoming_only=true')
      if (appts) this.upcomingAppointments = appts.appointments
    },
    async viewDepartment(dept) {
      this.selectedDepartment = dept
      const data = await this.apiRequest(`/departments/${dept.department_id}/doctors`)
      if (data) {
        this.departmentDoctors = data.doctors
        this.currentView = 'department'
      }
    },
    async viewDoctorProfile(id) {
      const data = await this.apiRequest(`/doctors/${id}`)
      if (data) {
        this.selectedDoctor = data
        this.currentView = 'doctor'
      }
    },
    goHome() {
      this.currentView = 'home'
      this.fetchDashboardData()
    },
    async viewAvailability(doctor) {
      if (!doctor.user_id && doctor.id) doctor.user_id = doctor.id
      this.selectedDoctor = doctor
      this.availabilityList = []
      this.selectedSlot = null
      this.showModal('availabilityModal')
      const data = await this.apiRequest(`/patient/doctor_availability/${doctor.user_id}`)
      if (data) {
        this.availabilityList = data.availability
      }
    },
    getSlotClass(day, type) {
      const slotInfo = day[type]
      const slotId = `${day.date}_${slotInfo.time}`
      const isSelected = this.selectedSlot && this.selectedSlot.id === slotId
      if (isSelected) return 'btn-primary text-white'
      if (slotInfo.available) return 'btn-outline-success'
      return 'btn-outline-danger'
    },
    selectSlot(day, type) {
      const slotInfo = day[type]
      this.selectedSlot = {
        id: `${day.date}_${slotInfo.time}`,
        date: day.date,
        raw_date: day.raw_date,
        time: slotInfo.time
      }
    },
    async bookAppointment() {
      if (!this.selectedSlot || !this.selectedDoctor.user_id) return
      const payload = {
        doctor_id: this.selectedDoctor.user_id,
        date: this.selectedSlot.raw_date,
        time: this.selectedSlot.time
      }
      const res = await this.apiRequest('/patient/book_appointment', 'POST', payload)
      if (res) {
        alert(res.message)
        this.hideModal('availabilityModal')
        this.goHome()
      }
    },
    async cancelAppointment(id) {
      if(!confirm("Cancel this appointment?")) return
      const res = await this.apiRequest(`/patient/appointments/${id}`, 'DELETE')
      if(res) {
        alert("Appointment cancelled")
        this.fetchDashboardData()
      }
    },
    async fetchHistory() {
      const data = await this.apiRequest('/patient/history/export_csv')
      const appts = await this.apiRequest('/patient/appointments?upcoming_only=false')
      if (appts) {
        this.patientHistory = appts.appointments.filter(a => a.status === 'Completed')
        this.showModal('historyModal')
      }
    },
    async exportCSV() {
      const token = this.getToken()
      const response = await fetch('/api/patient/history/export_csv', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if(response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'patient_history.csv'
        document.body.appendChild(a)
        a.click()
        a.remove()
      } else {
        alert("Failed to download CSV")
      }
    },
    openProfileModal() {
      this.showModal('profileModal')
    },
    async updateProfile() {
      const res = await this.apiRequest('/patient/profile', 'PUT', this.profileForm)
      if (res) {
        alert("Profile updated")
        this.patientName = this.profileForm.name
        this.hideModal('profileModal')
      }
    },
    showModal(id) {
      const el = document.getElementById(id)
      if(el && window.bootstrap) {
        this.modals[id] = new window.bootstrap.Modal(el, {backdrop: 'static'})
        this.modals[id].show()
      }
    },
    hideModal(id) {
      if(this.modals[id]) {
        this.modals[id].hide()
        this.modals[id] = null
      }
      setTimeout(() => {
        document.querySelectorAll('.modal-backdrop').forEach(e => e.remove())
        document.body.classList.remove('modal-open')
        document.body.style = ''
      }, 200)
    },
    logout() {
      localStorage.removeItem('patientToken')
      this.$router.push('/patient-login')
    }
  },
  mounted() {
    if (!this.getToken()) {
      this.$router.push('/patient-login')
    } else {
      this.fetchDashboardData()
    }
  }
}
</script>

<style scoped>
.dashboard-body {
  background-color: #fff;
  min-height: 100vh;
  border-top: 5px solid #333;
}
.card {
  border-radius: 0 !important;
}
</style>
