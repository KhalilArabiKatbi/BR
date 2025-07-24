# Frontend Development Guide

This guide provides a comprehensive overview of the frontend codebase, including the project structure, how to add new features, and best practices to follow.

## Table of Contents

1.  [Project Structure](#project-structure)
2.  [Getting Started](#getting-started)
3.  [Dependencies](#dependencies)
4.  [Routing](#routing)
5.  [State Management](#state-management)
6.  [API Calls](#api-calls)
7.  [Adding a New Component](#adding-a-new-component)
8.  [Styling](#styling)
9.  [Internationalization](#internationalization)

---

### Project Structure

The frontend is a React application built with Vite. Here's a breakdown of the key directories:

-   **`public/`**: Contains static assets that are not processed by the build pipeline.
-   **`src/`**: The main source code of the application.
    -   **`apis/`**: Handles API requests and configurations.
        -   `AxiosConfig.jsx`: Configures Axios for making HTTP requests, including interceptors for handling authentication and errors.
        -   `AuthServices.jsx`: Defines authentication-related API calls.
    -   **`assets/`**: Stores static assets like images and icons.
    -   **`components/`**: Contains reusable React components.
        -   `Auth/`: Components related to authentication (e.g., `Login.jsx`, `Logout.jsx`).
    -   **`routes/`**: Manages application routing.
        -   `AdminRoutes.jsx`: Defines routes accessible only to admin users.
        -   `AnonymousRoutes.jsx`: Defines routes accessible only to unauthenticated users.
    -   **`stores/`**: Manages global state using Zustand.
        -   `authStore.jsx`: Handles authentication-related state and actions.
    -   **`styles/`**: Contains CSS modules and global stylesheets.
    -   **`translations/`**: Stores translation files for internationalization.
-   **`vite.config.js`**: Configuration file for Vite.
-   **`package.json`**: Lists project dependencies and scripts.

---

### Getting Started

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Run the Development Server**:
    ```bash
    npm run dev
    ```

    The application will be available at `http://localhost:5173`.

---

### Dependencies

The project uses the following key libraries:

-   **React**: For building the user interface.
-   **Vite**: As the build tool and development server.
-   **React Router**: For handling client-side routing.
-   **Zustand**: For lightweight global state management.
-   **Axios**: For making HTTP requests to the backend.
-   **React-i18next**: For internationalization.
-   **js-cookie**: For managing cookies.

---

### Routing

Routing is managed using `react-router-dom`. The main routes are defined in `src/App.jsx`.

-   **`AnonymousRoutes`**: These routes are only accessible to users who are not logged in. If a logged-in user tries to access these routes, they will be redirected to the `/home` page.
-   **`AdminRoutes`**: These routes are protected and only accessible to users with the 'Admin' role. Unauthorized users will be redirected to the login page.

**To add a new route:**

1.  Open `src/App.jsx`.
2.  Add a new `<Route>` component within the `<Routes>` block.
3.  If the route should be protected, wrap it with the appropriate route component (e.g., `<AdminRoutes />`).

---

### State Management

Global state is managed using Zustand. The `authStore.jsx` file (`src/stores/authStore.jsx`) is a great example of how to create a store.

**To create a new store:**

1.  Create a new file in the `src/stores/` directory (e.g., `myStore.jsx`).
2.  Use the `create` function from Zustand to define your store's state and actions.

**To use a store in a component:**

```jsx
import useMyStore from '../stores/myStore';

const MyComponent = () => {
  const myValue = useMyStore((state) => state.myValue);
  const myAction = useMyStore((state) => state.myAction);

  // ...
};
```

---

### API Calls

API calls are made using Axios. The base configuration is in `src/apis/AxiosConfig.jsx`. This file sets up:

-   The base URL for the API.
-   Request interceptors to add the authentication token to headers.
-   Response interceptors to handle global errors (like 401 Unauthorized).

**To add a new API service:**

1.  Create a new file in `src/apis/` (e.g., `ProductServices.jsx`).
2.  Import `axiosInstance` from `AxiosConfig.jsx`.
3.  Define your API calls as async functions.

Example (`ProductServices.jsx`):

```jsx
import axiosInstance from './AxiosConfig';

export const productService = {
    fetchProducts: async () => {
        return axiosInstance.get('/products');
    },
    createProduct: async (productData) => {
        return axiosInstance.post('/products', productData);
    },
};
```

---

### Adding a New Component

1.  Create a new file for your component in the `src/components/` directory. If it's a larger component with its own state and logic, consider creating a new folder for it.
2.  Write your component code.
3.  If the component needs to be part of a route, add it to `src/App.jsx`.

---

### Styling

The project uses a combination of global CSS (`App.css`) and CSS modules (`*.module.css`).

-   **Global Styles**: For application-wide styles, modify `src/App.css`.
-   **Component-Specific Styles**: For styles that should be scoped to a single component, create a CSS module file (e.g., `MyComponent.module.css`) and import it into your component.

```jsx
import styles from './MyComponent.module.css';

const MyComponent = () => {
  return <div className={styles.myClass}>...</div>;
};
```

---

### Internationalization

Internationalization is handled by `react-i18next`.

-   **Translation Files**: English and Arabic translations are stored in `src/translations/en/global.json` and `src/translations/ar/global.json`, respectively.
-   **Initialization**: `i18next` is initialized in `src/main.jsx`.

**To use translations in a component:**

```jsx
import { useTranslation } from 'react-i18next';

const MyComponent = () => {
  const { t } = useTranslation('global');

  return <h1>{t('my_translation_key')}</h1>;
};
```

To add a new translation, add the key and value to the JSON files for each language.
