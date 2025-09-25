// Internships List JavaScript
class InternshipsList {
    constructor() {
        this.currentPage = 1;
        this.perPage = 12;
        this.currentFilters = {
            search: '',
            industry: '',
            location: '',
            education: ''
        };
        this.internships = [];
        this.pagination = {};
        this.deleteInternshipId = null;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadFilterOptions();
        this.loadInternships();
    }

    bindEvents() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.currentFilters.search = e.target.value;
                this.currentPage = 1;
                this.loadInternships();
            }, 500);
        });

        // Filter dropdowns
        document.getElementById('industryFilter').addEventListener('change', (e) => {
            this.currentFilters.industry = e.target.value;
            this.currentPage = 1;
            this.loadInternships();
        });

        document.getElementById('locationFilter').addEventListener('change', (e) => {
            this.currentFilters.location = e.target.value;
            this.currentPage = 1;
            this.loadInternships();
        });

        document.getElementById('educationFilter').addEventListener('change', (e) => {
            this.currentFilters.education = e.target.value;
            this.currentPage = 1;
            this.loadInternships();
        });

        // Clear filters
        document.getElementById('clearFilters').addEventListener('click', () => {
            this.clearFilters();
        });

        // Pagination
        document.getElementById('prevPage').addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.loadInternships();
            }
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            if (this.currentPage < this.pagination.pages) {
                this.currentPage++;
                this.loadInternships();
            }
        });

        // Modal events
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeEditModal();
        });

        document.getElementById('cancelDelete').addEventListener('click', () => {
            this.closeDeleteModal();
        });

        document.getElementById('confirmDelete').addEventListener('click', () => {
            this.confirmDelete();
        });

        // Close modals on backdrop click
        document.getElementById('editModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.closeEditModal();
            }
        });

        document.getElementById('deleteModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.closeDeleteModal();
            }
        });
    }

    async loadFilterOptions() {
        try {
            const response = await fetch('http://localhost:5001/api/internships/filters', {
                credentials: 'include'
            });
            const data = await response.json();
            
            if (data.success) {
                this.populateFilterDropdown('industryFilter', data.filters.industries);
            }
        } catch (error) {
            console.error('Error loading filter options:', error);
        }
    }

    populateFilterDropdown(selectId, options) {
        const select = document.getElementById(selectId);
        const currentValue = select.value;
        
        // Remove existing options except the first one
        while (select.children.length > 1) {
            select.removeChild(select.lastChild);
        }
        
        // Add new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
        
        // Restore current value if it still exists
        if (currentValue && options.includes(currentValue)) {
            select.value = currentValue;
        }
    }

    async loadInternships() {
        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.perPage
            });

            // Add filters to params
            if (this.currentFilters.search) {
                params.append('q', this.currentFilters.search);
            }
            if (this.currentFilters.industry) {
                params.append('industry', this.currentFilters.industry);
            }
            if (this.currentFilters.location) {
                params.append('location_type', this.currentFilters.location);
            }
            if (this.currentFilters.education) {
                params.append('education_level', this.currentFilters.education);
            }

            const url = this.currentFilters.search ? 
                'http://localhost:5001/api/internships/search' : 
                'http://localhost:5001/api/internships';

            const response = await fetch(`${url}?${params}`, {
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.internships = data.internships;
                this.pagination = data.pagination || { total: data.count || 0, pages: 1 };
                this.renderInternships();
                this.updatePagination();
            } else {
                this.showError(data.message || 'Failed to load internships');
            }
        } catch (error) {
            console.error('Error loading internships:', error);
            this.showError('Network error. Please check your connection.');
        } finally {
            this.hideLoading();
        }
    }

    renderInternships() {
        const grid = document.getElementById('internshipsGrid');
        const emptyState = document.getElementById('emptyState');

        if (this.internships.length === 0) {
            grid.innerHTML = '';
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');
        
        grid.innerHTML = this.internships.map(internship => `
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div class="p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-semibold text-gray-900 line-clamp-2">
                            ${this.escapeHtml(internship.internship_title)}
                        </h3>
                        <div class="flex space-x-2 ml-4">
                            <button 
                                onclick="internshipsList.editInternship(${internship.internship_id})" 
                                class="text-gray-400 hover:text-blue-600 transition-colors"
                                title="Edit"
                            >
                                <i class="fas fa-edit"></i>
                            </button>
                            <button 
                                onclick="internshipsList.deleteInternship(${internship.internship_id})" 
                                class="text-gray-400 hover:text-red-600 transition-colors"
                                title="Delete"
                            >
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="space-y-2 mb-4">
                        <div class="flex items-center text-sm text-gray-600">
                            <i class="fas fa-industry mr-2 w-4"></i>
                            <span>${this.escapeHtml(internship.industry_domain)}</span>
                        </div>
                        
                        <div class="flex items-center text-sm text-gray-600">
                            <i class="fas fa-map-marker-alt mr-2 w-4"></i>
                            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${this.getLocationTypeClass(internship.location_type)}">
                                ${internship.location_type}
                            </span>
                        </div>
                        
                        <div class="flex items-center text-sm text-gray-600">
                            <i class="fas fa-graduation-cap mr-2 w-4"></i>
                            <span>${internship.education_level}</span>
                        </div>
                        
                        <div class="flex items-center text-sm text-gray-600">
                            <i class="fas fa-clock mr-2 w-4"></i>
                            <span>${this.escapeHtml(internship.duration)}</span>
                        </div>
                        
                        ${internship.stipend ? `
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-dollar-sign mr-2 w-4"></i>
                                <span>${this.escapeHtml(internship.stipend)}</span>
                            </div>
                        ` : ''}
                        
                        ${internship.minimum_gpa ? `
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-chart-line mr-2 w-4"></i>
                                <span>Min GPA: ${internship.minimum_gpa}</span>
                            </div>
                        ` : ''}
                    </div>
                    
                    ${internship.fulltime_conversion ? `
                        <div class="mb-4">
                            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                <i class="fas fa-arrow-up mr-1"></i>
                                Full-time conversion available
                            </span>
                        </div>
                    ` : ''}
                    
                    ${internship.description ? `
                        <p class="text-sm text-gray-600 line-clamp-3 mb-4">
                            ${this.escapeHtml(internship.description)}
                        </p>
                    ` : ''}
                    
                    ${internship.required_skills ? `
                        <div class="mb-4">
                            <h4 class="text-sm font-medium text-gray-900 mb-2">Required Skills:</h4>
                            <p class="text-sm text-gray-600 line-clamp-2">
                                ${this.escapeHtml(internship.required_skills)}
                            </p>
                        </div>
                    ` : ''}
                    
                    <div class="flex justify-between items-center text-xs text-gray-500">
                        <span>Added: ${this.formatDate(internship.created_at)}</span>
                        ${internship.updated_at !== internship.created_at ? 
                            `<span>Updated: ${this.formatDate(internship.updated_at)}</span>` : ''
                        }
                    </div>
                </div>
            </div>
        `).join('');
    }

    getLocationTypeClass(locationType) {
        switch (locationType) {
            case 'Remote':
                return 'bg-green-100 text-green-800';
            case 'On-site':
                return 'bg-blue-100 text-blue-800';
            case 'Hybrid':
                return 'bg-purple-100 text-purple-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    }

    updatePagination() {
        const paginationDiv = document.getElementById('pagination');
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');
        const pageInfo = document.getElementById('pageInfo');

        if (this.pagination.pages <= 1) {
            paginationDiv.classList.add('hidden');
            return;
        }

        paginationDiv.classList.remove('hidden');
        pageInfo.textContent = `Page ${this.currentPage} of ${this.pagination.pages}`;
        
        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= this.pagination.pages;
    }

    async editInternship(internshipId) {
        try {
            const response = await fetch(`http://localhost:5001/api/internships/${internshipId}`, {
                credentials: 'include'
            });
            const data = await response.json();
            
            if (data.success) {
                this.populateEditForm(data.internship);
                this.showEditModal();
            } else {
                this.showError(data.message || 'Failed to load internship details');
            }
        } catch (error) {
            console.error('Error loading internship for edit:', error);
            this.showError('Network error. Please try again.');
        }
    }

    populateEditForm(internship) {
        const form = document.getElementById('editFormContainer');
        form.innerHTML = `
            <form id="editInternshipFormModal">
                <input type="hidden" id="edit_internship_id" value="${internship.internship_id}">
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Internship Title <span class="text-red-500">*</span>
                        </label>
                        <input 
                            type="text" 
                            id="edit_internship_title" 
                            value="${this.escapeHtml(internship.internship_title)}"
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Industry Domain <span class="text-red-500">*</span>
                        </label>
                        <input 
                            type="text" 
                            id="edit_industry_domain" 
                            value="${this.escapeHtml(internship.industry_domain)}"
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Location Type <span class="text-red-500">*</span>
                        </label>
                        <select 
                            id="edit_location_type" 
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                            <option value="On-site" ${internship.location_type === 'On-site' ? 'selected' : ''}>On-site</option>
                            <option value="Remote" ${internship.location_type === 'Remote' ? 'selected' : ''}>Remote</option>
                            <option value="Hybrid" ${internship.location_type === 'Hybrid' ? 'selected' : ''}>Hybrid</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Education Level <span class="text-red-500">*</span>
                        </label>
                        <select 
                            id="edit_education_level" 
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                            <option value="High School" ${internship.education_level === 'High School' ? 'selected' : ''}>High School</option>
                            <option value="Undergraduate" ${internship.education_level === 'Undergraduate' ? 'selected' : ''}>Undergraduate</option>
                            <option value="Graduate" ${internship.education_level === 'Graduate' ? 'selected' : ''}>Graduate</option>
                            <option value="Postgraduate" ${internship.education_level === 'Postgraduate' ? 'selected' : ''}>Postgraduate</option>
                            <option value="PhD" ${internship.education_level === 'PhD' ? 'selected' : ''}>PhD</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Duration <span class="text-red-500">*</span>
                        </label>
                        <input 
                            type="text" 
                            id="edit_duration" 
                            value="${this.escapeHtml(internship.duration)}"
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Minimum GPA
                        </label>
                        <input 
                            type="number" 
                            id="edit_minimum_gpa" 
                            value="${internship.minimum_gpa || ''}"
                            min="0" max="10" step="0.1"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Stipend
                        </label>
                        <input 
                            type="text" 
                            id="edit_stipend" 
                            value="${this.escapeHtml(internship.stipend || '')}"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >
                    </div>

                    <div class="flex items-center">
                        <input 
                            type="checkbox" 
                            id="edit_fulltime_conversion" 
                            ${internship.fulltime_conversion ? 'checked' : ''}
                            class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
                        >
                        <label for="edit_fulltime_conversion" class="ml-2 block text-sm text-gray-700">
                            Full-time conversion opportunity
                        </label>
                    </div>

                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Required Skills
                        </label>
                        <textarea 
                            id="edit_required_skills" 
                            rows="3"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >${this.escapeHtml(internship.required_skills || '')}</textarea>
                    </div>

                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Description
                        </label>
                        <textarea 
                            id="edit_description" 
                            rows="4"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >${this.escapeHtml(internship.description || '')}</textarea>
                    </div>

                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            Past Intern Records
                        </label>
                        <textarea 
                            id="edit_past_intern_records" 
                            rows="3"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                        >${this.escapeHtml(internship.past_intern_records || '')}</textarea>
                    </div>
                </div>

                <div class="mt-6 flex justify-end space-x-3">
                    <button 
                        type="button" 
                        onclick="internshipsList.closeEditModal()"
                        class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                    >
                        Cancel
                    </button>
                    <button 
                        type="submit" 
                        class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-600 transition-colors"
                    >
                        Update Internship
                    </button>
                </div>
            </form>
        `;

        // Bind form submit event
        document.getElementById('editInternshipFormModal').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitEditForm();
        });
    }

    async submitEditForm() {
        const formData = {
            internship_title: document.getElementById('edit_internship_title').value,
            industry_domain: document.getElementById('edit_industry_domain').value,
            location_type: document.getElementById('edit_location_type').value,
            education_level: document.getElementById('edit_education_level').value,
            duration: document.getElementById('edit_duration').value,
            minimum_gpa: document.getElementById('edit_minimum_gpa').value,
            stipend: document.getElementById('edit_stipend').value,
            fulltime_conversion: document.getElementById('edit_fulltime_conversion').checked,
            required_skills: document.getElementById('edit_required_skills').value,
            description: document.getElementById('edit_description').value,
            past_intern_records: document.getElementById('edit_past_intern_records').value
        };

        const internshipId = document.getElementById('edit_internship_id').value;

        try {
            const response = await fetch(`http://localhost:5001/api/internships/${internshipId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                this.closeEditModal();
                this.showSuccess('Internship updated successfully!');
                this.loadInternships(); // Refresh the list
            } else {
                this.showError(data.message || 'Failed to update internship');
            }
        } catch (error) {
            console.error('Error updating internship:', error);
            this.showError('Network error. Please try again.');
        }
    }

    deleteInternship(internshipId) {
        this.deleteInternshipId = internshipId;
        this.showDeleteModal();
    }

    async confirmDelete() {
        if (!this.deleteInternshipId) return;

        try {
            const response = await fetch(`http://localhost:5001/api/internships/${this.deleteInternshipId}`, {
                method: 'DELETE',
                credentials: 'include'
            });

            const data = await response.json();

            if (data.success) {
                this.closeDeleteModal();
                this.showSuccess('Internship deleted successfully!');
                this.loadInternships(); // Refresh the list
            } else {
                this.showError(data.message || 'Failed to delete internship');
            }
        } catch (error) {
            console.error('Error deleting internship:', error);
            this.showError('Network error. Please try again.');
        }
    }

    clearFilters() {
        this.currentFilters = {
            search: '',
            industry: '',
            location: '',
            education: ''
        };
        
        document.getElementById('searchInput').value = '';
        document.getElementById('industryFilter').value = '';
        document.getElementById('locationFilter').value = '';
        document.getElementById('educationFilter').value = '';
        
        this.currentPage = 1;
        this.loadInternships();
    }

    showEditModal() {
        document.getElementById('editModal').classList.remove('hidden');
    }

    closeEditModal() {
        document.getElementById('editModal').classList.add('hidden');
    }

    showDeleteModal() {
        document.getElementById('deleteModal').classList.remove('hidden');
    }

    closeDeleteModal() {
        document.getElementById('deleteModal').classList.add('hidden');
        this.deleteInternshipId = null;
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('hidden');
        document.getElementById('internshipsGrid').classList.add('opacity-50');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('hidden');
        document.getElementById('internshipsGrid').classList.remove('opacity-50');
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        errorText.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }

    showSuccess(message) {
        const toast = document.getElementById('successToast');
        const messageSpan = document.getElementById('successMessage');
        if (messageSpan) {
            messageSpan.textContent = message;
        }
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    window.internshipsList = new InternshipsList();
});