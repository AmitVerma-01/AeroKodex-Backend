# AeroKodex Admin Documentation

## Accessing the Panel
Login at `/admin/` utilizing your system superuser credentials.

## 1. Analytics Dashboard
Upon logging in, the home page will present real-time Analytics:
- **Total Products**: Sum of active aerospace and material packages in your database.
- **Workshop Bookings**: Global total of reservations processed.
- **Quote Requests**: The volume of standard specification submissions hitting your inbox.
- **Conversion Rate**: Indicates percentage of `QuoteRequests` manually toggled to `--CONVERTED--` status vs the overall inquiries sum.

## 2. Managing Products & Variants
Navigate to **Products**.
- Create a Category first (e.g., *Materials*).
- From the main Product form, you have full inline capability to:
  - Add **`meta_title`**, **`meta_description`** and **`meta_keywords`** to boost Organic SEO directly from the UI.
  - Insert unlimited **Product Variants** inline at the bottom specifying varying size grades and integer stock levels.
  - Apply unlimited **Product Images** inline, declaring which should be the primary `feature`.
  - Toggle **`is_active`** inline from the main dashboard to immediately un-publish low-stock items.

## 3. Workshops & Booking Workflows
Navigate to **Workshops**.
- Outline capacity limitations in `total_seats` vs `seats_available`.
- The Django REST API automatically manages atomic seat decrementing when new users enroll.
- **Email Notifications**: Next to `Booking` actions, select specific attendees, open the bulk Action dropdown and utilize **Send Email Notification to Attendees** for pre-workshop advisories.
- **CSV Data Pulling**: To manually register walk-ins or pass manifests to instructors, select bookings and click **Export selected to CSV**.

## 4. CMS (Content Management System)
Navigate to **CMS**.
- **SiteContent**: Use `section_key` (e.g. `home_hero`, `about_mission`) to store text or robust HTML injected seamlessly onto next.js frontend elements.
- **Testimonials**: Update consumer feedback. Include custom rating matrices internally up to 5 stars.
- **Blog**: Publish robust articles defining internal `author` assignments logic, complete with its own SEO headers logic.

## 5. Intake & Quotes Triage Pipeline
Navigate to **Inquiries**.
- Both simple 'Contact Submissions' and advanced multi-step 'Quote Requests' store here automatically.
- New entries inherently prompt automatic emails back to the user acknowledging receipt to ensure transparency.
- Track progression via `Pending` → `Reviewed` → `Converted`.
- Fully exportable via standard CSV hooks.
