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
    * **Key Response Headers:** `Location: /home`, `Set-Cookie`
    * **Session Mechanism:** The server responds with a `Set-Cookie` header containing a session token. Our client must store this cookie.

---

## 2. Data Extraction Flow

**Objective:** Fetch the account balance and transaction history after a successful login.

* **Step 1: Request Home Page**
    * **Endpoint:** `/home`
    * **Method:** `GET`
    * **Authentication:** Requires the **session cookie** obtained from the login step to be sent in the `Cookie` request header.

* **Step 2: Successful Response**
    * **Status Code:** `200 OK`
    * **Content:** The full HTML of the user's account page.

* **Step 3: HTML Parsing**
    Our client must parse the received HTML to extract the data. The following selectors should be used:

    * **Account Balance:**
        * **Selector:** `span#current-balance`
        * **Example:** `<span class="h1 mb-0" id="current-balance">$7,346.05</span>`
        * **Action:** Extract the text content and parse it to a number.

    * **Transaction List:**
        * **Container Selector:** `tbody#transaction-list`
        * **Row Selector:** `tr` (Iterate over each `<tr>` inside the container)
        * **Data Selectors per row:**
            * **Date:** `td.transaction-date`
            * **Label:** `td.transaction-label`
            * **Amount:** `td.transaction-amount`