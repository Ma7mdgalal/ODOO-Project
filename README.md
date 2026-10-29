# 📚 Library Management System
### 🚀 A Custom Odoo ERP Module

A custom **Library Management System** developed using **Odoo, Python, PostgreSQL, and XML** to streamline library operations and manage books, members, loans, and purchases.

The project demonstrates how real-world business requirements can be translated into a functional ERP application through structured data models, automated workflows, and business logic.

---

## 🌟 Project Overview

Managing a library involves more than organizing books. It requires tracking availability, borrowing activities, member information, and purchases while maintaining data consistency.

Our system provides a centralized solution for managing:

- 📚 **Books:** Book information, prices, and availability.
- 👥 **Members:** Member profiles and activity records.
- 📖 **Loans:** Book borrowing and return operations.
- 🛒 **Purchases:** Book purchases and sales tracking.

---

## ✨ Key Features

### 📚 Book Management
- Add, update, and manage books.
- Store book titles, authors, ISBNs, page counts, and prices.
- Track book status: `Available`, `Borrowed`, or `Sold`.
- View borrowing and purchase history.

### 👥 Member Management
- Register and manage library members.
- Store contact information and membership dates.
- Track member borrowing and purchasing activities.
- Manage active and inactive membership status.

### 📖 Loan Management
- Create and manage borrowing records.
- Track borrowing dates and return dates.
- Prevent duplicate active loans for the same book.
- Automatically update book status when loans change.
- Manage loan states: `Borrowed` and `Returned`.

### 🛒 Purchase Management
- Record book purchases.
- Associate purchases with books and members.
- Automatically retrieve book prices.
- Prevent purchases of unavailable books.
- Automatically mark purchased books as `Sold`.
- Open purchase forms directly using the **Buy Book** button.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Backend logic and model development |
| ⚙️ Odoo | ERP framework |
| 🗄️ PostgreSQL | Database |
| 🔗 Odoo ORM | Data models and relationships |
| 🧩 XML | User interface and views |
| 🔐 CSV | Access rights and permissions |

---

## 🏗️ System Architecture

The application consists of four main models:

```text
                  LIBRARY MANAGEMENT
                          |
            +-------------+-------------+
            |                           |
          BOOKS                       MEMBERS
            |                           |
            +-------------+-------------+
                          |
                 +--------+--------+
                 |                 |
                LOANS           PURCHASES
                 |                 |
           Borrow / Return      Buy Books
```

### 📌 Models

| Model | Technical Name | Description |
|-------|----------------|-------------|
| 📚 Book | `library.book` | Stores book information and availability |
| 👤 Member | `library.member` | Manages library members |
| 📖 Loan | `library.loan` | Handles borrowing and returns |
| 🛒 Purchase | `library.purchase` | Handles book purchases |

---

## 🔗 Model Relationships

The system uses **Many2one** and **One2many** relationships.

- One book can have multiple loan records over time.
- Each loan belongs to one book and one member.
- One member can have multiple loans.
- One member can have multiple purchases.
- Each purchase references one book.

### Example

```python
# Book Model
loan_ids = fields.One2many(
    'library.loan',
    'book_id',
    string='Loans'
)

# Loan Model
book_id = fields.Many2one(
    'library.book',
    string='Book',
    required=True
)
```

---

## 🔄 Book Lifecycle

Books have three possible states:

- 🟢 **Available**
- 🟡 **Borrowed**
- 🔴 **Sold**

```text
                  AVAILABLE
                      |
            +---------+---------+
            |                   |
            v                   v
         BORROWED              SOLD
            |
            | Returned
            v
         AVAILABLE
```

### Workflow

1. 📚 A newly created book starts as `Available`.
2. 📖 Creating an active loan changes its status to `Borrowed`.
3. 🔄 Returning the book changes its status back to `Available`, provided no active loan or purchase remains.
4. 🛒 Purchasing an available book changes its status to `Sold`.

---

## 🧠 Business Logic & Validation

### 🚫 Preventing Duplicate Loans

The system prevents multiple active loans for the same book.

```python
def _check_active_loan(self):
    for loan in self.filtered(
        lambda record: record.state == 'borrowed'
    ):
        active_loans = self.search([
            ('book_id', '=', loan.book_id.id),
            ('state', '=', 'borrowed'),
            ('id', '!=', loan.id),
        ], limit=1)

        if active_loans:
            raise ValidationError(
                'This book is already borrowed.'
            )
```

### 🛒 Purchase Validation

Only available books can be purchased.

```python
def _check_books_available(self):
    for purchase in self:
        if purchase.book_id.state != 'available':
            raise ValidationError(
                'Only available books can be purchased.'
            )
```

### 🔄 Automatic Book Status Updates

Book status is determined by purchase records and active loans.

```python
new_state = (
    'sold' if purchase
    else 'borrowed' if active_loan
    else 'available'
)
```

---

## 🖥️ User Interface

The application uses **XML views** to provide a structured interface.

### 📋 List Views
Display books, members, loans, and purchases in organized tables.

### 📝 Form Views
Allow users to create, edit, and view individual records.

### 📑 Notebook Tabs
Display related loans and purchases within Book and Member forms.

### 🛒 Buy Book Button
Opens the purchase form with the selected book automatically populated.

### 🔍 Domain Filtering
Filters available books during purchase selection.

---

## 🔐 Security & Access Rights

Access permissions are configured using:

`security/ir.model.access.csv`

The module grants Odoo internal users the following permissions:

| Model | Read | Create | Write | Delete |
|-------|------|--------|-------|--------|
| 📚 Books | ✅ | ✅ | ✅ | ✅ |
| 👥 Members | ✅ | ✅ | ✅ | ✅ |
| 📖 Loans | ✅ | ✅ | ✅ | ✅ |
| 🛒 Purchases | ✅ | ✅ | ✅ | ✅ |

---

## 📂 Project Structure

```text
library_management/
│
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_member.py
│   ├── library_loan.py
│   └── library_purchase.py
│
├── security/
│   └── ir.model.access.csv
│
├── views/
│   ├── library_book_views.xml
│   ├── library_member_views.xml
│   ├── library_loan_views.xml
│   └── library_purchase_views.xml
│
├── __init__.py
├── __manifest__.py
└── README.md
```

---

## ⚙️ Installation Guide

### Prerequisites

- Odoo installed and configured
- PostgreSQL database
- Python environment compatible with the installed Odoo version
- Access to an Odoo custom addons directory

### Installation Steps

**1️⃣ Clone the repository**

Clone this repository using Git or download it as a ZIP file.

**2️⃣ Add the custom module**

Copy the `library_management` folder into your Odoo custom addons directory.

**3️⃣ Configure Odoo**

Ensure the custom addons directory is included in the Odoo `addons_path`.

**4️⃣ Restart the Odoo server**

Restart Odoo to detect the module.

**5️⃣ Update the Apps List**

Enable Developer Mode and update the Apps List if needed.

**6️⃣ Install the module**

Search for **Library Management** in Odoo Apps and click **Install**.

**7️⃣ Start managing your library! 🎉**

---

## 🎯 Example Workflow

### 📚 Step 1: Add a Book

Create a new book with its title, author, ISBN, and price.

**Initial Status:** `Available`

### 👤 Step 2: Register a Member

Add a new library member with their name and contact information.

### 📖 Step 3: Borrow a Book

Create a loan linking the member to the selected book.

**Status:** `Available → Borrowed`

### 🔄 Step 4: Return the Book

Update the loan status to `Returned`.

**Status:** `Borrowed → Available`

### 🛒 Step 5: Purchase the Book

Create a purchase record for an available book.

**Status:** `Available → Sold`

---

## 📈 Learning Outcomes

This project provided hands-on experience with:

- 🐍 Python development within Odoo
- ⚙️ Custom ERP module development
- 🗄️ Relational database modeling
- 🔗 One2many and Many2one relationships
- 🧠 Business logic implementation
- 🚫 Data validation and error handling
- 🔄 ORM method overriding
- 🖥️ XML view customization
- 🔐 Access rights management
- 🚀 Translating business requirements into software solutions

---

## 🚀 Future Enhancements

Potential improvements include:

- 📊 Interactive dashboard with library KPIs
- 📅 Automated overdue book tracking
- 📧 Email notifications and return reminders
- 🔍 Advanced book search and filtering
- 📦 Multiple-copy inventory management
- 💰 Historical purchase price tracking
- 🔐 Role-based access control
- 🛡️ Additional loan availability validation
- 🧪 Automated testing

---

## ⚠️ Current Limitations

This is a learning-focused Odoo module with opportunities for further development.

- Loan validation prevents duplicate active loans but does not explicitly block loans for sold books.
- Purchase prices are related to book prices rather than preserved as historical transaction snapshots.
- Each book record represents a single tracked item.
- Return dates are not automatically synchronized with loan status.
- Internal users currently have full CRUD access to all four models.

---

## 💡 Final Thoughts

This project demonstrates how **Odoo ERP can be customized to transform business requirements into a structured management system**.

Through Python, Odoo ORM, XML, and relational data modeling, the module combines data management, business logic, and user interface customization into one application.

---

### ⭐ If you find this project useful, consider giving it a star!

**Built with Python, Odoo, and a passion for learning. 🚀**
