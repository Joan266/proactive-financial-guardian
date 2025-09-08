# Bank of Anthos Interface Documentation

This document describes the endpoints and flows required for the "Proactive Financial Guardian" to interact with the Bank of Anthos application. This information was obtained through source code and network analysis (F12).

The application follows a **traditional form submission** pattern with page reloads, not a REST API model with Fetch/XHR.

---

## 1. User Authentication Flow

**Objective:** Log in to establish a valid session that allows us to perform subsequent queries.

* **Step 1: Submit Credentials**
    * **Endpoint:** `/login`
    * **Method:** `POST`
    * **Request Type:** `application/x-www-form-urlencoded` (Form Data)

* **Step 2: Request Payload**
    ```
    username: (e.g., testuser)
    password: (e.g., bankofanthos)
    ```

* **Step 3: Successful Response**
    * **Status Code:** `302 FOUND`
    * **Key Response Headers:** `Location: /home`
    * **Session Mechanism:** The `frontend` service receives the credentials, internally calls the `userservice` to get a JWT, and manages the user's session via **cookies** in subsequent responses. Our client must store and resend these cookies.

---

## 2. Balance and Transaction Query Flow

*(This section will be completed once we analyze these requests, but it will follow a similar pattern)*

* **Endpoint:** `/` (Home page)
* **Method:** `GET`
* **Authentication:** Requires the **session cookie** obtained after a successful login.
* **Response:** The page's HTML, from which we will need to parse the balance and transaction list.