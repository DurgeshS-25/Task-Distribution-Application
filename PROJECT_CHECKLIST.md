
# ✅ Project Checklist – Task Distribution App

## 🔹 Phase 1 – Authentication & User Management
- [x] Database Setup (`database.py` with engine, SessionLocal, Base)
- [x] Create models:
  - [x] User → id, name, email, password_hash, role, is_active
  - [x] Invite → id, email, token, is_used
- [x] Create schemas (`schemas.py`): SignupRequest, UserLogin, UserOut, InviteRequest, Token
- [x] Add password utils (`utils.py`): hashing, verifying, JWT
- [x] Add get_current_user and admin_required
- [x] Endpoints:
  - [x] GET / (root)
  - [x] POST /admin/invite (admin-only)
  - [x] POST /signup
  - [x] POST /login
  - [x] GET /me (protected)
- [x] Roles:
  - [x] Create admin via create_admin.py
  - [x] Admin can invite
  - [x] User signs up with invite

## 🔹 Phase 2 – Task Management (Core Feature)
- [ ] Create Task model: id, title, description, assigned_to, created_by, status, deadline
- [ ] Create Task schemas (TaskCreate, TaskUpdate, TaskOut)
- [ ] Endpoints:
  - [ ] POST /tasks → create task (admin only)
  - [ ] GET /tasks → list all tasks (admin only)
  - [ ] GET /tasks/my → list tasks assigned to current user
  - [ ] PUT /tasks/{id} → update task (admin only)
  - [ ] DELETE /tasks/{id} → delete task (admin only)
- [ ] Add status workflow (pending, in-progress, completed)
- [ ] Add deadlines & filtering (overdue, upcoming)

## 🔹 Phase 3 – Collaboration Features
- [ ] Add comments model for tasks
- [ ] Endpoint: POST /tasks/{id}/comments
- [ ] Users can comment only on their assigned tasks
- [ ] Admins can comment on any task
- [ ] Add activity log (task created, updated, completed)

## 🔹 Phase 4 – Notifications
- [ ] Add email notifications (via SMTP or SendGrid):
  - [ ] On invite
  - [ ] On task assignment
  - [ ] On task deadline reminder
- [ ] In-app notifications (`notifications` table)
- [ ] Endpoint: GET /notifications (user-specific)

## 🔹 Phase 5 – Frontend Integration
- [ ] Build frontend (React or similar):
  - [ ] Login & Signup pages
  - [ ] Admin dashboard (invite users, assign tasks)
  - [ ] User dashboard (my tasks, notifications)
- [ ] Connect frontend with FastAPI backend (via API calls)

## 🔹 Phase 6 – Deployment & Security
- [ ] Move secrets to .env
- [ ] Add HTTPS (SSL)
- [ ] Containerize with Docker
- [ ] Deploy on cloud (AWS / Heroku / Railway / Render)
- [ ] Add monitoring & logging
