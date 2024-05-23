# Plastic Surgery Clinic Electronic Management System

![image](https://github.com/MoHazem02/Plastic-Surgey-Clinic/assets/66066832/8c6ce50f-ef08-4cc9-adf8-7007feffaca4)

Welcome to the Plastic Surgery Clinic Electronic Management System! This project is an electronic management system designed specifically for a plastic surgery clinic. The system supports four departments: Face, Breast, Body, and Non-Surgical. It is built using Django and provides distinct views and functionalities for patients, nurses, doctors, and administrators.

## Features

### Patient Portal

- **Book Appointments**: Patients can easily book appointments with their preferred doctors.
- **View Appointments**: Patients can view both upcoming and past appointments.
- **View Prescriptions**: Access to doctor prescriptions from past appointments.
- **Cancel Appointments**: Patients can cancel any upcoming appointment if needed.
![image](https://github.com/MoHazem02/Plastic-Surgey-Clinic/assets/66066832/fa272731-644e-4e43-a378-55755607cc53)


### Nurse View

- **Manage Patient Records**: Nurses can manage and update patient records within their department.
- **Coordinate Appointments**: Assist in the scheduling and coordination of appointments and treatments.

### Doctor View

- **Appointment Management**: Doctors can manage their schedules and appointments.
- **Access Patient Histories**: Doctors have access to patient medical histories for better diagnosis and treatment.
- **Prescribe Treatments**: Provide and update prescriptions for patients.

### Admin View

- **User Management**: Administrators can manage all users including patients, nurses, and doctors.
- **Department Management**: Control and update department information.
- **System Settings**: Full control over system-wide settings and configurations.

### API Integration

- **Disease Insights**: Integration with the Disease.sh API to provide insights about current diseases relevant to the clinic's patients. This helps in keeping the medical staff informed about potential outbreaks or prevalent diseases.

## Installation

To set up this project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/MoHazem02/Plastic-Surgey-Clinic.git
    cd Plastic-Surgey-Clinic
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

4. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

5. **Access the application**:
    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

After setting up the project, you can start using the system based on your role:

- **Patients**: Register and log in to book and manage your appointments.
- **Nurses**: Log in to manage patient records and assist in coordinating treatments.
- **Doctors**: Log in to manage appointments, view patient histories, and prescribe treatments.
- **Administrators**: Log in to manage users, departments, and system settings.

## Contributing

We welcome contributions to improve this project! To contribute, follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes** and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. **Push to the branch**:
    ```sh
    git push origin feature/your-feature-name
    ```
5. **Create a pull request**.

## Contact

For any inquiries or support, please contact [MoHazem02](https://github.com/MoHazem02).

