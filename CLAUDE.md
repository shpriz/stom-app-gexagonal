# Stomatology Practice Management System

## Project Overview
A Django-based web application for managing a dental practice with patient visit tracking and dynamic visualization of 6 key health indicators using hexagonal radar charts.

## Key Features
- Patient management system
- 6 configurable health indicators per patient
- Hexagonal radar chart visualization with color zones (green/yellow/red)
- Historical data overlay with semi-transparent layers (wind rose effect)
- Date-based filtering with "show on diagram" checkboxes
- Manual indicator configuration (min/max values, zones)

## Tech Stack
- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL (Docker container)
- **Frontend:** Django templates + Chart.js/D3.js for radar charts
- **Containerization:** Docker + docker-compose

## Memories
- Use `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>` for chart inclusion
- **CRITICAL**: Always use unified CSS framework from `/static/css/modern-medical.css` - Complete design system for consistent styling across ALL pages
- **NEVER** create custom CSS files or use inline styles - everything must use modern-medical.css classes

## UI Design System Rules (MANDATORY)
### Page Structure
- **ALWAYS** use unified header: `<header class="header">` with `<div class="container">` and `<div class="header-content">`
- **ALWAYS** use `<div class="container">` for page content
- **ALWAYS** wrap content in `<div class="card"><div class="card-body">`
- **NEVER** use old page-header, hero-section, or main-container structures

### Navigation
- Use standard nav structure with: 🏠 Панель управления, 👥 Все пациенты, ⚙️ Настройки, 📋 Схемы, 🚪 Выход
- Mark active page with `nav-link active` class
- Logout button uses `btn btn-danger btn-sm`

### Buttons (CRITICAL - Follow Exactly)
- **Edit actions**: `btn btn-warning` (orange #F59E0B with border)
- **Add/Create actions**: `btn btn-success` (green)  
- **Delete actions**: `btn btn-danger` (red)
- **Cancel actions**: `btn btn-secondary` (gray)
- **Button spacing**: Use `d-flex gap-2 justify-content-end mt-4` for button groups

### Form Fields
- **Input borders**: Light blue #a8c5f0 with hover effects (#7ba7e8)
- Use `form-group` class for field containers
- Use `help-text` class for field descriptions
- Required fields marked with `<span class="required">*</span>`

### Language
- **ALL** interface text must be in Russian
- Use "показатель" instead of "индикатор"
- Use professional medical terminology

### Layout Consistency
- Page headers use `patients-header-combined` structure
- Remove unnecessary banners and redundant navigation elements
- Keep interfaces clean and focused
- Use consistent spacing with mt-4, gap-2 classes

## Database Structure
### Core Models
- `Patient` - Patient information
- `Indicator` - Configurable indicators (name, min/max values, color zones)
- `Measurement` - Patient measurements with timestamps and visibility flags

## Development Environment
- PostgreSQL in Docker container
- Django development server
- Data persistence via Docker volumes

## Progress Completed
✅ Docker setup with PostgreSQL container
✅ Django project 'dental_office' created
✅ Three Django apps created: patients, measurements, indicators
✅ PostgreSQL database connection configured
✅ Initial Django migrations applied successfully
✅ Dependencies installed (Django, PostgreSQL, REST Framework, CORS)
✅ Database models created:
  - Patient (with patronymic field, phone default '0')
  - PatientHistory (name change tracking)
  - Indicator (6 configurable indicators with color zones)
  - Measurement & MeasurementValue (patient measurements)
✅ Django admin interface configured for all models
✅ Superuser account created
✅ API endpoints created:
  - `/api/measurements/` - CRUD operations
  - `/api/measurements/radar_chart_data/` - Chart data endpoint
✅ Hexagonal radar chart visualization:
  - Chart.js implementation at `/chart/<patient_id>/`
  - Semi-transparent overlays for multiple measurements
  - Color zones (green/yellow/red) based on thresholds
  - Date filtering with checkboxes
  - Interactive tooltips with actual values
✅ 6 indicators added via admin interface
✅ User-friendly patient forms:
  - Add patient form at `/patient/add/`
  - Edit patient form at `/patient/edit/<id>/`
  - Replaced admin interface for patient management
  - Phone number validation (flexible format)
  - Date of birth validation (no future dates)
  - History of illness field (10 char limit)
✅ Navigation and UI:
  - Dashboard at `/` with stats and recent measurements
  - Patient list at `/patients/` with chart links
  - Navigation between all pages
  - Error handling and validation messages
✅ Advanced measurement form:
  - Two-column layout with 3 indicators per column
  - Column widths: 70% indicator name, 15% input, 15% score
  - Consistent row heights: headers 40px, data rows 100px
  - Real-time score calculation using exact medical formulas
  - Automatic point assignment based on entered values
  - Clean professional styling without unnecessary backgrounds
✅ Medical scoring formulas implemented:
  - OHIP 14: 0-28=0pts, 29-42=1pt, 43-56=2pts
  - Length of stay: <5=0pts, 5-10=1pt, ≥11=2pts  
  - Smoking: 0=0pts, 1-19=1pt, ≥20=2pts
  - Somatic diseases: 0=0pts, 1=1pt, ≥2=2pts
  - Medication intake: 0=0pts, 1=1pt, ≥2=2pts
  - Compliance: 30-46=0pts, 23-29=1pt, 15-22=2pts
✅ Database optimization:
  - Changed MeasurementValue from FloatField to IntegerField
  - All measurements now stored as whole numbers (0, 1, 2)
  - Form validation enforces integer input only
✅ Hexagonal radar chart visualization:
  - Fixed chart scaling (0-2 points instead of 0-100%)
  - Horizontal filter layout for measurement selection
  - Color-coded zones: Green=low risk, Yellow=medium, Red=high risk
  - Semi-transparent overlays for multiple measurements
  - Interactive tooltips with actual point values
  - Debug logging for troubleshooting data flow
✅ Chart.js loading and background zones:
  - Fixed Chart.js loading issues using jsdelivr CDN
  - Implemented layered background color zones on radar chart
  - Red zone (1.5-2 points): Bottom layer (highest risk)
  - Yellow zone (1-1.5 points): Middle layer (medium risk)
  - Green zone (0-1 points): Top layer (low risk)
  - Proper visual hierarchy with red as outermost layer
✅ Chart improvements and enhancements:
  - Latest measurements now display on top (z-order fixed)
  - Removed yellow colors from measurement area filling
  - Increased font sizes: axis labels (20px), tick labels (18px), tooltips (16px/14px)
  - Doubled canvas size from 800x400px to 1600x800px for better visibility
✅ Complete CRUD operations for measurements:
  - Edit measurement view at `/measurement/edit/<measurement_id>/`
  - Delete measurement view at `/measurement/delete/<measurement_id>/`
  - Confirmation template for safe measurement deletion
  - Edit/Delete buttons integrated in radar chart interface
  - Pre-population of edit forms with existing measurement data
  - Raw value reconstruction from stored scores for editing
✅ Complete CRUD operations for patients:
  - Delete patient view at `/patient/delete/<patient_id>/`
  - Comprehensive confirmation template with data statistics
  - Delete buttons added to patient list and edit forms
  - Cascading deletion of all related measurements and history
  - Safety features with double confirmation (page + JavaScript alert)
  - Warning messages about permanent data loss
✅ Medical history number validation and duplicate detection:
  - Made history_of_illness field unique and required in Patient model
  - Added comprehensive form validation to check for existing patients
  - Duplicate detection shows existing patient details with edit/view options
  - Prevents creation of patients with same medical history number
  - User-friendly alert system with navigation to existing patient records
✅ User interface improvements:
  - Removed all admin panel references from navigation and help text
  - Clean professional interface focused on custom forms
  - Updated error messages to direct users to proper patient management flows
  - Eliminated administrative complexity from end-user experience
✅ Raw value to score conversion system:
  - Updated database min/max ranges to accept raw measurement inputs
  - OHIP 14: 0-56 input range with automatic 0-28=0б, 29-42=1б, 43-56=2б conversion
  - Duration: 0-50 years input with automatic <5=0б, 5-10=1б, ≥11=2б conversion
  - Medication: 0-10 drugs input with automatic 0=0б, 1=1б, ≥2=2б conversion
  - Real-time score display shows calculated points as user types
  - Enhanced form placeholders and help text explaining automatic conversion
✅ Chart scale and display improvements (corrected to 0-2 medical scale):
  - Fixed radar chart data validation to ensure only 0-2 score values
  - Updated chart scale to proper 0-2 medical scoring system
  - Removed "pts" labels - now shows clean numbers (0, 1, 2)
  - Updated background risk zones for 0-2 scale (Green: 0-1, Yellow: 1-1.5, Red: 1.5-2)
  - Fixed chart data clipping to prevent points appearing outside chart area
  - Added database validation to enforce 0-2 range for measurement values
  - Hexagon scaling: Increased visual size by 1.3x for better readability while maintaining correct data scale
  - Background zones properly aligned with numbered grid lines (red zone stops at "2" line)
✅ Indicator name display optimization:
  - Implemented smart 2-row text splitting for long indicator names
  - Automatic detection of natural break points (parentheses, prepositions, dashes)
  - Intelligent positioning to ensure readable splits
  - Improved chart readability and professional appearance
✅ Schema-based indicator system:
  - Created Schema model for organizing indicators into logical groups
  - Multiple schemas per practice (e.g., "OHIP Assessment", "Clinical Status")
  - Schema ordering and descriptions for better organization
  - Schema-specific measurement filtering and display
✅ Flexible automatic scoring system:
  - ScoringRange model supporting multiple range types:
    - Normal ranges (min-max values)
    - Exact value matching
    - Greater than or equal conditions (≥N)
    - Less than conditions (<N)
  - User-friendly scoring range management interface
  - Real-time score calculation using database-driven rules
  - Automatic point assignment based on entered raw values
✅ Enhanced measurement forms:
  - Schema selection dropdown in measurement forms
  - Dynamic indicator loading based on selected schema
  - Real-time score calculation with API-driven scoring ranges
  - Professional two-column layout with scoring display
✅ Dismissible message system:
  - Reusable message component with close buttons
  - Auto-dismiss for success messages (5-second timer)
  - Smooth fade-out animations
  - Consistent message handling across all templates
✅ Chart display improvements:
  - Enhanced indicator text to display on 3 lines instead of 2
  - Improved hexagon chart sizing with better text spacing
  - Consistent chart dimensions across multiple schemas
  - Better responsive layout for side-by-side chart display
✅ Group average and z-score analysis system:
  - API endpoints for group statistics calculation:
    - `/api/measurements/group_statistics/?schema_id=X` - Population statistics (mean, std dev, sample size)
    - `/api/measurements/patient_z_scores/?patient_id=X&schema_id=Y` - Z-score analysis
  - Group average visualization:
    - Dashed gray line showing population mean for each indicator
    - Toggle checkbox: "Show Group Average" to enable/disable
    - Enhanced tooltips displaying group statistics
    - Legend integration for group average display
  - Z-score analysis features:
    - Statistical comparison: (Patient Score - Group Mean) / Group Standard Deviation
    - Visible z-score panel below charts showing all indicator z-scores
    - Color-coded interpretation: Green (normal), Red (outlier beyond ±2σ)
    - Toggle checkbox: "Show Z-Scores" to enable z-score display
    - Automatic outlier detection and flagging
    - Smart handling for insufficient data (requires ≥2 patients)
  - Clinical benefits:
    - Patient benchmarking against practice population
    - Statistical outlier identification for clinical attention
    - Population-based quality metrics and trend tracking
    - Research data generation for practice analytics
  - Real-time dynamic calculations:
    - Group statistics recalculated on every chart view
    - Automatic inclusion of new patients in population analysis
    - Scalable from 2 patients to 1000+ patients
    - No caching - always uses current database state
✅ Authentication and authorization system:
  - Django session-based authentication for medical data security
  - Role-based access control: Doctor, Nurse, Administrator, Researcher
  - Permission decorators for granular access control
  - User profiles with medical practice specific fields (license, department)
  - Session security settings for healthcare compliance (8-hour timeout)
  - Automatic profile creation for new users via Django signals
  - Fixed redirect loop issues for seamless user experience
  - Clean navigation without unnecessary admin/profile buttons
✅ Multi-doctor patient segregation system:
  - Added doctor foreign key field to Patient model with database migration
  - Each doctor can only view, edit, and delete their own patients
  - Patient list, charts, and measurements filtered by current doctor
  - Medical history number validation scoped to individual doctors
  - New patients automatically assigned to current doctor on creation
  - All measurement operations (CRUD) filtered by patient ownership
  - Dashboard statistics show only current doctor's patient data
  - API endpoints secured to show only doctor's own patient measurements
  - Group average calculations use all patients database-wide for population statistics
  - 404 error page created with medical theme and Russian localization
✅ Schema chart layout and spacing improvements:
  - Reduced gap between schema charts from 20px to 10px for compact display
  - Single schema: 50% page width, centered on screen for optimal viewing
  - Two schemas: 90% screen width, arranged in 2 columns, 1 row layout
  - Three+ schemas: 90% screen width, 2 columns per row with automatic row wrapping
  - Enhanced measurement update persistence with aggressive cache-busting
  - URL-based refresh detection to force fresh data after measurement edits
  - Fixed measurement save issues with database transaction commits and browser cache prevention
✅ Dynamic risk calculation system:
  - Real-time risk recalculation when selecting different measurement dates
  - Dynamic "Общий балл: X/X" updates based on selected measurements
  - Risk level text updates (Низкий/Умеренный/Высокий риск) automatically
  - Works with single or multiple measurement selections
  - Uses latest selected measurement for multi-selection scenarios
✅ Chart visualization fixes:
  - Fixed radar chart scaling issue where 2-point scores appeared in yellow zone
  - Corrected data point scaling to match background color zones perfectly
  - Score 0 → Green zone, Score 1 → Yellow zone, Score 2 → Red zone alignment
  - Both measurement data and arithmetic mean scaling fixed
  - Professional hexagonal chart with proper risk zone visualization
✅ Measurement form UI improvements:
  - Fixed indicator item border overlap with score display elements
  - Optimized grid layout: 60% indicator name, 25% input, 15% score display
  - Improved spacing and padding for better visual separation
  - Reduced font sizes for compact indicator names and descriptions
  - Professional two-column layout with clear visual hierarchy
✅ Comprehensive PDF export functionality:
  - Complete medical report generation with all patient information
  - Dynamic risk assessment based on selected measurements
  - High-quality hexagonal chart image capture (1400x1400 resolution)
  - Professional bilingual layout (English structure + Russian content preservation)
  - Includes: patient details, schema info, risk assessment, measurement data, chart image, recommendations, doctor signature area
  - Small PDF export button positioned next to schema titles
  - Automatic multi-page layout with proper content flow
  - File naming: medical_report_[HISTORY_ID]_[SCHEMA]_[DATE].pdf
✅ Complete UI modernization and design system unification:
  - Created comprehensive modern-medical.css design framework
  - Unified all pages to use consistent blue gradient theme
  - Standardized navigation header across all pages
  - Implemented consistent button styling with proper colors:
    - btn-warning: Orange (#F59E0B) with darker border for "Edit" actions
    - btn-success: Green for "Add/Create" actions  
    - btn-danger: Red for "Delete" actions
    - btn-secondary: Gray for "Cancel" actions
  - Applied light blue input field borders (#a8c5f0) with hover effects
  - Translated all interface text to Russian language
  - Modernized page layouts using patients-header-combined structure
  - Updated all forms to use consistent styling and spacing
  - Removed redundant custom CSS and inline styles
  - Achieved complete visual consistency across entire application

## Commands
- `docker-compose up -d` - Start PostgreSQL container
- `python manage.py runserver` - Start Django dev server
- `python manage.py makemigrations` - Create database migrations
- `python manage.py migrate` - Apply migrations
- `python manage.py createsuperuser` - Create admin user

## Next Steps (Future Enhancements)
### Immediate Priorities
- [x] ~~Add chart export functionality (PDF/PNG)~~ **COMPLETED** ✅
- [ ] Add chart legend showing risk zone meanings
- [ ] Optimize chart performance and responsiveness
- [ ] Fine-tune chart appearance and user experience

### Medium-term Features  
- [x] ~~Patient report generation with charts~~ **COMPLETED** ✅ 
- [ ] Historical trend analysis between measurements
- [ ] Advanced chart customization options
- [ ] Data backup and restore features
- [ ] Bulk data import/export

### Long-term Enhancements
- [ ] Mobile-responsive improvements
- [ ] Integration with external medical systems
- [ ] Advanced analytics and reporting dashboard

## Current Status
🎉 **Advanced medical practice management system with authentication, analytics, and PDF export!**

The stomatology practice management system is complete with:
- Patient management with comprehensive forms and full CRUD operations
- Schema-based indicator organization system for multiple assessment types
- Flexible automatic scoring system with user-configurable ranges
- Professional measurement interface with real-time scoring and full CRUD operations
- Interactive hexagonal radar charts with enhanced 3-line text display
- Advanced population analytics with group averages and z-score analysis
- Statistical outlier detection and benchmarking capabilities
- Real-time dynamic calculations scaling from 2 to 1000+ patients
- All medical scoring formulas properly implemented
- Dismissible message system with smooth animations
- Clean, professional UI suitable for healthcare environment
- Research-grade statistical analysis for clinical decision making
- Comprehensive authentication system with role-based access control
- Session security settings meeting healthcare compliance requirements
- **Dynamic risk calculation that updates when selecting different measurement dates**
- **Fixed chart scaling so 2-point scores appear correctly in red risk zones**
- **Professional PDF export with complete medical reports including charts**

## Project Structure
```
stomatology_project/
├── patients/          # Patient management app
├── measurements/      # Measurement tracking and visualization
├── indicators/        # Indicator configuration
├── authentication/   # User authentication and authorization
├── static/           # JS/CSS for charts
├── templates/        # HTML templates
└── docker-compose.yml
```