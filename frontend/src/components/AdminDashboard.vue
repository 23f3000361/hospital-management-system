<template>
  <div class="dashboard-body">
    <nav class="navbar navbar-expand-lg bg-dark border-bottom border-body" data-bs-theme="dark">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold fs-3" href="#">
          <i class="fas fa-user-shield me-2"></i> Admin Dashboard
        </a>
        <button class="btn btn-outline-light rounded-pill px-3" @click="logout">
          <i class="fas fa-sign-out-alt me-2"></i> Logout
        </button>
      </div>
    </nav>

    <div class="container-fluid p-4">
      <div class="p-4 mb-4 rounded-3 shadow-sm welcome-banner">
        <div class="container-fluid py-3">
          <h1 class="display-5 fw-bold">Welcome, Admin</h1>
          <div class="input-group">
            <input
              v-model="searchQuery"
              class="form-control form-control-lg"
              placeholder="Search for a doctor or patient by name or email..."
              type="text"
            />
            <span class="input-group-text bg-white"><i class="fas fa-search"></i></span>
          </div>
        </div>
      </div>

      <div class="row gy-4">
        <div class="col-lg-8">
          <!-- DEPARTMENTS SECTION -->
          <div class="card shadow-sm mb-4 border-0">
            <div
              class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
            >
              <h4 class="mb-0"><i class="fas fa-clinic-medical me-2"></i> Departments</h4>
              <button class="btn btn-light text-primary fw-bold" @click="openDepartmentModal">
                <i class="fas fa-plus me-2"></i> Add Department
              </button>
            </div>
            <div class="card-body">
              <div v-if="departments.length === 0" class="text-center text-muted py-3">
                No departments found. Please create one.
              </div>
              <div v-else class="row g-3">
                <div v-for="dept in departments" :key="dept.department_id" class="col-md-6">
                  <div
                    class="p-3 border rounded bg-light h-100 d-flex flex-column position-relative"
                  >
                    <!-- Edit Department Button -->
                    <button
                      class="btn btn-sm btn-outline-primary position-absolute top-0 end-0 m-2"
                      @click="openEditDepartmentModal(dept)"
                    >
                      <i class="fas fa-edit"></i>
                    </button>

                    <h5 class="fw-bold text-primary mb-1 pe-4">{{ dept.department_name }}</h5>
                    <small class="text-muted mb-2 flex-grow-1">{{
                      dept.description || 'No description provided.'
                    }}</small>
                    <div>
                      <span v-if="dept.head_doctor !== 'N/A'" class="badge bg-success">
                        <i class="fas fa-user-md me-1"></i> HOD: {{ dept.head_doctor }}
                      </span>
                      <span v-else class="badge bg-secondary">No HOD Assigned</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- DOCTORS SECTION -->
          <div class="card shadow-sm mb-4 border-0">
            <div
              class="card-header bg-success text-white d-flex justify-content-between align-items-center"
            >
              <h4 class="mb-0"><i class="fas fa-user-doctor me-2"></i> Registered Doctors</h4>
              <button class="btn btn-light text-success fw-bold" @click="openCreateDoctorModal">
                <i class="fas fa-plus me-2"></i> Create
              </button>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li
                  v-for="doctor in filteredDoctors"
                  :key="doctor.user_id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <span class="fw-bold">{{ doctor.name }}</span>
                    <span v-if="doctor.status === 'Inactive'" class="badge bg-danger ms-2"
                      >Blacklisted</span
                    >
                    <br />
                    <!-- ADDED EMAIL HERE -->
                    <small class="text-dark"
                      ><i class="fas fa-envelope me-1"></i> {{ doctor.email }}</small
                    >
                    <br />
                    <small class="text-muted">
                      <i class="fas fa-graduation-cap me-1"></i>
                      {{ doctor.qualification || 'Qualification not set' }}
                    </small>
                  </div>
                  <div class="d-flex gap-2">
                    <button
                      class="btn btn-outline-warning rounded-pill px-3"
                      @click="openEditDoctorModal(doctor)"
                    >
                      <i class="fas fa-edit"></i> Edit
                    </button>
                    <button
                      class="btn btn-outline-danger rounded-pill px-3"
                      @click="deleteUser(doctor, 'Doctor')"
                    >
                      <i class="fas fa-trash"></i> Delete
                    </button>
                    <button
                      v-if="doctor.status !== 'Inactive'"
                      class="btn btn-outline-dark rounded-pill px-3"
                      @click="blacklistUser(doctor, 'Doctor')"
                    >
                      <i class="fas fa-ban"></i> Blacklist
                    </button>
                    <button v-else class="btn btn-secondary rounded-pill px-3" disabled>
                      <i class="fas fa-ban"></i> Blacklisted
                    </button>
                  </div>
                </li>
                <li
                  v-if="filteredDoctors.length === 0"
                  class="list-group-item text-center text-muted"
                >
                  No doctors found.
                </li>
              </ul>
            </div>
          </div>

          <!-- PATIENTS SECTION -->
          <div class="card shadow-sm border-0">
            <div
              class="card-header bg-warning text-dark d-flex justify-content-between align-items-center"
            >
              <h4 class="mb-0"><i class="fas fa-user-injured me-2"></i> Registered Patients</h4>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li
                  v-for="patient in filteredPatients"
                  :key="patient.user_id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <span class="fw-bold">{{ patient.name }}</span>
                    <span v-if="patient.status === 'Inactive'" class="badge bg-danger ms-2"
                      >Blacklisted</span
                    >
                    <br />
                    <small class="text-muted">{{ patient.email }}</small>
                  </div>
                  <div class="d-flex gap-2">
                    <button
                      class="btn btn-outline-warning rounded-pill px-3"
                      @click="openEditPatientModal(patient)"
                    >
                      <i class="fas fa-edit"></i> Edit
                    </button>
                    <button
                      class="btn btn-outline-danger rounded-pill px-3"
                      @click="deleteUser(patient, 'Patient')"
                    >
                      <i class="fas fa-trash"></i> Delete
                    </button>
                    <button
                      v-if="patient.status !== 'Inactive'"
                      class="btn btn-outline-dark rounded-pill px-3"
                      @click="blacklistUser(patient, 'Patient')"
                    >
                      <i class="fas fa-ban"></i> Blacklist
                    </button>
                    <button v-else class="btn btn-secondary rounded-pill px-3" disabled>
                      <i class="fas fa-ban"></i> Blacklisted
                    </button>
                  </div>
                </li>
                <li
                  v-if="filteredPatients.length === 0"
                  class="list-group-item text-center text-muted"
                >
                  No patients found.
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN -->
        <div class="col-lg-4">
          <div class="card shadow-sm border-0">
            <div class="card-header bg-info text-white">
              <h4 class="mb-0"><i class="fas fa-calendar-alt me-2"></i> Upcoming Appointments</h4>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-striped table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Sr No.</th>
                      <th scope="col">Patient Name</th>
                      <th scope="col">Doctor Name</th>
                      <th scope="col">Department</th>
                      <th scope="col">Patient History</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(appt, index) in appointments" :key="appt.appointment_id">
                      <th>{{ index + 1 }}</th>
                      <td>{{ appt.patient_name }}</td>
                      <td>{{ appt.doctor_name }}</td>
                      <td>{{ appt.department }}</td>
                      <td>
                        <button
                          class="btn btn-sm btn-outline-primary"
                          @click="viewPatientHistory(appt.patient_id)"
                        >
                          <i class="fas fa-eye me-1"></i> View
                        </button>
                      </td>
                    </tr>
                    <tr v-if="appointments.length === 0">
                      <td class="text-center text-muted" colspan="5">No upcoming appointments.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- DEPARTMENT MODAL (Updated for Edit) -->
    <div id="departmentModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              {{ deptModalMode === 'create' ? 'Add New Department' : 'Edit Department' }}
            </h5>
            <button
              class="btn-close btn-close-white"
              type="button"
              @click="hideActiveModal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleDepartmentSubmit">
              <div class="mb-3">
                <label class="form-label fw-bold">Department Name</label>
                <input
                  v-model="departmentForm.department_name"
                  class="form-control"
                  required
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Description</label>
                <textarea
                  v-model="departmentForm.description"
                  class="form-control"
                  rows="3"
                ></textarea>
              </div>

              <!-- Head of Department Dropdown (Only in Edit Mode) -->
              <div v-if="deptModalMode === 'edit'" class="mb-3">
                <label class="form-label fw-bold">Head of Department</label>
                <select v-model="departmentForm.head_doctor_id" class="form-select">
                  <option :value="null">-- None --</option>

                  <!-- FILTER LOGIC:
                       1. Status is Active
                       2. AND (Belongs to THIS department OR Belongs to NO department)
                  -->
                  <option
                    v-for="doc in doctors.filter(d =>
                      d.status === 'Active' &&
                      (d.department_id == departmentForm.department_id || !d.department_id)
                    )"
                    :key="doc.user_id"
                    :value="doc.user_id"
                  >
                    {{ doc.name }} ({{ doc.department || 'Unassigned' }})
                  </option>
                </select>

                <div class="form-text text-muted">
                  Lists doctors currently in this department or unassigned doctors.
                </div>
              </div>

              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" @click="hideActiveModal">
                  Close
                </button>
                <button class="btn btn-primary" type="submit">
                  {{ deptModalMode === 'create' ? 'Create' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Doctor Modal -->
    <div id="doctorModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">
              {{ modalMode === 'create' ? 'Add New Doctor' : 'Edit Doctor Details' }}
            </h5>
            <button
              aria-label="Close"
              class="btn-close btn-close-white"
              type="button"
              @click="hideActiveModal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleDoctorSubmit">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold" for="doctorName">Full Name</label>
                  <input
                    id="doctorName"
                    v-model="editingDoctor.name"
                    class="form-control"
                    required
                    type="text"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold" for="doctorEmail">Email</label>
                  <input
                    id="doctorEmail"
                    v-model="editingDoctor.email"
                    :readonly="modalMode === 'edit'"
                    class="form-control"
                    required
                    type="email"
                  />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold" for="doctorDept">Assign Department</label>

                <select
                  v-if="departments.length > 0"
                  id="doctorDept"
                  v-model="editingDoctor.department_id"
                  class="form-select"
                  required
                >
                  <option disabled selected value="">Select a Department</option>
                  <option
                    v-for="dept in departments"
                    :key="dept.department_id"
                    :value="dept.department_id"
                  >
                    {{ dept.department_name }}
                  </option>
                </select>

                <div
                  v-else
                  class="alert alert-warning d-flex align-items-center justify-content-between p-2"
                >
                  <span>
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    No departments found!
                  </span>
                  <button
                    class="btn btn-sm btn-outline-dark fw-bold"
                    type="button"
                    @click="switchToDepartmentModal"
                  >
                    + Create One
                  </button>
                </div>

                <div v-if="departments.length === 0" class="form-text text-danger">
                  You cannot create a doctor without assigning a department.
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold" for="doctorPassword">Password</label>
                <input
                  id="doctorPassword"
                  v-model="editingDoctor.password"
                  :required="modalMode === 'create'"
                  autocomplete="new-password"
                  class="form-control"
                  minlength="8"
                  type="password"
                />
                <small v-if="modalMode === 'create'" class="form-text text-muted">
                  Password must be at least 8 characters long.
                </small>
                <small v-else class="form-text text-muted">
                  Leave blank to keep the current password.
                </small>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold" for="doctorQualification">
                    Qualification/Specialization
                  </label>
                  <input
                    id="doctorQualification"
                    v-model="editingDoctor.qualification"
                    class="form-control"
                    required
                    type="text"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold" for="doctorExperience">
                    Experience (Years)
                  </label>
                  <input
                    id="doctorExperience"
                    v-model.number="editingDoctor.experience_years"
                    class="form-control"
                    min="0"
                    required
                    type="number"
                  />
                </div>
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" @click="hideActiveModal">
                  Close
                </button>
                <button class="btn btn-success" type="submit">
                  {{ modalMode === 'create' ? 'Create Doctor' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Patient, History Modals (Unchanged) -->
    <div id="patientModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-warning text-dark">
            <h5 class="modal-title">Edit Patient Details</h5>
            <button
              aria-label="Close"
              class="btn-close"
              type="button"
              @click="hideActiveModal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handlePatientSubmit">
              <div class="mb-3">
                <label class="form-label fw-bold" for="patientName">Full Name</label>
                <input
                  id="patientName"
                  v-model="editingPatient.name"
                  class="form-control"
                  required
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold" for="patientEmail">Email</label>
                <input
                  id="patientEmail"
                  v-model="editingPatient.email"
                  class="form-control"
                  readonly
                  type="email"
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold" for="patientPhone">Phone</label>
                <input
                  id="patientPhone"
                  v-model="editingPatient.phone"
                  class="form-control"
                  type="text"
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold" for="patientAddress">Address</label>
                <textarea
                  id="patientAddress"
                  v-model="editingPatient.address"
                  class="form-control"
                  rows="3"
                ></textarea>
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" @click="hideActiveModal">
                  Close
                </button>
                <button class="btn btn-warning" type="submit">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div id="historyModal" class="modal fade" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title">Patient Appointment History</h5>
            <button
              class="btn-close btn-close-white"
              type="button"
              @click="hideActiveModal"
            ></button>
          </div>
          <div v-if="currentPatientHistory" class="modal-body">
            <h4>{{ currentPatientHistory.patient_name }}</h4>
            <div class="table-responsive">
              <table class="table table-bordered">
                <thead class="table-light">
                  <tr>
                    <th>Date & Time</th>
                    <th>Doctor</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appt in currentPatientHistory.appointments" :key="appt.appointment_id">
                    <td>{{ appt.date }} at {{ appt.time }}</td>
                    <td>{{ appt.doctor_name }}</td>
                    <td>{{ appt.treatment_details ? appt.treatment_details.diagnosis : 'N/A' }}</td>
                    <td>
                      {{ appt.treatment_details ? appt.treatment_details.prescription : 'N/A' }}
                    </td>
                    <td>{{ appt.treatment_details ? appt.treatment_details.notes : 'N/A' }}</td>
                  </tr>
                  <tr v-if="currentPatientHistory.appointments.length === 0">
                    <td class="text-center" colspan="5">No appointment history found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" type="button" @click="hideActiveModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      departments: [],
      doctors: [],
      patients: [],
      appointments: [],
      searchQuery: '',
      modalMode: 'create',
      deptModalMode: 'create', // New mode for Department modal
      editingDoctor: {},
      editingPatient: {},
      departmentForm: {
        department_id: null,
        department_name: '',
        description: '',
        head_doctor_id: null,
      },
      currentPatientHistory: null,
      activeModal: null,
    }
  },
  computed: {
    filteredDoctors() {
      if (!this.searchQuery) return this.doctors
      const lowerQuery = this.searchQuery.toLowerCase()
      return this.doctors.filter(
        (d) =>
          (d.name || '').toLowerCase().includes(lowerQuery) ||
          (d.email || '').toLowerCase().includes(lowerQuery),
      )
    },
    filteredPatients() {
      if (!this.searchQuery) return this.patients
      const lowerQuery = this.searchQuery.toLowerCase()
      return this.patients.filter(
        (p) =>
          (p.name || '').toLowerCase().includes(lowerQuery) ||
          (p.email || '').toLowerCase().includes(lowerQuery),
      )
    },
  },
  methods: {
    getToken() {
      return localStorage.getItem('adminToken')
    },
    async apiRequest(endpoint, method = 'GET', body = null) {
      let response = null
      try {
        const headers = { Authorization: `Bearer ${this.getToken()}` }
        const options = { method, headers }
        if (body) {
          headers['Content-Type'] = 'application/json'
          options.body = JSON.stringify(this._sanitizePayload(body))
        }
        response = await fetch(`/api${endpoint}`, options)
        const text = await response.text()
        let responseData = null
        try {
          responseData = text ? JSON.parse(text) : null
        } catch (e) {
          responseData = { __raw_text: text }
        }

        if (!response.ok) {
          const serverMessage =
            (responseData && (responseData.message || responseData.msg || responseData.detail)) ||
            responseData?.__raw_text ||
            response.statusText ||
            `HTTP ${response.status}`

          throw new Error(serverMessage)
        }
        return responseData
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

      const modalEl = document.getElementById(modalId)
      if (!modalEl) return
      if (window.bootstrap) {
        this.activeModal = new window.bootstrap.Modal(modalEl, {
          backdrop: 'static',
          keyboard: false,
        })
        this.activeModal.show()
      }
    },

    hideActiveModal() {
      if (this.activeModal) {
        this.activeModal.hide()
        this.activeModal = null
      }
      setTimeout(() => {
        document.querySelectorAll('.modal-backdrop').forEach((backdrop) => backdrop.remove())
        document.body.classList.remove('modal-open')
        document.body.style.overflow = ''
        document.body.style.paddingRight = ''
      }, 200)
    },

    _sanitizePayload(payload) {
      if (!payload || typeof payload !== 'object') return payload
      const out = Array.isArray(payload) ? [] : {}
      for (const k in payload) {
        if (!Object.prototype.hasOwnProperty.call(payload, k)) continue
        const v = payload[k]
        if (v === undefined || v === null) continue
        if (typeof v === 'number' && isNaN(v)) continue
        out[k] = v
      }
      return out
    },

    async fetchAllData() {
      await this.fetchDepartments()
      await this.fetchDoctors()
      await this.fetchPatients()
      await this.fetchAppointments()
    },

    async fetchDepartments() {
      const data = await this.apiRequest('/departments')
      if (data && data.departments) {
        this.departments = data.departments
      }
    },

    async fetchDoctors() {
      const data = await this.apiRequest('/admin/doctors')
      if (data && data.doctors) {
        this.doctors = data.doctors
      }
    },

    async fetchPatients() {
      const data = await this.apiRequest('/admin/patients')
      if (data) {
        if (Array.isArray(data)) this.patients = data
        else if (data.patients) this.patients = data.patients
        else if (data.users) this.patients = data.users
        else if (data.data) this.patients = data.data
      }
    },

    async fetchAppointments() {
      const data = await this.apiRequest('/admin/upcoming_appointments')
      if (data && data.upcoming_appointments) {
        this.appointments = data.upcoming_appointments
      }
    },

    // --- DEPARTMENT LOGIC ---
    openDepartmentModal() {
      this.deptModalMode = 'create'
      this.departmentForm = { department_name: '', description: '', head_doctor_id: null }
      this.showModal('departmentModal')
    },

    openEditDepartmentModal(dept) {
      this.deptModalMode = 'edit'
      this.departmentForm = {
        department_id: dept.department_id,
        department_name: dept.department_name,
        description: dept.description,
        head_doctor_id: dept.head_doctor_id || null,
      }
      this.showModal('departmentModal')
    },

    getDoctorsInDept(deptId) {
      // Filter local doctors list to only show those in the current dept
      return this.doctors.filter((d) => d.department_id === deptId)
    },

    async handleDepartmentSubmit() {
      let result
      if (this.deptModalMode === 'create') {
        result = await this.apiRequest('/add_dept', 'POST', this.departmentForm)
      } else {
        result = await this.apiRequest(
          `/admin/department/edit/${this.departmentForm.department_id}`,
          'PUT',
          this.departmentForm,
        )
      }

      if (result) {
        alert(result.message)
        this.hideActiveModal()
        this.fetchDepartments()
      }
    },

    switchToDepartmentModal() {
      this.hideActiveModal()
      setTimeout(() => {
        this.openDepartmentModal()
      }, 300)
    },

    // --- DOCTOR LOGIC ---
    openCreateDoctorModal() {
      this.modalMode = 'create'
      this.editingDoctor = {
        name: '',
        email: '',
        password: '',
        qualification: '',
        experience_years: null,
        phone: '',
        gender: '',
        date_of_birth: '',
        address: '',
        status: 'Active',
        department_id: '',
      }
      this.showModal('doctorModal')
    },
    openEditDoctorModal(doctor) {
      this.modalMode = 'edit'
      this.editingDoctor = {
        ...doctor,
        qualification: doctor.qualification || doctor.qualifications || doctor.specialization || '',
        department_id: doctor.department_id || '',
        password: '',
      }
      this.showModal('doctorModal')
    },
    async handleDoctorSubmit() {
      if (this.departments.length === 0) {
        alert('Please create a Department first.')
        return
      }
      // Password Validation
      if (
        this.modalMode === 'create' &&
        (!this.editingDoctor.password || this.editingDoctor.password.length < 8)
      ) {
        alert('Password must be at least 8 characters long.')
        return
      }
      if (
        this.modalMode === 'edit' &&
        this.editingDoctor.password &&
        this.editingDoctor.password.length < 8
      ) {
        alert('Password must be at least 8 characters long.')
        return
      }

      this.hideActiveModal()

      try {
        if (this.modalMode === 'create') {
          const result = await this.apiRequest('/admin/add_doctor', 'POST', this.editingDoctor)
          if (result) {
            alert('Doctor created successfully!')
            await this.fetchDoctors()
          }
        } else {
          const payload = { ...this.editingDoctor }
          if (!payload.password) delete payload.password
          await this.apiRequest(`/admin/doctor/edit/${this.editingDoctor.user_id}`, 'PUT', payload)
          await this.fetchDoctors()
        }
      } catch (e) {
        console.error(e)
        this.fetchDoctors()
      }
    },

    // --- PATIENT LOGIC ---
    openEditPatientModal(patient) {
      this.editingPatient = { ...patient }
      this.showModal('patientModal')
    },
    async handlePatientSubmit() {
      this.hideActiveModal()
      try {
        await this.apiRequest(
          `/admin/patient/edit/${this.editingPatient.user_id}`,
          'PUT',
          this.editingPatient,
        )
        await this.fetchPatients()
      } catch (e) {
        console.error(e)
      }
    },

    async viewPatientHistory(patientId) {
      this.currentPatientHistory = null
      const data = await this.apiRequest(`/admin/patient/history/${patientId}`)
      if (data) {
        this.currentPatientHistory = data
        this.showModal('historyModal')
      }
    },

    async deleteUser(user, role) {
      if (!confirm(`Are you sure you want to delete this ${role.toLowerCase()}?`)) return
      const endpoint =
        role === 'Doctor'
          ? `/admin/doctor/delete/${user.user_id}`
          : `/admin/patient/delete/${user.user_id}`
      if (await this.apiRequest(endpoint, 'DELETE')) {
        alert(`${role} deleted successfully!`)
        await this.fetchAllData()
      }
    },

    async blacklistUser(user, role) {
      if (!confirm(`Are you sure you want to blacklist this ${role.toLowerCase()}?`)) return
      user.status = 'Inactive'
      const endpoint =
        role === 'Doctor'
          ? `/admin/doctor/blacklist/${user.user_id}`
          : `/admin/patient/blacklist/${user.user_id}`
      const result = await this.apiRequest(endpoint, 'POST')
      if (result) {
        alert(result.message || `${role} blacklisted successfully!`)
        await this.fetchAllData()
      }
    },

    logout() {
      localStorage.removeItem('adminToken')
      this.$router.push('/admin-login')
    },
  },
  mounted() {
    if (!this.getToken()) {
      this.$router.push('/admin-login')
    } else {
      this.fetchAllData()
    }
  },
}
</script>

<style scoped>
.dashboard-body {
  background-color: #f8f9fa;
  min-height: 100vh;
}
.welcome-banner {
  background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
}
.card {
  transition: box-shadow 0.2s ease-in-out;
}
.list-group-item {
  transition: background-color 0.2s ease-in-out;
}
.list-group-item:hover {
  background-color: #f1f3f5;
}
.modal-header {
  border-bottom: none;
}
</style>
