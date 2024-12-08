import { Counter } from "./components/Counter";
import { FetchData } from "./components/FetchData";
import { Home } from "./components/Home";
import Dashboard from "./components/Dashboard";

const AppRoutes = [
  {
    path: '/counter',
    element: <Counter />
  },
  {
    path: '/fetch-data',
    element: <FetchData />
  },
  {
    index: true,
    path: '/dashboard',
    element: <Dashboard/>
  }
];

export default AppRoutes;
