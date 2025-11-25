<template>
  <div class="dashboard-body">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom shadow-sm sticky-top">
      <div class="container-fluid px-4">
        <span class="navbar-brand fw-bold fs-4">
          <i class="fas fa-procedures me-2"></i> Patient Dashboard
        </span>

        <div class="d-flex align-items-center text-white gap-3">
          <div class="d-none d-md-block text-end me-3">
            <small class="text-white-50">Welcome,</small><br />
            <span class="fw-bold">{{ patientName }}</span>
          </div>

          <div class="btn-group">
            <button class="btn btn-outline-light btn-sm" @click="openProfileModal">
              <i class="fas fa-user-edit me-1"></i> Profile
            </button>
            <button class="btn btn-outline-light btn-sm" @click="fetchHistory">
              <i class="fas fa-history me-1"></i> History
            </button>
            <button class="btn btn-danger btn-sm" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="container-fluid px-4 py-4">
      <div v-if="currentView === 'home'" class="row g-4">
        <div class="col-lg-5 col-xl-4">
          <div class="card shadow border-0 h-100">
            <div class="card-header bg-indigo text-white py-3">
              <h5 class="mb-0 fw-bold"><i class="fas fa-hospital-alt me-2"></i> Departments</h5>
            </div>
            <div class="card-body bg-light">
              <div class="list-group list-group-flush gap-2">
                <div
                  v-for="dept in departments"
                  :key="dept.department_id"
                  class="list-group-item border-0 shadow-sm rounded d-flex justify-content-between align-items-center p-3"
                >
                  <div class="d-flex align-items-center">
                    <div
                      class="bg-indigo-soft text-indigo rounded-circle d-flex align-items-center justify-content-center me-3"
                      style="width: 40px; height: 40px"
                    >
                      <i class="fas fa-clinic-medical"></i>
                    </div>
                    <span class="fw-bold text-dark">{{ dept.department_name }}</span>
                  </div>
                  <button
                    class="btn btn-sm btn-indigo rounded-pill px-3"
                    @click="viewDepartment(dept)"
                  >
                    View
                  </button>
                </div>
                <div v-if="departments.length === 0" class="text-center text-muted py-4">
                  <i class="fas fa-exclamation-circle me-1"></i> No departments found.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-7 col-xl-8">
          <div class="card shadow border-0 h-100">
            <div class="card-header bg-teal text-white py-3">
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-calendar-alt me-2"></i> Upcoming Appointments
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-striped table-hover mb-0 align-middle">
                  <thead class="bg-light text-uppercase small text-muted">
                    <tr>
                      <th class="ps-4 py-3">#</th>
                      <th class="py-3">Doctor</th>
                      <th class="py-3">Department</th>
                      <th class="py-3">Schedule</th>
                      <th class="text-center py-3">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(appt, index) in upcomingAppointments" :key="appt.appointment_id">
                      <td class="ps-4 fw-bold text-muted">{{ index + 1 }}</td>
                      <td class="fw-bold text-dark">Dr. {{ appt.doctor_name }}</td>
                      <td>
                        <span class="badge bg-light text-dark border">{{ appt.department }}</span>
                      </td>
                      <td>
                        <div class="small fw-bold">{{ appt.date }}</div>
                        <div class="small text-muted">{{ appt.time }}</div>
                      </td>
                      <td class="text-center">
                        <button
                          class="btn btn-danger btn-sm px-3"
                          @click="cancelAppointment(appt.appointment_id)"
                        >
                          <i class="fas fa-times"></i> Cancel
                        </button>
                      </td>
                    </tr>
                    <tr v-if="upcomingAppointments.length === 0">
                      <td class="text-center py-5 text-muted" colspan="6">
                        <div class="mb-2">
                          <i class="far fa-calendar-check fa-2x opacity-25"></i>
                        </div>
                        No upcoming appointments.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'department'">
        <div class="card shadow border-0">
          <div
            class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center"
          >
            <div>
              <small class="text-muted text-uppercase fw-bold">Department</small>
              <h4 class="mb-0 fw-bold text-indigo">{{ selectedDepartment.department_name }}</h4>
            </div>
            <button class="btn btn-outline-dark" @click="goHome">
              <i class="fas fa-arrow-left me-2"></i> Back to Dashboard
            </button>
          </div>
          <div class="card-body p-4">
            <div class="alert alert-light border-start border-4 border-indigo shadow-sm mb-4">
              <h6 class="fw-bold text-dark">Overview</h6>
              <p class="mb-0 text-secondary">
                {{ selectedDepartment.description || 'No description available.' }}
              </p>
            </div>

            <h5 class="fw-bold mb-3 border-bottom pb-2">Available Doctors</h5>
            <div class="row g-3">
              <div v-for="doc in departmentDoctors" :key="doc.user_id" class="col-md-6 col-xl-4">
                <div class="card h-100 border shadow-sm">
                  <div class="card-body d-flex align-items-center">
                    <div
                      class="bg-light rounded-circle d-flex align-items-center justify-content-center me-3 border"
                      style="width: 60px; height: 60px"
                    >
                      <i class="fas fa-user-md fa-lg text-secondary"></i>
                    </div>
                    <div class="flex-grow-1">
                      <h6 class="fw-bold mb-1">Dr. {{ doc.name }}</h6>
                      <small class="text-muted d-block mb-2">{{ doc.qualification }}</small>
                    </div>
                  </div>
                  <div class="card-footer bg-white border-top-0 d-flex gap-2">
                    <button class="btn btn-primary btn-sm w-100" @click="viewAvailability(doc)">
                      Book Appointment
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm w-100"
                      @click="viewDoctorProfile(doc.user_id)"
                    >
                      Profile
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="departmentDoctors.length === 0" class="col-12 text-center text-muted py-4">
                No doctors found in this department.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'doctor'">
        <div class="row justify-content-center">
          <div class="col-lg-10 col-xl-8">
            <div class="card shadow border-0">
              <div class="card-header bg-white border-0 pt-4 ps-4">
                <button
                  class="btn btn-link text-decoration-none text-secondary p-0"
                  @click="currentView = 'department'"
                >
                  <i class="fas fa-arrow-left me-1"></i> Back to Department
                </button>
              </div>
              <div class="card-body p-5">
                <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
                  <div
                    class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center shadow"
                    style="width: 120px; height: 120px; font-size: 3rem"
                  >
                    <i class="fas fa-user-md"></i>
                  </div>
                  <div class="text-center text-md-start">
                    <h2 class="fw-bold mb-1">Dr. {{ selectedDoctor.name }}</h2>
                    <span class="badge bg-indigo mb-2">{{ selectedDoctor.department }}</span>
                    <div class="text-muted">{{ selectedDoctor.qualification }}</div>
                  </div>
                  <div class="ms-md-auto">
                    <button
                      class="btn btn-lg btn-success px-5 shadow-sm"
                      @click="viewAvailability(selectedDoctor)"
                    >
                      <i class="fas fa-calendar-check me-2"></i> Book Now
                    </button>
                  </div>
                </div>

                <div class="row g-4">
                  <div class="col-md-6">
                    <div class="p-3 border rounded bg-light h-100">
                      <h6 class="fw-bold text-dark border-bottom pb-2">Professional Details</h6>
                      <p class="mb-1">
                        <strong>Experience:</strong> {{ selectedDoctor.experience_years }} Years
                      </p>
                      <p class="mb-0">
                        <strong>Specialization:</strong> {{ selectedDoctor.department }}
                      </p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="p-3 border rounded bg-light h-100">
                      <h6 class="fw-bold text-dark border-bottom pb-2">Contact Information</h6>
                      <p class="mb-1">
                        <i class="fas fa-envelope me-2 text-muted"></i> {{ selectedDoctor.email }}
                      </p>
                      <p class="mb-0">
                        <i class="fas fa-phone me-2 text-muted"></i> {{ selectedDoctor.phone }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="availabilityModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-bold">
              <i class="fas fa-calendar-alt me-2"></i> Select a Slot
            </h5>
            <button
              class="btn-close btn-close-white"
              type="button"
              @click="hideModal('availabilityModal')"
            ></button>
          </div>
          <div class="modal-body bg-light p-4">
            <div v-if="availabilityList.length > 0">
              <p class="text-muted mb-3">Showing availability for next 7 days:</p>
              <div
                v-for="(day, idx) in availabilityList"
                :key="idx"
                class="row mb-3 align-items-center bg-white p-2 border rounded shadow-sm mx-0"
              >
                <div class="col-md-3 border-end">
                  <div class="fw-bold text-dark text-center">{{ day.date }}</div>
                </div>

                <div class="col-md-9">
                  <div class="d-flex gap-2">
                    <button
                      :class="getSlotClass(day, 'morning')"
                      :disabled="!day.morning.available"
                      class="btn flex-grow-1"
                      @click="selectSlot(day, 'morning')"
                    >
                      <i class="fas fa-sun me-1"></i> {{ day.morning.time }}
                    </button>
                    <button
                      :class="getSlotClass(day, 'evening')"
                      :disabled="!day.evening.available"
                      class="btn flex-grow-1"
                      @click="selectSlot(day, 'evening')"
                    >
                      <i class="fas fa-moon me-1"></i> {{ day.evening.time }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-5 text-muted">
              <div class="spinner-border text-primary mb-2" role="status"></div>
              <p>Loading schedule...</p>
            </div>

            <div
              v-if="selectedSlot"
              class="alert alert-success d-flex justify-content-between align-items-center mt-3 mb-0 shadow-sm"
            >
              <div>
                <i class="fas fa-check-circle me-2"></i>
                <strong>Selected:</strong> {{ selectedSlot.date }} at {{ selectedSlot.time }}
              </div>
              <button class="btn btn-success fw-bold px-4" @click="bookAppointment">
                Confirm Booking
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="historyModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-xl modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title fw-bold">
              <i class="fas fa-file-medical-alt me-2"></i> Medical History
            </h5>
            <div class="d-flex gap-2">
              <button class="btn btn-success btn-sm" @click="exportCSV">
                <i class="fas fa-file-csv me-1"></i> Export CSV
              </button>
              <button class="btn btn-light btn-sm text-dark" @click="hideModal('historyModal')">
                Close
              </button>
            </div>
          </div>
          <div class="modal-body p-0">
            <div class="table-responsive">
              <table class="table table-striped mb-0">
                <thead class="bg-light text-uppercase small">
                  <tr>
                    <th>#</th>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(visit, idx) in patientHistory" :key="idx">
                    <td class="fw-bold text-muted">{{ idx + 1 }}</td>
                    <td>{{ visit.date }}</td>
                    <td class="text-primary fw-bold">{{ visit.doctor_name }}</td>
                    <td>{{ visit.diagnosis }}</td>
                    <td>{{ visit.prescription }}</td>
                    <td class="small text-muted">{{ visit.notes }}</td>
                  </tr>
                  <tr v-if="patientHistory.length === 0">
                    <td class="text-center py-5 text-muted" colspan="6">
                      <i class="fas fa-box-open fa-2x mb-2 opacity-25"></i>
                      <p>No history records found.</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="profileModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title"><i class="fas fa-user-cog me-2"></i> Edit Profile</h5>
            <button
              class="btn-close btn-close-white"
              type="button"
              @click="hideModal('profileModal')"
            ></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary">Full Name</label>
                <input v-model="profileForm.name" class="form-control" required type="text" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary">Phone Number</label>
                <input v-model="profileForm.phone" class="form-control" type="text" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary">Date of Birth</label>
                <input v-model="profileForm.date_of_birth" class="form-control" type="date" />
              </div>
              <div class="mb-4">
                <label class="form-label fw-bold text-secondary">Address</label>
                <textarea v-model="profileForm.address" class="form-control" rows="3"></textarea>
              </div>
              <button class="btn btn-primary w-100 py-2 fw-bold" type="submit">Save Changes</button>
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
      profileForm: { name: '', phone: '', address: '', date_of_birth: '' },

      modals: {},
    }
  },
  methods: {
    getToken() {
      return localStorage.getItem('patientToken')
    },
    async apiRequest(endpoint, method = 'GET', body = null) {
      try {
        const headers = {
          Authorization: `Bearer ${this.getToken()}`,
          'Content-Type': 'application/json',
        }
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

      if (isSelected) return 'btn-success text-white'
      if (slotInfo.available) return 'btn-outline-success'
      return 'btn-secondary disabled opacity-50'
    },

    selectSlot(day, type) {
      const slotInfo = day[type]
      this.selectedSlot = {
        id: `${day.date}_${slotInfo.time}`,
        date: day.date,
        raw_date: day.raw_date,
        time: slotInfo.time,
      }
    },

    async bookAppointment() {
      if (!this.selectedSlot || !this.selectedDoctor.user_id) return

      const payload = {
        doctor_id: this.selectedDoctor.user_id,
        date: this.selectedSlot.raw_date,
        time: this.selectedSlot.time,
      }

      const res = await this.apiRequest('/patient/book_appointment', 'POST', payload)
      if (res) {
        alert(res.message)
        this.hideModal('availabilityModal')
        this.goHome()
      }
    },

    async cancelAppointment(id) {
      if (!confirm('Cancel this appointment?')) return
      const res = await this.apiRequest(`/patient/appointments/${id}`, 'DELETE')
      if (res) {
        alert('Appointment cancelled')
        this.fetchDashboardData()
      }
    },

    async fetchHistory() {
      const appts = await this.apiRequest('/patient/appointments?upcoming_only=false')
      if (appts) {
        this.patientHistory = appts.appointments.filter((a) => a.status === 'Completed')
        this.showModal('historyModal')
      }
    },

    async exportCSV() {
      const token = this.getToken()
      const response = await fetch('/api/patient/history/export_csv', {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'patient_history.csv'
        document.body.appendChild(a)
        a.click()
        a.remove()
      } else {
        alert('Failed to download CSV')
      }
    },

    openProfileModal() {
      this.showModal('profileModal')
    },
    async updateProfile() {
      const res = await this.apiRequest('/patient/profile', 'PUT', this.profileForm)
      if (res) {
        alert('Profile updated')
        this.patientName = this.profileForm.name
        this.hideModal('profileModal')
      }
    },

    showModal(id) {
      const el = document.getElementById(id)
      if (el && window.bootstrap) {
        this.modals[id] = new window.bootstrap.Modal(el, { backdrop: 'static' })
        this.modals[id].show()
      }
    },
    hideModal(id) {
      if (this.modals[id]) {
        this.modals[id].hide()
        this.modals[id] = null
      }
      setTimeout(() => {
        document.querySelectorAll('.modal-backdrop').forEach((e) => e.remove())
        document.body.classList.remove('modal-open')
        document.body.style = ''
      }, 200)
    },

    logout() {
      localStorage.removeItem('patientToken')
      this.$router.push('/patient-login')
    },
  },
  mounted() {
    if (!this.getToken()) {
      this.$router.push('/patient-login')
    } else {
      this.fetchDashboardData()
    }
  },
}
</script>

<style scoped>
.dashboard-body {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.bg-indigo {
  background-color: #6610f2;
}
.text-indigo {
  color: #6610f2;
}
.btn-indigo {
  background-color: #6610f2;
  color: white;
}
.btn-indigo:hover {
  background-color: #520dc2;
  color: white;
}
.bg-indigo-soft {
  background-color: rgba(102, 16, 242, 0.1);
}

.bg-teal {
  background-color: #20c997;
}
.text-teal {
  color: #20c997;
}

.card {
  transition: none;
}
</style>
