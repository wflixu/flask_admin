

import './App.css'
import Theme from './Theme/index.jsx'
import ObjectBreadcrumbs from './components/ObjectBreadcrumbs.jsx'
import { pgAdmin } from './core/pgadmin.js'
function App() {

  return (
   
    <Theme>
      <ObjectBreadcrumbs pgAdmin={pgAdmin} />
    </Theme>
  )
}

export default App
