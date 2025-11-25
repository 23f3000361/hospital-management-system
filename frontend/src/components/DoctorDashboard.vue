<template>
  <div class="dashboard-body">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container-fluid px-4">
        <span class="navbar-brand fw-bold fs-3">
          <i class="fas fa-user-md me-2"></i> Doctor Dashboard
        </span>
        <div class="d-flex align-items-center text-white">
          <div class="me-3 text-end d-none d-md-block">
            <small class="text-white-50">Logged in as</small><br>
            <span class="fw-bold">Dr. {{ doctorName }}</span>
          </div>
          <button class="btn btn-danger rounded-pill px-4" @click="logout">
            <i class="fas fa-sign-out-alt me-1"></i> Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container py-5">

      <!-- Section 1: Upcoming Appointments -->
      <div class="card shadow mb-5 border-0 rounded-3">
        <div class="card-header bg-primary text-white py-3 rounded-top-3">
          <h5 class="mb-0 fw-bold"><i class="fas fa-calendar-day me-2"></i> Upcoming Appointments</h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-striped table-hover mb-0 align-middle">
              <thead class="table-light">
              <tr class="text-uppercase small">
                <th class="ps-4 py-3">#</th>
                <th class="py-3">Patient Name</th>
                <th class="py-3">Details</th>
                <th class="text-end pe-4 py-3">Actions</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(appt, index) in appointments" :key="appt.appointment_id">
                <td class="ps-4 fw-bold text-muted">{{ index + 1 }}</td>
                <td>
                  <div class="fw-bold text-dark">{{ appt.patient_name }}</div>
                  <span class="badge bg-light text-dark border mt-1">
                      <i class="far fa-clock me-1"></i> {{ appt.time }} on {{ appt.date }}
                    </span>
                </td>
                <td>
                  <button
                      class="btn btn-info btn-sm text-white rounded-pill px-3"
                      @click="viewHistory(appt.patient_id)"
                  >
                    <i class="fas fa-file-medical me-1"></i> View History
                  </button>
                </td>
                <td class="text-end pe-4">
                  <div class="d-inline-flex gap-2">
                    <button
                        class="btn btn-outline-primary btn-sm"
                        @click="openCompleteModal(appt)"
                    >
                      <i class="fas fa-edit"></i> Update
                    </button>
                    <button
                        class="btn btn-success btn-sm text-white"
                        @click="openCompleteModal(appt)"
                    >
                      <i class="fas fa-check-circle me-1"></i> Complete
                    </button>
                    <button
                        class="btn btn-outline-danger btn-sm"
                        @click="cancelAppointment(appt.appointment_id)"
                    >
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="appointments.length === 0">
                <td class="text-center py-5 text-muted" colspan="4">
                  <div class="mb-2"><i class="fas fa-calendar-check fa-2x opacity-25"></i></div>
                  <h6 class="fw-normal">No upcoming appointments scheduled.</h6>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Section 2: Assigned Patients -->
        <div class="col-lg-7">
          <div class="card shadow border-0 h-100 rounded-3">
            <div class="card-header bg-success text-white py-3 rounded-top-3">
              <h5 class="mb-0 fw-bold"><i class="fas fa-users me-2"></i> Assigned Patients</h5>
            </div>
            <div class="card-body p-0">
              <ul class="list-group list-group-flush">
                <li
                    v-for="patient in assignedPatients"
                    :key="patient.patient_id"
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center px-4 py-3"
                >
                  <div class="d-flex align-items-center">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center me-3 text-success border" style="width:45px; height:45px">
                      <i class="fas fa-user"></i>
                    </div>
                    <div>
                      <h6 class="mb-0 fw-bold">{{ patient.name }}</h6>
                      <small class="text-muted"><i class="fas fa-envelope me-1"></i> {{ patient.email }}</small>
                    </div>
                  </div>
                  <button
                      class="btn btn-outline-success btn-sm rounded-pill px-3"
                      @click="viewHistory(patient.patient_id)"
                  >
                    View Profile
                  </button>
                </li>
                <li v-if="assignedPatients.length === 0" class="list-group-item text-center text-muted py-5 border-0">
                  No patients assigned yet.
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Section 3: Availability -->
        <div class="col-lg-5">
          <div class="card shadow border-0 h-100 rounded-3">
            <div class="card-header bg-dark text-white py-3 rounded-top-3 d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold"><i class="fas fa-clock me-2"></i> Availability</h5>
              <span class="badge bg-secondary border border-secondary">Next 7 Days</span>
            </div>
            <div class="card-body bg-light">
              <div v-for="(day, index) in availability" :key="index" class="row mb-2 g-2 align-items-center">
                <!-- Date Box -->
                <div class="col-3">
                  <div class="bg-white border rounded text-center py-2 shadow-sm">
                    <strong class="d-block text-dark">{{ day.date.split('/')[0] }}/{{ day.date.split('/')[1] }}</strong>
                  </div>
                </div>
                <!-- Morning Slot -->
                <div class="col-4">
                  <button
                      :class="day.morning ? 'btn-outline-success' : 'btn-outline-danger'"
                      class="btn w-100 btn-sm fw-bold"
                      @click="toggleAvailability(index, 'morning')"
                  >
                    <!-- Updated Text -->
                    {{ day.morning ? '08:00 am - 12:00 pm' : 'Unavailable' }}
                  </button>
                </div>

                <!-- Evening Slot -->
                <div class="col-4">
                  <button
                      :class="day.evening ? 'btn-outline-success' : 'btn-outline-danger'"
                      class="btn w-100 btn-sm fw-bold"
                      @click="toggleAvailability(index, 'evening')"
                  >
                    <!-- Updated Text (Converted to 12h format with pm) -->
                    {{ day.evening ? '04:00 pm - 09:00 pm' : 'Unavailable' }}
                  </button>
                </div>
              </div>
            </div>
            <div class="card-footer bg-white p-3 text-end">
              <button class="btn btn-dark px-4 fw-bold" @click="saveAvailability">
                <i class="fas fa-save me-2"></i> Save Schedule
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Complete Modal -->
    <div id="completeModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title"><i class="fas fa-stethoscope me-2"></i> Update Medical Record</h5>
            <button class="btn-close btn-close-white" type="button" @click="hideActiveModal"></button>
          </div>
          <div class="modal-body p-4">
            <div class="alert alert-primary d-flex align-items-center mb-4">
              <i class="fas fa-user-circle fa-2x me-3"></i>
              <div>
                <small class="text-uppercase fw-bold" style="font-size: 0.7rem">Patient Name</small>
                <h5 class="mb-0 fw-bold">{{ activeAppt?.patient_name }}</h5>
              </div>
            </div>

            <form @submit.prevent="submitComplete">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold text-secondary">Visit Type</label>
                  <input class="form-control bg-light" readonly type="text" value="In-person">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold text-secondary">Tests Conducted</label>
                  <input v-model="completionForm.tests" class="form-control" placeholder="e.g. Blood Pressure" type="text">
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold text-secondary">Diagnosis</label>
                <input v-model="completionForm.diagnosis" class="form-control" placeholder="Primary diagnosis..." required type="text">
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold text-secondary">Prescription</label>
                  <textarea v-model="completionForm.prescription" class="form-control" placeholder="Medication details..." required rows="4"></textarea>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold text-secondary">Notes & Advice</label>
                  <textarea v-model="completionForm.notes" class="form-control" placeholder="Diet, Exercise, Follow-up..." required rows="4"></textarea>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                <button class="btn btn-light border px-4" type="button" @click="hideActiveModal">Close</button>
                <button class="btn btn-success px-4 fw-bold" type="submit">
                  <i class="fas fa-save me-2"></i> Save Record
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- History Modal -->
    <div id="historyModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-xl modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title fw-bold"><i class="fas fa-history me-2"></i> Patient History</h5>
            <button class="btn-close btn-close-white" type="button" @click="hideActiveModal"></button>
          </div>
          <div class="modal-body bg-light">
            <div v-if="patientHistory" class="card shadow-sm border-0 mb-3">
              <div class="card-body">
                <h4 class="fw-bold text-dark mb-0">{{ patientHistory.patient_name }}</h4>
                <small class="text-muted">Medical Record Archive</small>
              </div>
            </div>

            <div class="table-responsive card shadow-sm border-0">
              <table class="table table-bordered mb-0">
                <thead class="bg-light text-secondary">
                <tr>
                  <th style="width: 15%">Date</th>
                  <th style="width: 20%">Doctor</th>
                  <th style="width: 20%">Diagnosis</th>
                  <th style="width: 25%">Prescription</th>
                  <th style="width: 20%">Notes</th>
                </tr>
                </thead>
                <tbody v-if="patientHistory && patientHistory.history.length > 0" class="bg-white">
                <tr v-for="(entry, idx) in patientHistory.history" :key="idx">
                  <td class="fw-bold text-muted">{{ entry.date }}</td>
                  <td class="text-primary fw-bold">{{ entry.doctor_name }}</td>
                  <td>{{ entry.diagnosis }}</td>
                  <td><div class="p-1 bg-light rounded border">{{ entry.prescription }}</div></td>
                  <td class="small text-muted">{{ entry.notes }}</td>
                </tr>
                </tbody>
                <tbody v-else class="bg-white">
                <tr>
                  <td class="text-center py-5 text-muted" colspan="5">
                    <i class="fas fa-folder-open fa-2x mb-3 opacity-25"></i>
                    <p>No medical history found for this patient.</p>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer bg-white">
            <button class="btn btn-secondary px-4" @click="hideActiveModal">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'DoctorDashboard',
  data() {
    return {
      doctorName: 'Doctor',
      appointments: [],
      assignedPatients: [],
      availability: [],
      activeAppt: null,
      completionForm: {
        tests: '',
        diagnosis: '',
        prescription: '',
        notes: ''
      },
      patientHistory: null,
      activeModal: null
    }
  },
  methods: {
    getToken() {
      return localStorage.getItem('doctorToken')
    },

    async apiRequest(endpoint, method = 'GET', body = null) {
      try {
        const headers = {
          'Authorization': `Bearer ${this.getToken()}`,
          'Content-Type': 'application/json'
        }
        const options = { method, headers }
        if (body) options.body = JSON.stringify(body)

        const response = await fetch(`/api${endpoint}`, options)
        const data = await response.json()

        if (!response.ok) throw new Error(data.message || 'Request failed')
        return data
      } catch (error) {
        alert(error.message)
        return null
      }
    },

    showModal(modalId) {
      if (this.activeModal) {
        this.activeModal.hide()
        this.activeModal = null
      }
      const el = document.getElementById(modalId)
      if (el && window.bootstrap) {
        this.activeModal = new window.bootstrap.Modal(el, { backdrop: 'static' })
        this.activeModal.show()
      }
    },

    hideActiveModal() {
      if (this.activeModal) {
        this.activeModal.hide()
        this.activeModal = null
      }
      setTimeout(() => {
        document.querySelectorAll('.modal-backdrop').forEach(e => e.remove())
        document.body.classList.remove('modal-open')
        document.body.style = ''
      }, 200)
    },

    async fetchDashboardData() {
      const profile = await this.apiRequest('/doctor/profile')
      if (profile) this.doctorName = profile.name

      const apptData = await this.apiRequest('/doctor/appointments')
      if (apptData) this.appointments = apptData.appointments

      const patData = await this.apiRequest('/doctor/assigned_patients')
      if (patData) this.assignedPatients = patData.assigned_patients

      const availData = await this.apiRequest('/doctor/availability')
      if (availData && availData.availability) {
        this.availability = availData.availability
      }
    },

    async cancelAppointment(id) {
      if (!confirm("Are you sure you want to cancel this appointment?")) return

      const idx = this.appointments.findIndex(a => a.appointment_id === id)
      if (idx !== -1) this.appointments.splice(idx, 1)

      const res = await this.apiRequest(`/doctor/appointments/${id}`, 'PUT')
      if (!res) await this.fetchDashboardData()
    },

    openCompleteModal(appt) {
      this.activeAppt = appt
      this.completionForm = { tests: '', diagnosis: '', prescription: '', notes: '' }
      this.showModal('completeModal')
    },

    async submitComplete() {
      if (!this.activeAppt) return

      const idx = this.appointments.findIndex(a => a.appointment_id === this.activeAppt.appointment_id)
      if (idx !== -1) this.appointments.splice(idx, 1)

      this.hideActiveModal()

      const payload = {
        appointment_id: this.activeAppt.appointment_id,
        diagnosis: this.completionForm.diagnosis,
        prescription: this.completionForm.prescription,
        notes: this.completionForm.notes
      }

      await this.apiRequest('/doctor/complete_appointment', 'POST', payload)
    },

    async viewHistory(patientId) {
      this.patientHistory = null
      const data = await this.apiRequest(`/doctor/patient_history/${patientId}`)
      if (data) {
        this.patientHistory = data
        this.showModal('historyModal')
      }
    },

    toggleAvailability(index, type) {
      this.availability[index][type] = !this.availability[index][type]
    },

    async saveAvailability() {
      const res = await this.apiRequest('/doctor/availability', 'POST', { availability: this.availability })
      if (res) alert("Availability schedule updated.")
    },

    logout() {
      localStorage.removeItem('doctorToken')
      this.$router.push('/doctor-login')
    }
  },
  mounted() {
    if (!this.getToken()) {
      this.$router.push('/doctor-login')
    } else {
      this.fetchDashboardData()
    }
  }
}
</script>

<style scoped>
.dashboard-body {
  background-color: #f4f6f9; /* Light gray background to make white cards pop */
  min-height: 100vh;
}
</style>